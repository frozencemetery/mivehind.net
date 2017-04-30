---
layout: post
tags:
  - tech
---

Before one uses an item - be it a car, a piece of silicon, or even software -
it is desirable to have assurances as to its quality.  What assurances these
are can vary depending on the part and use, but they are all some degree of
"will this work as I expect it to when I use it".

Linux distributions (distros), roughly speaking, have two styles of release:
periodic stable (where there are formal releases of the distribution, like
Debian or RHEL/CentOS) and rolling release (where the package versions are
always updating, like Gentoo).  These stable-release distributions are always
frozen (in some fashion) from an associated rolling release, be it another
distro or a special branch for this purpose.  (So Debian freezes from its
unstable/testing branches, while Fedora freezes from its rawhide branch, which
is in turn approximately re-frozen to become RHEL/CentOS.)  Although these
associated rolling distros (sub-distros?) are usually intended primarily for
improving the quality of the main distros, they often become commonly-run in
their own right (Fedora, Debian testing).

Of course there are quality assurance efforts involved in the freezing
process, but I want to talk about the rolling efforts.  Ultimately, we'd like
some degree of assurance that package updates don't break (first) unrelated
components on the system, (second) other packages that depend on it, and
(third) expectations of direct users of the package.  For each of these, there
are automated tests that can be run (e.g., verifying dependencies, ABI
compatibility checks, regression suites, etc.), and it is also desirable to
have human verification as well.  So let's look at some!

I will explicitly ignore the following distros: RHEL/CentOS, because I can't
talk about it; Arch, because it's not documented anywhere; Gentoo, because the
documentation isn't clear (I think it's wholly discretion of maintainer?);
Ubuntu, because they do very little on top of Debian's branches; Mint, because
it is three (!) steps of snapshot-and-freeze from a rolling distro; and any
other distros I don't talk about due to marketshare.  This does mean I can't
talk about any purely rolling distros, which is unfortunate but so is their
documentation.

So first, let's look at a distro I don't use: openSUSE.  Their release process
is documented [here](https://en.opensuse.org/openSUSE:Release_process), and
I'm also pulling information from
[here](https://en.opensuse.org/Portal:Factory),
and [here](https://en.opensuse.org/Portal:Tumbleweed).  According to these
documents, package updates start in Factory, which is rolling.  As updates in
Factory pass QA, they are moved into Tumbleweed.  Tumbleweed is therefore also
rolling, but with additional stability testing.  Periodically, snapshots of
Tumbleweed are taken and become beta versions of the next stable release
(Leap).  I don't have information on the details of the migration process, and
as I have never used this distro, I cannot comment on its effectiveness.

Next, let's look at a distro that I contribute to and whose process I consider
"working": Debian.  The release process is documented
[here](https://wiki.debian.org/DebianUnstable),
[here](https://wiki.debian.org/DebianTesting),
[here](https://wiki.debian.org/DebianExperimental), and
[here](https://wiki.debian.org/DebianStable).  (Debian also has an LTS process
that I will ignore for this discussion.)  First, there is an optional
repository - Experimental - which maintainers can use for potentially buggy
updates that they do not wish to release to the general population.  Normally
though, package updates go into Unstable (permanently nicknamed "sid"), which
is rolling.  After an amount of time has passed (depending on the importance
of the update; usually two weeks) and no new bugs have been reported as
introduced by the update, it is automatically migrated into Testing.  Every
two years, Testing is frozen (i.e., no more automatic migrations from
Unstable) for about six months, and becomes the new Stable release.
(Whereupon migration into new Testing starts up again as normal.)  Since there
are users of both Testing and Unstable, this process functions well; Stable is
extremely stable (which is the primary goal of the project), and there is a
quality rolling release available in Testing (when not frozen).

And also, we have Fedora.  An example of the release cycle is
[here](https://fedoraproject.org/wiki/Releases/24/Schedule), and further
information is [here](https://fedoraproject.org/wiki/Releases/Rawhide) and
[here](https://fedoraproject.org/wiki/Bodhi).  Fedora has a pure rolling
branch called "rawhide" into which updates can be made at any time.  Every six
months or so, a snapshot of rawhide is taken and becomes the base for the next
numbered Fedora release.  Updates to non-rawhide branches can be made at any
time provided they pass Bodhi (Bodhi is enabled shortly before alpha).  Feodra
policy encourages maintainers to provide "latest stable" versions of software,
and so the releases tend to end up both with newer features and more bugs than
Debian's more conservative packaging policies.

Bodhi is really what I want to talk about in this post.  Bodhi aggregates
views into many metrics, but package migrations happen solely on two criteria:
number of upvotes (without too many downvotes), or elapsed time.  Notably
absent from migration are requirements such as: packages in newer branches
must have version (NVR) >= the same package in an older branch, package
dependencies must make sense, and package updates cannot introduce new bugs.
That's not to say these things aren't checked - they are or could easily be -
but they are not enforced.

Here are some other problems with this approach.  In theory, updates which
introduce bugs will be downvoted, but in practice they are not - if a bug
doesn't affect the user, they do not in practice downvote.  Downvotes on
updates are largely ignored by everyone involved.  Additionally, updates which
fix bugs are supposed to be verified as fixing the bugs in question - and
there's even a field for this - but it is not enforced.  Because tests are
conducted by people who have binned themselves as "testers", they happen most
on the newest branches of Fedora.  Which doesn't reflect either the importance
of the updates, or even where the users are, and results in non-latest branc
updates just always migrating due to time.  To counteract this, Fedora - as
part of the gamification efforts - has badges (think achievements) for testing
updates, as well as a weekly leaderboard.

Choosing my words carefully, this leaderboard has killed the usefulness of
Bodhi.  The top five people on the leaderboard (and it only shows top five)
have all submitted feedback on more than 1400 updates to the distro, across
all branches.  Looking somewhat arbitrarily at the person in the #3 spot,
they've submitted almost 2000 feedback this week.  If they spent 8 hours per
day for five days a week doing nothing but testing, this would be nearly 50
updates per hour - a bit slower than an update per minute.  If this were
mostly failures of some kind, I could understand that - maybe they have an
automated testing grid.  But they aren't, and they don't.  These five people
are the names I *always* see submitting karma to my updates, and it's *always*
positive.  The only times I've in fact seen them submit non-positive updates
were when dependencies were broken - which is automatically checked by Bodhi
already.  In the past three months of update submission (i.e. my last 12
submitted updates), I have received two useful pieces of feedback, and more
than a third of those updates did not receive the requisite positive karma
before time expired.

So much of what makes distros have a unique flavor is tied up in unwritten
policy, but it's important to look at the explicit policy as well, especially
for processes that happen at large scale such as update migrations.
Fundamentally, there are some things that need to be hard enforced by tooling,
if only so that maintainers (like me!) don't fat-finger and push the wrong
thing, since if there are enough of us, inevitably someone will.  And Bodhi
doesn't do that.  It places no virtually no requirements on the updates that I
(or any other maintainer) can push to the distribution, no checks for my
mistakes.  And make mistakes I have: forgetting to include patches for the
issues, most commonly, but I've also broken the dependencies of another
package, and Bodhi frequently causes newer versions to appear in older Fedora
branches if they get enough karma before the newer one does (though I maintain
this isn't a constraint that I should be responsible for at that point).

I believe that Fedora does fill an important ecological niche for Linux
distributions, and while I don't want it to become any other distro
necessarily, I do think we need to re-evaluate how we're doing quality
assurance.
