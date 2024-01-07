---
layout: post
tags:
    - tech
    - security
---

Unfortunate scheduling means that LineageOS users are exposed to publicly
disclosed vulnerabilities for typically nine days per month.  Here's why, and
what I (a user who is otherwise uninvolved in the project) think could be done
to improve the situation.

Per [official Android
documentation](https://source.android.com/docs/security/bulletin/asb-overview):

> **Important**: The Android Security Bulletins are published on the first
> Monday of each month unless that Monday falls on a holiday. If the first
> Monday of the month is a holiday the bulletins will be published on the
> following work day.

Holiday time off makes sense for human reasons, though it makes release days
inconsistent.  (And I assume we're talking US holidays because Google, though
this isn't stated.)  Adherence to this isn't great - most egregiously,
something happened that resulted in a March 13, 2023 release which is probably
the largest slip since August 13, 2015 (which is far back as the table goes).
But I've worked in security engineering long enough to know that sometimes
dates will slip, and I'm sure it's not intentional.  Clerical errors like the
November 2023 bulletin date are also inevitable.

But let's assume for the sake of simplicity that disclosure happens as
written: on the first Monday of the month (or the following day) a bulletin is
published listing the CVEs included, their type/severity, and which Android
(i.e., AOSP) versions are affected.  Importantly absent here are the patches
for these vulnerabilities, which per the bulletin boilerplate take 2 days to
appear.  So what's the point of the bulletin?

In any case, this means that patches won't be available until Wednesday or
Thursday.  Lineage posts updates on Friday; per datestamps, these updates are
built on Thursdays.  This means that in order to have the security fixes (and
security string) in the next Lineage update, there is less than a day's window
to gather patches, backport them, post pull requests, run CI, get code review,
etc., before the weekly build is made - a seemingly herculean feat.  And
sometime months, it won't be technically possible at all.

So since patches will not land in the next release, all users of official
builds are exposed to publicly disclosed vulnerabilities for typically nine
days.  (I think it's 8-10, but I don't discount off-by-one, and that also
relies on Lineage not slipping further; everyone's human and it does happen,
especially on volunteer projects.)

Clearly, the schedule is a problem.  Here are my initial thoughts on how this
might be addressed:

1. **Release Lineage updates on a different day.**  If it takes four days to
   run through the backport+review+build pipelines, then plan to release on
   Monday.  Users will still be exposed for the length of time it takes to
   backport+review+build.
2. **Add Lineage to the embargo list.**  This would mean that backport and
   review could take place prior to public disclosure, and so including the
   security fixes in the upcoming Friday update becomes doable.  Users are
   still exposed for 2 days, but that's way better than 9.  (I am not involved
   in the Lineage project so it's possible they already are included, but that
   seems unlikely given security update PRs are not usually sent on the day
   code becomes publicly available.)
3. **Stop the bulletin/patch desync.** I cannot come up with a good reason why
   the security bulletin and patches are released at different times, let
   alone releasing the bulletin before the patches.  This makes reasoning
   about fix availability unnecessarily complicated.  However, it would
   probably require Google to care.
4. **Update Lineage less frequently.**  It seems like the least amount of
   work, but if, e.g., Lineage released once per month, then the day of the
   release could be whenever the security fixes for the month land.  This is
   also helpful beccause it minimizes the number of times that flashing needs
   to occur.  (But that may be a larger discussion for a different post.)
   
These are not mutually exclusive, either.

To close out, I need to head off something that I am quite sure will come up.
Yes, I am capable of running my own custom Android builds and kernel trees.  I
do not want to do this, and more importantly, users who are not developers by
definition cannot do it.  That is to say: OTA updates and official builds are
the most important versions of the project, not whatever custom stuff we make.
(After all, if that weren't the case, there wouldn't be [five major
forks](https://en.wikipedia.org/wiki/LineageOS#Forks) over [the signature
spoofing
decision](https://review.lineageos.org/c/LineageOS/android_frameworks_base/+/195284).)
