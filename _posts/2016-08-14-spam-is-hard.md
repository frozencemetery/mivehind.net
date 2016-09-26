---
layout: post
---

I get a lot of spam.  There are a variety of reasons for this - I don't like
captchas or javascript hiding of my email address, I have public PGP keys, I'm
subscribed to public mailing lists - and the result is that I end up with
around a 10% spam rate.  I don't know if this sounds like a lot, but it sure
feels like it, especially when all of these messages go straight to my inbox
and don't fall into any filters.

If there's one thing I'd change about all this, it'd be to have everyone who
runs a public mailing list perform some kind of spam control.  Probably the
best thing to start with would be to whitelist posts from subscribers and put
everything else in moderation.  But honestly, it's better than the actual
nothing that so many lists I'm on seem to have.  And as far as I can tell, the
various Debian project mailing lists are my single largest provider of spam.

## Why this is hard for me

I think it's important for users to be able to replace components of their
software stack at will.  Until a couple years ago, I believed that everyone
who advocated free software cared about this.  I won't harp farther on that
here right now.

So when I decided that I needed some spam control, naturally I asked those
around me how they were handling this particular part of the email firehose.
Invariably I received one of two answers:

1. I don't get spam and / or I'm worried about missing messages from a spam
   filter
2. My provider takes care of this for me.

If one fall into (1), then they lucky and I'm a bit jealous if I'm being
really honest.  Still, it doesn't solve my problem.  And if they fell into
(2), not only does it not help me since I am my own provider (as part of
CMUCC), but their in question is invariably Google, which is even worse from
my perspective.

So, I asked the internet.

## afew

