This first post will be a bit of a look into the technical side of how I set
all of this (my site) up.  Welcome to here; hopefully the content herein is at
least interesting if not useful.

### Backstory ###

I acquired the domain mivehind.net earlier this year.  The name was not born
of my imagination; rather, it comes from one of my friends.  With their
permission, I am using it as my own.

I purchased the domain through [Gandi SAS](https://www.gandi.net), a French
company that handles both domain registration and web hosting.  (A special
thanks to my bank for flagging this purchase and not my sudden purchases in
Las Vegas.  Way to go, guys.)  They are committed to privacy and open source,
both topics about which I care deeply.  Plus, it was cheap.

Paying other people to run computer systems has never been my thing, though.
Checking the IP mivehind.net resolves to will reveal that it is in the 128.237
block, denoting Carnegie Mellon University.  I'm currently an undergraduate
there, but more importantly the machine sits in a machine room that we, the
[Computer Club](https://www.club.cc.cmu.edu/services), run.  I'm using a
CMS that is still under heavy development, so having full access to my
machines is important.  More on that presently.

### Software Decisions ###

CClub is predominantly [Debian GNU/Linux](http://www.debian.org), which is
good because I like Debian.  We also use [Xen](http://www.xenproject.org) as
our hypervisor.  A brief comment about Xen: it and paravirtualization in
general are excellent and fast, but expect Xen to be the subject of future
less-than-happy posts on here.

Once I purchased a domain, though, I was slow to do anything with it.  Mostly
that's because I hate developing for the web; my ideal design is a terminal
with an emacs window open.  To be fair, though, I'm also fairly anti-the
modern web (there is another term for the modern web which I will not utter
here), in particular ECMAScript and Flash.  But then, I also use `ifconfig`
and System V init scripts, so maybe the same principle applies here.

Two things I do like, though, are [Haskell](http://www.haskell.org) and
version control.  As a result, I was pointed to [Gitit](http://gitit.net),
which is a wiki backed by DVCS (git, darcs, or mercurial, at the moment); it
also allows input in LaTeX, which is also something I like.  I haven't found a
use for a wiki yet, but I'm still looking.  Once I understood the concept, I
noticed that gitit uses the [Happstack](http://happstack.com) web framework.
And as one might expect, the 'H' on the beginning of that name does indeed
indicate that it's Haskell software; specifically, a web stack.  So suddenly
I'm interested in my website again.

As it happens, I'm not using Happstack directly, though I do rely on it.
Instead, I'm using [clckwrks](http://www.clckwrks.com), which is a Haskell CMS
that uses Happstack as a backend.  It lets me write pages in Markdown (okay,
it's not entirely Markdown, but I'll get to that momentarily), and handles
syntax highlighting and even allows for media management.  It's still in its
early stages, though; knowing Haskell is somewhat of a must for successful
deployment.

#### A Few Words about Markdown ####

One can read the full definition for Markdown on the very helpful Wikipedia
page, although Wikipedia currently notes that

    This article is written like a manual or guidebook. Please help rewrite this article from a descriptive, neutral point of view, and remove advice or instruction. (May 2010).

Thanks, Wikipedia.  In any case, I'd like to draw attention to the
[Code](https://en.wikipedia.org/wiki/Markdown#Code) and
[Blockquotes](https://en.wikipedia.org/wiki/Markdown#Blockquotes) section of
the language definition.  Clckwrks gets them backward; or rather, more
accurately, hscolour gets them backward, and at the moment hscolour is being
used for syntax highlighting.  Following discussion with the authors on
[#happs](irc://irc.freenode.net/#happs), I have learned that the developers
are aware of this problem (good), and plan to switch to pandoc soon (even
better).  I'm told there are other reasons as well, but this seems like a good
one to me, especially since prefixing code with '>' increases strongly the
difficulty of copy-pasting it.

### Creating the -stack ###

I'll assume as the base a fresh, minimal install of Debian Wheezy (the current
stable release).  A Wheezy install means ghcv7.4.1, which is new but not
bleeding edge.  These instructions are based off of those found
[on the clckwrks website](http://www.clckwrks.com/page/view-page-slug/3/get-started)
which are themselves quite good.

#### Talk to aptitude ####

From a fresh install, we first grab the things we absolutely need:

    # aptitude install cabal-install darcs make unzip markdown
    # aptitude install lib{crypto++,ssl}-dev # for HsOpenSSL
    # aptitude install happy # for haskell-src-exts
    # aptitude install libncurses{,w}5-dev # for terminfo

enable the extra functionality we'd like to have:

    # aptitude install libmagic-dev libgd2-xpm-dev libexpat1-dev # for media
    # aptitude install hscolour # for code markup; note the spelling

#### Talk about clckwrks ####

The first thing to do is get a fresh copy of the clckwrks source code.  The
developers have plans for the editing process to become more streamlined and
friendly to non-Haskellers, but for the moment there is only the bleeding
edge, so to speak.

    $ darcs get http://hub.darcs.net/stepcut/clckwrks

The instructions on the clckwrks website I linked above are quite good; I
followed them entirely for the remainder of the setup, and would recommend
that those reading this do the same.  

#### Talking about cabal ####

cabal is Haskell's package manager of sorts.  A more accurate description is
to say that it is a _build manager_, since it has no notion of **uninstall**.
Rather, uninstallation is accomplished through a combination of `ghc-pkg
unregister` and judicious use of `rm`.  I will ascribe it the adjective
"touchy", and say no more on that front.

#### On Darcs, Git, and Github ####

Most (sane) users don't have darcs installed.  In the version control world,
it looks like git has come out ahead.  There is a Github repository
clckwrks/clckwrks.git which purports to be the "Official mirror of clckwrks
darcs repo".  It may therefore be tempting to grab source from there instead
of from the darcs.  Unfortunately, while official it may be; up to date it is
not.  It was exactly a year behind on commits as of this writing.  I
determined this the hard way.  I'm told this is the fault of darcs-bridge.

I actually do prefer Darcs's model of the world (it tracks patches as its
basic object).  My first version control was Subversion, which I actually
liked (though I'm told this is because I never had to resolve any merges with
it or do serious branch management), and Mercurial felt to me like a natural
extension of Subversion into the DVCS world.  I found Git to be extremely
unintuitive when learning it, though I can understand the appeal of
sacrificing usability in order to gain speed.

### Results ###

The result of the above (and more web development than I would have liked
(ever seen
[this bug report](https://bugzilla.mozilla.org/show_bug.cgi?id=245633)?) is
this site.  It's not flashy, but then I didn't want flashy.  What few design
decisions I have made were optimized for my own ease of use, and I appreciate
feedback on both them and the content herein.
