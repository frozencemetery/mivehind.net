---
layout: post
tags:
  - tech
---

Given my interest in version control, a post on Pijul was pretty much
inevitable.  The thing I most wanted to understand was of course its conflict
resolution algorithm.  Unfortunately I don't know enough category theory
[for that](https://arxiv.org/abs/1311.3903), which is a novel problem to have
at least.  There also don't seem to exist explanations of how this algorithm
works that don't rely on category theory, which is unfortunate.  The
documentation that exists for this tool is generally sparse, which is fine;
it's new software, after all, and these are alpha releases.

Fortunately, according to their [blog](https://pijul.org/blog.html), there's
been a useful version released recently.  So what follows are my thoughts on
playing with that version (0.4.1).

First important thing is that the Pijul repository is itself kept in pijul.
There's a GitHub repository that has all the trappings of being an official
mirror, but it looks to have stopped working when they switched the pijul
repository off of darcs.  To resolve the bootstrapping problem, I installed it
with `cargo` instead, which took a short seven minutes to download and compile
everything and dependencies. (Peeking behind my curtain slightly, I tried to
write this post both Friday and yesterday, but was unable to do so because
their hosting (Nest) was down.)

The next logical thing to do, once the tool is installed, is to clone a
repository and play with it.  I chose the pijul repository itself on the
theory that it would be fairly sizeable and that I wanted to browse it anyway.
Unfortunately, they seem to reset their history; there are only about nine
commits lying around, one of which seems to be a squashed "reboot" commit.
(This is apparently due to some one-time changes to the internal store that
coincided with the 0.4 release.)

Several commands share a name with verbs from Git - `add`, `clone`, `init`,
`pull`, `push`, `status` - and all seem to present a similar interface (though
of course less cluttered).  I recognize a few verbs from Darcs as well -
`record`, `revert`, `unrecord`, and maybe some others.  There's in-repo
branching already, which gives it a leg up on Darcs and Bazaar, neither of
which ever got that far.  And many other things, as one would expect.  I think
the most interesting part is that they almost-accidentally baked in a Pull
Request model: you just push to a remote, and it makes a listing of patches
that can be pulled in later.  I think it's a neat approach, at least, and it
seems to integrate well with Nest (their web interface).

### merges?

Yeah okay let's talk about this.  The way a repository is presented doesn't
have a notion of history in the traditional sense.  Instead, dependencies
between patches are tracked, and then each branch has a notion of what patches
it contains.  So when I `pijul record` a new commit, the location it shows up
in `pijul changes` is undexpected - often not near the top or the bottom of
the list.  (I also wish there were more whitespace in its output, but
details.)

Now, because their internal patch format is not the traditional Diff-style,
there doesn't seem to be an easy way to figure out what changed in a given
patch (yes, this nomenclature is confusing; I'll try to use "Diff" for the
expected thing, and "patch" for Pijul's base object).  I can output patch
objects, which is kind of cool, but I don't see a way to turn these into
something I can look at.  `pijul status` also reflects this: it shows the
changes currently not associated with a patch, but not in a Diff format.

Anyway, I don't totally have a feel for this interface, so everything comes
off a bit clunky, but I did manage to play with making some of my own
patches.  An important thing is that I don't understand the failure mode for
its conflict resolution - I applied two explicitly conflicting patches to see
what it would do, and it gave me a file that looked like this

```
prelude
line from patch I applied first
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
line from patch I applied second
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
rest of file
```

which is of course familiar from git-land, but there's no *indication* that it
did this - nothing in `pijul status` or anywhere else I can find.  I assume
then that Pijul is both aware of the conflict and able to detect this in
files, but I do wonder what would happen if I needed to put a bunch of ">" and
"<" in a file like that.

Beyond that: merging seems good, it's fast, and it seems to be able to handle
[badmerge](https://tahoe-lafs.org/~zooko/badmerge/simple.html) correctly.

I'm excited to see what happens in the future, but this doesn't really merit
the "usable" label its authors applied.  This is general problem I'm finding
with Rust and the Rust ecosystem, though: many projects technically *work*,
but aren't polished or really done to the point where one wants to use them.
For this one in particular, no one else seems to know how to use it either
(searching for Pijul tutorials got me nowhere, but it did get me a surprising
number of articles hyping it as a git-killer without explaining it very much).
