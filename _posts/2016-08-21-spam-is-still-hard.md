---
layout: post
---

This is a follow-up to
[last week's post](https://mivehind.net/2016/08/14/spam-is-hard/) on bulk spam
processing.  Forewarning: this goes downhill quickly and stays there.  If you
are the author of one of these projects, and care about having users, please
consider fixing your project rather than complaining to me (though if you want
suggestions I am happy to offer them).

# Or, the Paul Graham showcase exhibition

Yes okay, you could also call it the Paul Graham show because this is all the
clients I avoided last time because they cite his essay.

## spamprobe

A friend recommended this tool, so I gave it a try.  Reading through the
README, I saw some nice things - the ability to process Maildir and the
ability to process multiple messages in a single process invocation among
them, but there were also some things I did not like.

First, there is this flag: `-a char`.  The description of this flag explains
that what's going on is that spamprobe operates only on ascii, and
accomplishes this by changing all non-ascii into the specified character (by
default 'z').  (There is also a flag to have it store the eighth bit, but this
doesn't actually add UTF-8 support in.)  So this tool won't work at all for
people who receive a lot of non-English mail.

Second, assertions seem to be off in the codebase by default.  The text
associated with this states that "Generally this [enabling assertions] is not
desirable for production use since the assertions reduce performance.".
Alarming, but this seems to be common practice.  Perhaps I'll go into why this
is bad in another post.

I'd also heard several words of caution from various sources that the database
for spamprobe grows rather fast, so I was watching that.  I didn't actually
use this tool for very long though, as will be seen, so I can't really speak
to this particular problem.

So alright.  Training time.  I fed it in my spam corpus:

```bash
notmuch search --output=files tag:spam | xargs spamprobe -v spam
```

It took 90 seconds to process the ~4 thousand messages, which is not bad at
all.  The resulting database is 50 MB, which is very workable.

Unfortunately, it has a TON of false positives when run over incoming mail.
So I started training some of the non-spam messages as well:

```bash
$ notmuch search --output=files tag:sent and not tag:spam | xargs spamprobe good
libpng warning: iCCP: profile 'ICC Profile': 'RGB ': RGB color space not permitted on grayscale PNG
```

Wait, what?  Who called libpng?  I'm doing email processing here; have I been
had?

Well, sort of.

```bash
$ ldd $(which spamprobe)
        linux-vdso.so.1 (0x00007ffd1f4fb000)
        libdb-5.3.so => /usr/lib/x86_64-linux-gnu/libdb-5.3.so (0x00007fe42e999000)
        libgif.so.7 => /usr/lib/x86_64-linux-gnu/libgif.so.7 (0x00007fe42e78f000)
        libpng16.so.16 => /usr/lib/x86_64-linux-gnu/libpng16.so.16 (0x00007fe42e55b000)
        libjpeg.so.62 => /usr/lib/x86_64-linux-gnu/libjpeg.so.62 (0x00007fe42e2f0000)
        libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007fe42df6f000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fe42dc69000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007fe42da53000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fe42d6b2000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007fe42d494000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007fe42d279000)
        /lib64/ld-linux-x86-64.so.2 (0x000055f282a14000)
```

Comforting.  The README says that this is because spamprobe "[a]nalyzes image
attachments to extract useful terms for scoring.  This catches the majority of
spams with only images and no words".  A quick skim through the buildsystem
suggest no way to turn it off, so this isn't going to work for me given the
amount of malware I receive.

```bash
sudo aptitude purge spamprobe
```

## spambayes

This one's in python, which is novel I suppose.  Immediate checks: no image
processing library dependencies.  Good so far.

Turns out, this one's just unmaintained.  I'm not sure why it's packaged.
Sourceforge page and a SVN repository there at least, but no changes since
late 2008.

### Brief note on unmaintained code

EMail can be very scary.  We're working with untrusted data from the
internet - anyone can send me mail.  The tools need to be hardened for this,
audited for this, and maintained so that having the hardening and auditing is
meaningful.

## spamoracle

If spambayes was novel for being in python, well then hold on because this
one's in O'Caml.  It also seems to call itself "Saint Peter" for reasons that
are not at all clear to me.  Points for the O'Caml, at least.  Personally I
think that "spamoracle" is a more entertaining name because it encapsulates
the feeling I imagine people get using Oracle tooling perfectly.

Unfortunately, it's also "slanted towards Western European languages, i.e. the
ISO Latin-1 and Latin-9 character sets" so this one isn't going to work well
for everyone.  And it's aimed at procmail, so it's probably not going to work
well for me, either.

Also?  All of the examples in the man page that involve piping to a pager pipe
to more(1).  To each their own I suppose, but this tool isn't that old... is
it?  Well, where's the upstream and when did they release?

It's not listed in the package, but if you search around hard enough (I looked
at the watchfile, but it's also the fifth or so DDG result for "spamoracle"),
it's [this person's](http://pauillac.inria.fr/~xleroy/software/) pet project.
Well done making a thing, but 1.0 is late 2002, 1.1 is immediately thereafter,
two 1.3 versions happen in June 2003, and 1.4 happens in October 2003.

Also there's no VCS repository, so we won't be going to space on this anytime
soon.

## bmf

All of these projects frontload the Paul Graham essay and push it harder than
their own homepate.  It's really strange.  I'm mentioning this here because I
also had a hard time finding the page for this one.  It seems to be a
Sourceforge page with no repository, and the website link doesn't work (did
they never set it up with Sourceforge)?  Unclear.

## bsfilter

Ruby isn't quite as novel as O'Caml, but it's definitely something I don't see
a lot of.  The documentation for this one seems to be entirely in Japanese,
which makes sense given that it's ruby.  I claim to speak a couple languages,
but this isn't one of them.  Good on them for supporting non-ascii, though.

## qsf

No VCS repository.  Also it seems to need mysql, so it's probably working for
a different use case than mine.

## And I'm out

There are no more general-purpose (or even procmail-specific, irritating
though that interface is) spam classification tools in Debian.  I'm done.
Either I make one of the ones I've looked at work or I need to write my own.