I use an email frontend called [notmuch](https://notmuchmail.org).  This is
largely extraneous to this discussion, except that when notmuch users need
more heavyweight classification they tend to turn to
[afew](https://github.com/teythoon/afew).  So I tried it, despite it not
having distro packaging.

The first thing I tried was its spam detection.  After staring at its
documentation and trying to determine the difference between `--learn`,
`--update`, and `--update-reference`, I followed the setup instructions and
trained it on a corpus of several thousand of my spam messages.  I then asked
it about my messages from the past two months.  It didn't flag a single one.

So I got curious and tried its general classifier support.  After learning the
hard way that it doesn't error out (or even warn!) if files it needs don't
exist, I did get its general classifier working.  I ran it against my inbox.
I mentioned above that I'm on a several mailing lists: one nice feature for
classification purposes is that they all have a consistent `To:` (or `Cc:`)
header.  Of the hundred messages tested, afew didn't get a single one.

Conclusion: not ready for prime time.

## spamassassin

You can't get very far on the internet without running into mention of this
thing from the Apache project.  It's even packaged in distros.  Unfortunately
it's written in Perl, but I wouldn't be using Debian if I couldn't stomach
some Perl, and besides, it's still a far cry from all the Paul Graham (yes I
do literally mean Paul Graham)-inspired Bayesian clients.

So I fired it up.  Classification turned out to be pretty good; I trained it
in the same way I did for afew, and it properly detected all the spam from my
inbox without any false positives or negatives.  Great start.

Then I became curious and tested it on all my mail.  All ~150,000 messages.
There were more false positives here, and I had to teach it about those, which
is fine.  The problem was how long it took.  It took four days.  That doesn't
properly express my frustration, so let me give it the proper emphasis:

It took **four days**.

### I'm sorry, what?

Okay let's back up.  Why did it take so long?

As far as I can tell, spamsassasin was designed for use with procmail.
procmail likes piping messages.  So the way spamassassin wants to work is to
receive a message on stdin, classify it, and return a score.

In theory, one can achieve better performance by spinning up a `spamd` process
or 128 and connecting to them with `spamc`.  I actually recorded the four days
time with this approach; in hindsight I should have probably checked
performance characteristics, but I don't want to wait another four days.

(For clarity purposes, in the following examples I will be eliding some
external logic for handling results of spamc.)

The stdin requirement actually turns out to be extremely irritating because it
becomes nontrival to use with `xargs`.  To elaborate on that, normally we
would want to do something like this:

```bash
notmuch search --output=files 'tag:new' | xargs spamc -c
```

but we can't, for two reasons: first, spamc/spamassassin demands that it take
message bodies on stdin, and second that it can't handle multiple messages at
a time.  (More on that second point in a moment.)

There are two approaches one can take instead:

```bash
notmuch search --output=files 'tag:new' | while read m; do
   spamc -c < "$m" &
done

for job in $(jobs -p); do
    wait $job;
done
```

This has the advantage of spawning many processes, but it has the drawback of
spawning many processes.  Instead, we'd really like to be able to limit that
number, like we can with xargs:

```
notmuch search --output=files 'tag:new' | xargs -n 1 -P 8 bash -c 'exec spamc -c < "$1"'
```

and then we can control the number of running processes by adjusting the value
of `-P`.  This has the disadvantage of being absolutely terrible.  We've now
increased the syscall overhead, and on top of that, the throughput barely goes
up over the single-threaded approach.

### Perhaps the protocol...?

spamc only being able to process one message at a time seems like terrible
design.  But maybe I can work around that by speaking the protocol myself.

So I started reading through the code to find out how the protocol works.  And
all I will say about that is that I wish they used a consistent style, and
that I gave up and switched to using wireshark.

I could explain it, or I could just show this Python client I wrote:

```Python
#!/usr/bin/python2

import socket

s = socket.socket()
s.connect(("localhost", 783))

m = open("/home/frozencemetery/Mail/local/cur/1428080852.M434957P18350Q17727.kirtar:2,S",
         "r").read()

p = "\r\n".join(["CHECK SPAMC/1.5",
                 "User: frozencemetery",
                 "Content-length: %s",
                 "",
                 "%s",
]) % (len(m), m)

print(p)
s.send(p)

print(s.recv(2048))

print(p)
s.send(p)

# this recv() will always fail
print(s.recv(2048))
```

So it looks a lot like HTTP.  And, just like HTTP, there are some fields that
really should be optional and aren't.  Documentation indicates that the
"SPAMC/1.5" is supposed to be a client-and-version string.  It's not.  The
server drops your connection if you don't send that.

The other, much more infuriating, part of this is what I've highlighted with a
commment.  That is, the server closes the connection after replying to the
query.

### Go back to that part where the multithreaded doesn't give a speedup

So I filed a bug, which I'm not going to link here because I'm too annoyed at
the developer response to open it again.  In my bug, I asked for the spamd
server to not close the socket every message, thus allowing for multiple
queries and actual speedup.  I provided performance numbers (quad-core CPU
with 16 GB DDR3) to show that the whole "classify 150,000 messages"-thing
isn't CPU bound, but rather is alternately bound by `fork()` and the TCP
handshake and closure (which takes up fully three quarters of all the traffic
that is sent).

They won't be fixing this.  The tool is designed not to scale, and there's
nothing else I can say to convince the developers to care.

## rspamd

To end on a more lighthearted note, I want to give "honorable" mention to
another client I looked at, at the suggestion of a friend: rspamd.  Maybe this
client works great; I didn't actually try it.  I was put off for two reasons:

First, they seem to abhor the distro model.  I'm not sure why this is.  Their
README claims, somewhat deceptively if you ask me, that "Rspamd is packaged
for the major Linux distributives".  Dig a little further, and you'll find
that it's not packaged *in* any well-known distro.  They actually ltierally
meant that it is packaged *for* them - as in, they provide you packages for
those distros.

And in what I consider much more deceptive, the README also states that
"Furthermore, Lua programs are very fast and their performance is rather
[close](http://attractivechaos.github.io/plb/) to pure C."  I'm not sure *why*
they felt the need to say this; the next sentence is even "However, you should
mention that for the most of performance critical tasks you usually use the
rspamd core functionality than Lua code.".  I'd like it to be clear here: the
author's own linked benchmark does not demonstrate what the text claims.

So I submitted a pull reqest for this.  The author very politely told me that
I was wrong, that he didn't care, and immediately started swearing.  You know,
all the polite things you want a software project to do to welcome potential
users and contributors.

Happy Sunday to you.
