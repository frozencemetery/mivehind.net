---
layout: post
tags:
  - tech
  - security
---

A year (and change) later, this is a followup to my previous post on how
[Feodra has too many security
bugs](/2020/01/28/Fedora-has-too-many-security-bugs/).  The code and
methodology I'm using are unchanged from that post - this is just new numbers
and some thoughts on the delta.

Right now, there are 2,089 open CVE bugs against Fedora.  This is a decrease
of 247 from last year - so that's good news.  My gratitude toward maintainers
who have been reducing their backlog.

Year breakdown:

    2009: 1
    2010: 0
    2011: 2
    2012: 9
    2013: 5
    2014: 5
    2015: 17
    2016: 72
    2017: 242
    2018: 367
    2019: 260
    2020: 701
    2021: 408

With the exception of the 2009 bug (opened on 2021-03-27), the tail shrunk by
one year.  The per-year deltas are:

    2009: +1
    2010: -4
    2011: -9
    2012: -8
    2013: -13
    2014: -25
    2015: -57
    2016: -123
    2017: -183
    2018: -315
    2019: -485
    2020: +674
    2021: N/A

(The 2020 change is of course expected, since 2020 mostly hadn't happened yet
at the time the last post was written, and there's often lag between number
assignment and disclosure of CVEs.)

The EPEL/non distribution no longer skews toward EPEL: now there are 958 EPEL
bugs, compared to 1131 non-EPEL.  However, given the relative size of the two
package sets, this is still a surprisingly high number of EPEL issues.  The
deltas are EPEL: -308, non-EPEL: +61.

For ecosystems, right now I see:

    mingw: 140 (-319)
    python: 109 (+28)
    nodejs: 99 (+27)
    rubygem: 27 (-5)
    php: 19 (-4)
    
An interesting datum here is that mingw's reduction is more than the total
Fedora reduction.  In other words, if mingw had been CVE-neutral, Fedora would
have increased total count by 72.  So in a sense, mingw improved, while the
rest of Fedora became worse.

Finally, while the documentation links have been fixed, there has been no
change to Fedora policy around security handling, nor is there a functioning
Security Team right now.  Making a Security Team happen would be a Herculean
task, so I have nothing but appreciation for the folks who have worked on it.
However, it does suggest that our incentive structure is wrong.
