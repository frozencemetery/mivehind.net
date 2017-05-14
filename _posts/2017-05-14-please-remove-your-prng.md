---
layout: post
tags:
  - tech
  - security
---

The gist of this post is that if your program or library has its own PRNG, I
would like you to remove it.  If you are not convinced that this is a good
idea, read on; if you want links on what to do instead, skip to the second
section.

# Why do you have this?

I believe in code re-use, in not re-inventing the wheel where necessary, and
in cooperation.  So if code to do something exists, and there are no strong
reasons why I shouldn't use it: I use it.  Formulated in this manner it sounds
almost like a strict rule; in practice, the same result can be achieved for
new code just by laziness.  For existing code, it becomes a maintainability
question.  I maintain code as well as writing it (as everyone who writes code
should), and while I won't deny a certain satisfaction in well-oiled
machinery, less would be better.  So everything we maintain should serve a
purpose, and reducing unneeded size, scope, and complexity are worthwhile.

Every project is different, which means your project's reasons for having a
PRNG will be different as well.  Maybe it doesn't care about the quality of
the pseudorandom numbers (at which point it should probably just read
/dev/urandom).  Or maybe it's performing cryptographic operations (use
`getrandom(2)` or similar).  But I invite you to think about whether
continuing to maintain your own is worth it, or whether it might be better to
use something which has been more strongly audited (e.g., the kernel CSPRNG).

To look at an example: a few months ago now, I performed this change for krb5.
In our case, we had a Fortuna implementation because quality entropy used to
be difficult to come by.  Fortuna specifically was used due to its ability to
recover from low-quality input.  However, upon further examination, the time
to recover is quite long (so it only really helps the server), and in the mean
time, operation will appear to be normal, with low quality random numbers.
Since there're already quality random numbers available on all server
platforms we support, I added the option to just use them directly.  (This
describes the current behavior on Fedora, as well as the behavior for all
future RHEL/CentOS releases).

# What to do instead

For this post, I will be focusing on Linux.  If you are not in a Linux
environment, you
[call](https://msdn.microsoft.com/en-us/library/windows/desktop/aa379942(v=vs.85).aspx)
a [different](http://man.openbsd.org/getentropy.2) function.

Anyway, the short answer is: you should use `getrandom(2)`.

The longer answer is just me telling you how to use `getrandom(2)`.  For that,
I want to draw from [this post](https://www.2uo.de/myths-about-urandom/) which
contains a useful diagram about how /dev/random and /dev/urandom relate.  The
author points out two issues with using /dev/urandom directly on Linux (that
do not occur on certain BSD, where one just uses /dev/random instead): 

- First, that /dev/urandom is not guaranteed to be seeded.  `getrandom(2)`
  actually provides seeding guarantees by default.  More precisely, it will
  block the call until the requested number of bytes can be generated; in the
  case of the urandom pool, this means until the pool has been seeded.  (If
  this behavior is not desired, one should just read directly from
  /dev/urandom instead.)

- Second, that one may wish to use /dev/random despite it being slower if
  they're feeling especially paranoid.  There's a `getrandom(2)` flag for
  this, it turns out: `GRND_RANDOM`.

There's one pitfall with this approach, which is that (for reasons that are
opaque to me) glibc was slow to add a wrapper for this function.  (See:
[rhbz](https://bugzilla.redhat.com/show_bug.cgi?id=1253474),
[upstream](https://sourceware.org/bugzilla/show_bug.cgi?id=17252).)  So if you
want to support older versions of glibc, you have to use `syscall(2)` instead,
like [this](https://github.com/krb5/krb5/blob/master/src/lib/crypto/krb/prng.c#L102-L128).

# ~~Pie in the sky~~ Future work

A while back, I remember reading (but can no longer find) a post which
surveyed open source software's usage of `rand()/srand()` and related
functions.  There were some decidedly bizarre usages in there, but most of
them were just run-of-the-mill incorrect.  Anyway, inspired by that, I've been
toying with the idea of writing a shim library of sorts to make these
functions actually return cryptographically random numbers, discarding seeding
and such.  The only real pitfall I'm aware of with this is users of these
functions that expect deterministic behavior, but I'm not really sure I want
to care.  Maybe an environment variable for configuration or something.
