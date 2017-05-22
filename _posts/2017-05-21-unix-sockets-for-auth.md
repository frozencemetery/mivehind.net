---
layout: post
tags:
  - tech
  - security
---

Let's not talk about the Pam/NSS stack and instead talk about a different
weird auth thing on Linux.

So sockets aren't just for communication over the network.  And by that I
don't mean that one can talk to local processes on the same machine by
connecting to localhost (which is correct, but goes over the "lo" network),
but rather something designed for this purpose only: Unix domain sockets.
Because they're restricted to local use only, their features can take
advantage of both ends being managed by the same kernel.

I'm not interested in performance effects (and I doubt there are any worth
writing home about), but rather what the security implications are.  So of
particular interest is `SO_PEERCRED`.  With the receiving end of an AF\_UNIX
stream socket, if you ask `getsockopt(2)` nicely, it will give you back
assurances about the connecting end of the socket in the form of a `struct
ucred`.  When `\_GNU\_SOURCE` is defined, this will contain pid, uid, and gid
of the process on the other end.

It's worth noting that these are set while in the syscall `connect(2)`.  Which
is to say that they can be changed by the process on the other end by things
like dropping privileges, for instance.  This isn't really a problem, though,
in that it can't be exploited to gain a higher level of access, since the
connector already has that access.

Anyway, the uid information is clearly useful; one can imagine filtering such
that a connection came from apache, for instance (or *not* from apache, for
that matter), or keeping per-user settings, or any number of things.  The gid
is less clearly useful, but I can immediately see uses in terms of policy
setting, perhaps.  But what about the pid?

Linux has a relative of plan9's procfs, which means there's a lot of
information presented in **/proc**.  (**/proc** can be locked down pretty hard
by admins, but let's assume it's not.)  proc(5) covers more of these than I
will, but there are some really neat ones.  Within **/proc/[pid]**, the
interesting ones for my purposes are:

- **cmdline** shows the process's `argv`.

- **cwd** shows the current working directory of the process.

- **environ** similarly shows the process's environment.

- **exe** is a symlink to the executable for the process.

- **root** is a symlink to the process's root directory, which means we can
  tell whether it's in a chroot.
  
So it seems like we could use this to implement filtering by the process being
run: for instance, we could do things only if the executable is
**/usr/bin/ssh**.  And indeed we can; **/proc/[pid]/exe** will be a symlink to
the ssh binary, and everything works out.

There's a slight snag, though: **/usr/bin/ssh** is a native executable (in
this case, an ELF file).  But we can also run non-native executables using the
shebang - e.g., `#!/bin/sh`, or `#!/usr/bin/python2`, and so on.  While this
is convenient for scripting, it makes the **/proc/[pid]/exe** value much less
useful, since it will just point at the interpreter.

The way the shebang is implemented causes the interpreter to be run with
`argv[1]` set to the input file.  So we can pull it out of
**/proc/[pid]/cmdline** and everything is fine, right?

Well, no.  Linux doesn't canonicalize the path to the script file, so unless
it was originally invoked using a non-relative path, we don't have that
information.

Maybe we can do the resolution ourselves, though.  We have the process
environment, so `$PATH`-based resolution should be doable, right?  And if it's
a relative path, we can use **/proc/[pid]/cwd**, right?

Nope.  Although inspecting the behavior of shells would suggest that
**/proc/[pid]/cwd** doesn't change, this is a shell implementation detail; the
program can just modify this value if it wants.

Even if we nix relative paths, we're still not out of the woods.
**/proc/[pid]/environ** looks like exactly what it want, as the man page
specifies that even `getenv(3)/setenv(3)` do not modify this.  However, the
next paragraph indicates the syscall needed to just move what region of memory
it points to, so we can't trust that value either.

There's actually a bigger problem, though.  Predictably, from the way the last
two went, processes can just modify `argv`.  So: native code only.

Anyway, thanks for reading this post about a piece of
[gssproxy](https://pagure.io/gssproxy)'s guts.  Surprise!
