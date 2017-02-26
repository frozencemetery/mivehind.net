---
layout: post
---

Last week, by chance, I wrote the
[Git tutorial I'd been threatening friends with](/2017/02/19/an-intro-to-git/).
And I say by chance, of course, because this week the ability to generate
SHA-1 collisions was all but dropped on the world.

Which, let's be clear, is horrible news for everyone who now has to move their
software off of SHA-1.  But this work isn't entirely new: for the most part,
it's a practicalization of work published in 2015.  Which follows on the heels
of a string of weakings dating all the way back into early 2005 (or even
earlier, depending on what you're willing to count).  During which time there
has been growing concern from the security-minded about software that used
SHA-1, and even more importantly, serious efforts from industry leaders to
futureproof their code.

It's a shame that Git, released in mid-2005, didn't heed the warnings.
[From John Gilmore](http://www.metzdowd.com/pipermail/cryptography/2017-February/031623.html),
no less.  But that was my main point in the previous post: Linus - and Git -
[abhor abstraction (and politeness)](https://wayback.archive.org/web/20160206023141/http://article.gmane.org/gmane.comp.version-control.git/57918)
in any form.  And it is to their detriment.

## Problem?

So in practical terms, to you and me (both relatively normal Git users), what
does the ability to generate SHA-1 collisions mean?

To be fair,
[Linus did think about this](https://marc.info/?l=git&m=115678778717621&w=2).
And he's right, as far as I know: Git prefers the local version of a hash, so
there is no danger of a remote overwriting it.  But the problem space is
bigger than that, and therefore not a "non-issue" (as he put it).

The important discussion is this: what if the collided hash *isn't* in the
local repository already?

Of course, there are many hashes (most, even) which are not in any given local
repository.  We, as hypothetical attackers, need concern ourselves with
predicting a hash that the user will download (which they do not already have)
that we can substitute a malicious collision for.  We also need to do this in
such a way that the user will not notice: pulling a commit or branch for
purposes of code review will not be sufficient, for instance.

I think the easiest way to ensnare users is to catch emergency re-clones, and
similar operations ([toot toot](/2017/02/19/an-intro-to-git/)), during which
the user places more trust than they ought in the server.  If everything looks
right on the surface, and the old repository is in a semi-destroyed state, are
we really going to review the immense amount of code looking for problems?  In
a project the size of this blog: maybe.  Certainly not for the larger
projects.

And of course there are a few clever offshoots of this idea that could be
exploited (how many people do you think *really* check that the code they
reviewed in the web tool matches the contents of the commit they just
merged?), but that interests me less than this attack I thought up this
morning.

In last week's post, I mentioned release branches.  These are an model I work
with a great deal, both as a contributor to established upstream projects and
as a maintainer for distributions.  A release branch, of course, mostly
consists of commits which are the result of `cherry-pick`ing the development
branch.  And in that post, I suggested further the use of a flag - `-x` -
which embeds the hash of the original commit in the release branch's version
(in the commit messsage, specifically).

Having the "original" commit hash easily accessible from the release branch is
advantageous because we are working around a design decision in Git: that
the uniqueness of commits takes into account their parents.  More
specifically, two commits which make the exact same changes to the exact same
files but with different parents are, for purposes of Git, considered
different commits.  They will have different SHA-1 hashes.

This design decision becomes a design failure when we want to make release
branches (which the kernel itself does...) and need to backport (i.e.,
duplicate changing only the parent) commits from stable branches.  So to paper
around the issue, we use `-x`, and then we can then (by hand!)  extract the
original commit hash from the backport's message.  It's worth noting that in
"patch-based" systems (Darcs, Pijul, and friends), the original commit and the
backport are the **same commit**, just applied on different branches.  They do
not suffer from this problem.

As each commit contains parent information, Git can normally be quite good at
leaving no references unresolved by just downloading all the hashes that are
referred to.  But the `cherry-pick` hashes are not references that are visible
to Git, and even if we added logic to try to detect them, it would never be
good enough.  Git also has the misfeature of allowing unique substrings of
hashes at any point where full hashes could be used, which, in hindsight,
seems designed to enable collision (and is a decision that GPG also made for
fingerprints, where it is a [problem today](https://evil32.com/)).

All that remains at that point is for an unsuspecting user to have a release
branch checked out without a full copy of the master branch.  Which is
surprisingly likely for a distro packager (speaking from experience), or for
new users who don't really need years of development and so made a shallow
clone (`git clone --depth 1` or so) in order to save time/bandwidth.

This practice of embedding SHA-1 hashes in commits is also why I predict that
migrating Git off of SHA-1, if it even happens, will require an effort on the
scale of migrating off of SVN (which still hasn't happened for many modern
projects!).

## Final thoughts

I would love it if the ideas we abandoned in the quest for speed *uber alles*
would return.  I see projects like [Pijul](https://pijul.org/), improving on
Darcs, written in [a modern language](http://rust-lang.org/), and boasting
performance better than Git, and it gives me hope.  BitKeeper has an open
source license now, so perhaps we will think about weave merge once again.  It
doesn't feel like too much of stretch to imagine a resurrected Monotone
pushing the importance of integrity (cryptographic or otherwise) and
abstraction, or perhaps
[large](https://hg.mozilla.org/mozilla-central/shortlog) corporate
[players](https://code.facebook.com/posts/218678814984400/scaling-mercurial-at-facebook/?_fb_noscript=1)
will continue to forcibly drag Mercurial along with them.  Or maybe a new
tool that hasn't yet seen attention will steal the show.

Just please, not Git.  Not again.  Not still.  No more.
