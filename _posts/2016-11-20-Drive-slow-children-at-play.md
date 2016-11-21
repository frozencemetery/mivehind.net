---
layout: post
---

The first side of this issue is compilers.  Modern compilers are of course
expected to turn our programming languages into executables, but they are also
supposed to do so in an efficient way.  This requires them to understand how
larger pieces of the program fit together (not just single statements).  In
the quest to create maximally efficient code (gotta go fast), optimizations
have over time required increasingly complicated conditions for application,
as one would expect.

Any code will encounter some bugs, and I do not want to fault compiler authors
for trying to go fast.  For how complicated Clang/LLVM and GCC and so on are,
there are few bugs, which is nice.  (Most of this is due to regression testing
and only counting bugs in released versions, but whatever gets them there is
good.)  I do, however, want to question *ever* optimizing away calls to
`memset()`, `bzero()`, and the like.  There are two reasons I think it is
always wrong.

The first reason is that compilers get it wrong.  More than zero times, which
is the exact number of times it is okay to get this wrong.  I will prove this
to you right now by linking
[a GCC bug](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78408) about getting
it wrong.

The second is that it is too important to get wrong.  This is because of
cryptography.  More accurately, it is due to the need to ensure, without any
doubt whatsoever, that a chunk of memory has been set to zero at a given time
so that they can not only hold key material but also guarantee that it has
been disposed of and therefore not leak out to actors that should not have it.

### An Example

To look at a codebase I can confidently explain,
[this](https://github.com/krb5/krb5/blob/c163275f899b201dc2807b3ff2949d5e2ee7d838/src/include/k5-int.h#L640-L683)
(with help from another file) is how krb5 does it in master.  For reference,
this is an incredibly reasonable way to handle it: there's a Windows function
guaranteed to solve this problem, with fallback to a C11 function guaranteed
to solve the problem.  These are fine and dandy, and if this were all it took
I probably would not have anything to complain about this week.

The problem is that the two other cases are not only needed (because not
everyone is C11) but also disgusting: in the first, language assembly is used,
and then as a
[final fallback](https://github.com/krb5/krb5/blob/c163275f899b201dc2807b3ff2949d5e2ee7d838/src/util/support/zap.c)
there's a cast to volatile with manual scrub.  Altogether, there are an absurd
number of cases: in an ideal world, we would have one case (the C standard
builtin function) and in a realistic world two cases (the Windows one and the
one for the rest of the world), but we need four.

It is important to note that a bug in any of these functions or the way they
are compiled is a potential cryptographic key disclosure.

### OpenSSL

I feel that no article that mentions cryptography can be complete without
taking potshots (friendly or unfriendly) at OpenSSL.  I promise I tried to do
this in good faith, though that was because I had not actually seen this code
before sitting down to right.

Feast your eyes, if you would, on the delta that is
[pull 455](https://github.com/openssl/openssl/pull/455/files).

On the right hand (or additions, if you do not use split diff on Github for
some reason) we have a function `OPENSSL_cleanse()` that looks a lot like
krb5's `zap()` - try the C11 function, try the Windows function, fall back to
mucking around with volatile pointers.  It is different chicanery than what
krb5 does, and I am not familiar enough with the standard to say whether it is
good or not, but that academic anyway as this pull request did not merge.
More on that in a moment.

On the left hand side (i.e., existing code), we have the kind of thing that
drives programmers to go raise sheep.  At first glance it appears to be
assembly, segregated by architecture.  This is not great.  What is even worse
is that it is in fact, on closer inspection, a pile of Perl that generates
architecture-specific assembly.  It also does not work according to its
specification.

Fortunately, I did not determine this by reading the code myself.  It is
mentioned as part of
[the corresponding PR](https://github.com/openssl/openssl/pull/455), which I
will suggest that you do while refraining from comment.  The result of those
conversations, confusingly enough, is
[this change](https://github.com/openssl/openssl/commit/104ce8a9f02d250dd43c255eb7b8747e81b29422),
which reflects the code as it stands today.  Please note that all of the
assembly is still present.  I will not comment further on this code.

Next week I will try to post something happier, with lots of slide whistles.
