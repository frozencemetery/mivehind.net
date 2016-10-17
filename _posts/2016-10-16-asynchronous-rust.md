---
layout: post
---

Multiple people have asked me this week whether my blog "is basically all
technical stuff".  The answer is of course that yes, it is mostly technical
things, but this isn't by choice.  In response I wanted to make an extremely
non-technical post this week, but it turns out that those take substantially
more time for me to write.  (I haven't thought too hard about why this is yet
in an effort to not deprive myself of a future post on the subject.)

Anyway, here's this thing instead.

### Why this, frozen?  Why now?

Those are fair questions.  The crux of the problem is that instead of working
on my post for this week I spent the time playing^w writing rust for my
project Trapper.  This is relevant because Trapper involves Nethack and there
was a full moon.  Relevant to me, anyway.

So I was writing some Rust.  In case this changes in the future: I'm staring
at rustc 1.10.0 for reference (with 1.12.0 the most current stable release).
Trapper is my "get to know the language" project: it both serves a purpose
(for me, anyway), and is a nontrivial piece of software to write.  Which
mostly means that I went in with a lot of problems that I mostly know how to
solve in other languages but not in Rust.

To collapse this particular yak, I ended up needing to perform asynchronous IO
on some file descriptors.  Which seems fine and dandy; we go look at the
standard library and get the
[read trait](https://doc.rust-lang.org/1.5.0/std/io/trait.Read.html#tymethod.read)
which states that "This function does not provide any guarantees about whether
it blocks waiting for data" which sounds about like what I'm looking for.  If
you read it right.  And the moon is full.  Which it is, so we press onward.

But it doesn't matter, because nothing implements `Read` in std in a
nonblocking fashion.  And this has been an open issue against rust since
[2013](https://github.com/rust-lang/rust/issues/6842) (later moved from
"issue" to ["rfc"](https://github.com/rust-lang/rfcs/issues/1081)).  If one
searches around, the recommended way to solve the problem of needing async IO
is to just spin up a separate thread for each socket, which reeks of plan9 to
me.

In fairness to the Rust team, this isn't because they think this is a
particularly *good* way of doing things, or that they think asynchronous IO is
*bad*.  It's because when 1.0 was approaching, everything that wasn't stable
(or even implemented) that could be jettisoned had to be kicked into crates.
There's a time and place for such minimalism, and it's hard to say that
they're *wrong* in this decision; Rust needed to launch at some point, after
all.  But what went with this was the promise (well, two promises really) that
the contents of std would expand with each release (they have) and that crates
would fill this void.

So let's take a look at the crates.

There are 21 results on crates.io for "asynchronous IO".  They boil into NNN
groups: mio (and things based on it), gjio, nemo, and slog (which is a logging
system and we therefore ignore) along with other false hits.  You've seen me
do this before; let's walk through them.  In reverse order this time because
it reflects the complexity of what I have to say about them and if you think
I'm planning this post more than a sentence or two ahead... oh boy.

- "[Nemo](https://github.com/ebfull/nemo) is a Rust language session types
  library which focuses on asynchronous networking interfaces."  Ignoring that
  the use of session types is going to deter most users (I find it attractive,
  but I'm not most users), the problem here is that this is a library for
  writing protocols.  I'm trying to hand the data in my sockets off to
  something else to process, which is not an uncommon use.  Also their build
  is failing right now; I didn't know that button could even say that.

- [gjio2](https://github.com/dwrensha/gjio) is an event-loop based solution
  with the additional drawback that I've never heard of the event loop in
  question, though it promises to be built on `epoll(7)`.  Because it's locked
  to an event loop - and it doesn't matter which one - anything that decides
  to use this library is automatically incompatible with anything else that's
  used a different loop (a problem we've seen in other established languages,
  C and Python in particular by which I mean in my experience).  Honestly, for
  my purposes, if I wanted an event loop, I'd refuse to pick one and just bind
  [libverto](https://github.com/npmccallum/libverto).  But I don't want an
  event loop: I want a way to tell whether I can perform IO on my sockets or
  not.

- [mio](https://github.com/carllerche/mio) - maybe this is what you wanted.  I
  really don't know.  I'm led to believe that this is an extremely powerful
  library for IO management that will run Very Fast on whatever platform you
  want.  (Except Windows, which leaves me wondering why I'd use it over
  something in POSIX, like `select(2)` but we'll get back to that, don't
  worry.)  I should hope it's powerful, because using it is incredibly
  complicated, as evidenced by the complexity of
  [the basic tutorial](https://github.com/carllerche/mio/blob/getting-started/doc/getting-started.md).

I get that this is a project intended to be extremely powerful, and so
provides an absurd level of control to users, and there's definitely a place
for that.  But what we need is sensible defaults to keep the barrier between
me (or any other programmer) and understanding "hello world" (or it's
equivalent) with the library as small as reasonably possible, or barring that,
at least reasonable.

To drive this point further home: in another project of mine (currently tabled
for this reason), I needed some code to act based on input to a FIFO.  Why not
use Rust and mio?  Why not indeed.  Probably because the resulting file is 75
lines long just to support printing input from the FIFO and stdin to stdout,
is pretty close to mininal, only runs on unix-like platforms, and uses
`unsafe` twice.

### What about this new wheel-like device?

I could write my own here, it's true.  In writing this post, I've sketched out
most of what I'd want out of such a library (no event loop, libverto if you
must have an event loop, and reasonably-tuned defaults).  But this isn't an
unsolved problem; it's just an unsolved problem in Rust.

The original Rust issue contains this interesting tidbit: "`select` may not be
the right abstraction. Maybe there are more expressive ways to do this."  And
it's absolutely true: there are more expressive ways to do it, and it's
probably not the right abstraction (I have no particular love for the behavior
around FD_SETSIZE, for instance, and the usage of macros drives me absolutely
crazy), but it's *an* abstraction.  It's *something*, and for a language that
has recently released its twelth stable minor version to not have anything
here is distressing.  So today, trying to do anything in a pure-Rust fashion,
using the tools available to me, is gross, bad, or painful (pick at least
two).  I'd honestly be happier trying to do this in Haskell, a language whose
IO situation I regularly lambast.

But for Trapper?  I'm going to use the FFI to call `select`.
