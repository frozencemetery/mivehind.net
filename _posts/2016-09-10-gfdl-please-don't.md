---
layout: post
---

It took every bit of my restraint to not call this "GFDL: Considered Harmful".

Or "GFDL: Not Even Once".

(Is it really better if I put them up here?)

## Please Don't

This topic came up in two different conversations this week, and I was unable
to find any cohesive writeups.  Hopefully that's fixed now.

### What is the GFDL?

The GFDL (GNU Free Documentation License) is very similar to a software
license (like the GPL) except intended for software documentation
specifically.  You can read the full text of it on
[GNU's website](https://www.gnu.org/licenses/fdl.html), but I really don't
recommend doing that.

At a high level, the GFDL is similar to the GPL.  Both require modifications
to be under the same license, both require preservation of authorship, and
both manage intellectual property.  There are some important differences
though: the GFDL requires retitling of derivative works (similar to the LaTeX
license, the LPPL), and the GFDL has additional provision for "Invariant
Sections" of the doocument, which cannot be modified in derivative works.

### Why is the GFDL?

This is a really good question.  As far as I can tell, when GNU was preparing
to release GNU software documentation, a decision was made that documentation
is not code and therefore needs to be licensed separately.

This distinction may seem odd: after all, many projects treat their
documentation as code and just use the same license for both, which ends up
being particularly convenient for distribution.  Today, the distinction
between code and documentation is particularly blurry because a lot of
documentation is in the code itself (doxygen and other such systems, for
instance) but also because of the prevalence of markup languages (like ReST
and Markdown) that are arguably code themselves.  While there were certainly
fewer markup languages in the day, troff (man pages) and GNU's beloved texinfo
(info pages) were definitely in use for documentation.

Really, it seems to be intended for manuals, though it's of course been
applied many places elsewhere.

### What uses the GFDL?

It's one of the FSF's recommended licenses, so of course there are GNU
projects that use it (GCC, emacs, etc.) for their documentation.  Many
websites with user-generated content use it for licensing this content
(Wikipedia most notably, but also sites like last.fm).  Increasingly, sites
that have used the GFDL exclusively are moving to dual-licensing with Creative
Commons (CC-BY-SA, or attribution share-alike) which notably does not permit
invariant sections or require re-titling of works.

### Problem?

There are basically two problems I have with this license.

The first is that it means that code and its documentation are under different
licenses.  As mentioned earlier, this can be difficult to work with because
the distinction is often quite blurry between code and its documentation.  It
complicates distribution, because now the case can occur where the
documentation license is considered favorable but the code is not, or vice
versa.  It just contributes to complicating the licensing choice: now it's one
more license to evaluate, and to determine compatibility with all other
licenses.

The second problem I have is with invariant sections.  The FSF doesn't really
explain what these are intended *for*; their
[tips on using the GFDL page](https://www.gnu.org/licenses/fdl-howto.html)
very helpfully says to use invariant sections "If a section's contents ought to
be invariant".  So okay, what does GNU do with them?

They tack on the GNU manifesto.

They made a license just so that you couldn't remove the GNU manifesto from
their projects.

One might think that having the text of the GPL (or whatever other relevant
license) would be enough.  Apparently it's not.

These two problems collide perfectly in the Linux distribution world.  Of
course the GPL is acceptable in such cases (it is the license Linux is using,
after all), but what if the GFDL isn't?  Then we get the case where tools can
be packaged, but their documentation isn't.  And this is exactly what has
occurred: often gcc, emacs, bison, and everything else from GNU will be easily
installable, but the documentation is just... not.  As a result many people
have never read, for instance, the gcc man page.  (Not that it's particularly
great, but it's been a problem on multiple occasions.)

#### Invariant sections revisited

Alright, but what if we used the GFDL without any invariant sections?
Ignoring that there are better licenses for this purpose (Creative Commons, or
even better whatever license your code is under), this is a grey area.  Some
don't like the ability to add in invariant sections in derivative works, and
honestly I don't understand how that would work either.  (Your original text
has no invariant sections; fork A adds such a section and some non-invariant
changes; can fork B take only the non-invariant changes from A if it considers
itself a fork of my original text?  I would be willing to believe that has an
answer, but it is decidedly non-obvious.)

[Debian's current stance](https://www.debian.org/vote/2006/vote_001#outcome)
is that GFDL works can be included in the distribution proper (i.e., the main
archive) as long as they do not include invariant sections.  But it's a shaky
stance: the decision was far from unilateral, though most people seemed to
agree that GFDL works will never be fully DFSG-compatible (i.e., licenses that
Debian likes as sharing similar goals to the Debian project).

#### But your blog...

Yeah, my blog uses two licenses.  Some people have (angrily) complained to me
about this in the past, though this is more to do with *which* Creative
Commons license I chose rather than that I use two.  But in essence, I
consider my code and anything that documents what it does and how it does that
to be one unit, and my general essays, musings, and so forth to be an easily
separable unit.  To put this perhaps more clearly: no one will ever (usefully)
make an installable software package that is one of my blog posts, since
they're mostly me talking about ideas.
