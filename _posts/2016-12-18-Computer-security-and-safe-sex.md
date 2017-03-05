---
layout: post
tags:
  - tech
  - security
---

I work in computer security (security engineering).  It is a hobby that grew
into a job, and as such is something I have cared about for some time now.
For the most part, I work on "defense": not doing penetration testing or
anything like that, but rather building and maintaining tools for people to
protect themselves.  (My current professional focus is Kerberos, for
instance.)  I have previously performed "offense" (albeit in a
non-professional capacity with [PPP](https://ctftime.org/team/284)), and in a
moment will discuss part of why I tend not to do that anymore.

Anyway, this position means that I come in contact with many other security
people.  And, increasingly, I come in contact with a particular narrative that
I strongly dislike: that security is an unsolvable problem.  (I should note
here that there are problems with security culture more important than this
one; however, that is not in scope for this post.)

So, security is unsolvable, they say.  And the conclusion that is usually
drawn as a result is that we ought to be as uninteresting, and as useless to
target, as we possibly can.  Thus, we will hopefully (if we cross our fingers
and wish really hard) both avoid surveillance and direct targeting entirely.

As best I can tell, this position of hopelessness ironically originates from
the actions security people themselves have taken.  It was no doubt
exacerbated by the revelations of Snowden, Manning, and others, but I think
that the root cause is the endless procession of critical vulnerabilities that
we seem to pride ourselves on discovering.  There is money to be had in
exploit sales, after all, and more importantly, there is prestige.

There is no prestige when something you have built resists an exploit, when it
mitigates a flaw.  The only conferences that gets one invited to are
corporate; the only people interested are "enterprise"; the reward is a few
handclaps, compared to the giant headlines when OpenSSL breaks again.  (It's a
technical post, so I have to take shots at OpenSSL.  That's the rule.)

And I think both of these combine into the idea that it is only a matter of
time for a critical exploit to be found in *any* given piece of software.
Fortunately, there are two problems with this idea: first, that it is not
true, and second, that even if it were true, it does not matter.

Consider the meaning of the idea: it is impossible for any piece of software
to be free of security bugs.  This means that it is impossible for any piece
of software to be correct, so all software must either have an infinite number
of bugs, or there must be a finite number.  It is ridiculous for a
finite-length piece of software to have an infinite number of bugs, so as long
as we continue to remove bugs, it will eventually be bug-free.  So, assuming
we continue to remove bugs at a rate faster than we add them (which seems to
be the case; rarely do bugfixes introduce new bugs, though it happens), we
approach bug-free.

But despite the idea being patently false, even if I grant the premise, there
is no need for closing our eyes and wishing.  We have, today, incredible
containment tools in Linux - SELinux and virtual machines being perhaps the
most powerful, among others.  If one is really worried about compromise of a
particular piece of software, wedge it off in its own world.  Strengthen one's
cryptography; layer security; reduce trust; and on and on.  There are so many
things that can be done now it is difficult to enumerate them.

### What happened to the cypherpunks?

And maybe this is the reason the myth has not gone away.  It is easier to
decry everything as broken, unfixable, then to actually learn what the
domain's duct tape and bandages are (so to speak).  It is **far** easier to
yell about everything being terrible then to actually put on knee pads and go
fix the problems.

Because there are people, today, who do work to address these issues.  Rust is
a programming language designed to remove entire classes of vulnerabilities.
People produce entirely open hardware now.  Strong - really strong -
cryptography is readily available for one's communication.  And we are even
making traction on the Trusting Trust problem:
[fully reproducible builds](https://reproducible-builds.org/) are in sight,
thanks to Debian contributors and other hobbyists.

If you can attack software, and you have understanding of what you are doing,
you can defend that software.  This should be self-evident.  We can do better.

### What do I want?

Another thing I did when younger was go to Catholic school, with all that
entails.  And it strikes me that our climate here is very similar to a
particular nugget of "sex education" we received there: no birth control is
100% effective, so we ought to fully abstain from sexual contact entirely.
While the premise is true, and while abstinence even may work for a handful of
people, the idea that it is actually an effective preventative measure does
not pan out in the larger case (see also: AIDS).

Instead, since the idea that condoms are not enough protection is hammered
into teenagers's skulls (and also since God hates them), when they inevitably
start having sex they do not use protection.  Likewise, since the idea that
defensive measures are not enough protection is hammered into developers's
skulls (and also since offensive security people hate them), when they
inevitably start writing and deploying software they do not use them.

So what do I want here?  I want security to stop spreading fear, first, and I
want glorification of the broken (and the breakers) to take a backseat to
glorification of the strong (and the fixers).

To paraphrase a quote (whose source I have forgotten, apologies): the real
security people are not the ones who tell you that everything is broken.  The
real security people are those who tell you to use Signal, use QEMU: who tell
you how to fix it.
