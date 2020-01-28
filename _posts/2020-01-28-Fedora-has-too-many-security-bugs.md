---
layout: post
tags:
  - tech
  - security
---

I don't work on Fedora security directly, but I do maintain some crypto
components.  As such, I have my own opinions about how things *ought* to work,
which I will refrain from here.  My intent is to demonstrate the problem so
that the project can discuss solutions.

To keep this easy to follow, my data and process is in a section at the end;
curious readers should be able to double-check me.

# Problem

At the time of writing, there are 2,336 open CVE bugs against Fedora.  While
it's not realistic for that number to be 0, this is clearly way too many.

Additionally, a majority of them (2309) are older than 4 weeks.  I understand
from experience that even the most important bugs are rarely fixed
instantaneously, but having bugs that old (and so many) speaks to deeper
problems with the way maintenance is done right now.  In fact, here's the year
breakdown:

    2010: 4
    2011: 11
    2012: 17
    2013: 18
    2014: 30
    2015: 74
    2016: 195
    2017: 425
    2018: 682
    2019: 852
    2020: 27

So a concentration in the past couple years, but with a very long tail.

My query includes both "regular" Fedora and EPEL.  There are 1266 EPEL bugs in
this set (which leaves 1070 non-EPEL).  So the problem is worse for EPEL, but
EPEL is by no means responsible for this huge number.

It's possible to slice this by component, but I don't actually want to do that
here because my intent is not to point fingers at specific people.  However,
there are a few ecosystems that seem to be having particular trouble (based on
visual inspection of names):

    mingw: 459
    python: 81
    nodejs: 72
    ruby: 32
    php: 23

(The remainder don't clearly group.)

That's all the analysis I could think of to run, but see the methodology
section below if you want to build on what's here.

# Fedora policies

A majority of CVE bugs are created by Red Hat's Product Security (of which
team I am not a member; I'm in Security Engineering).  They provide this
service on a best-effort basis.  As I understand it, the theory is that
maintainers should be aware enough of their packages to know whether a release
fixes a security bug or not.  (And also that an extra bug for us to close
once in a while isn't the end of the world.)

Fedora has some policy around security bugs in the [Package maintainer
responsibilities](https://docs.fedoraproject.org/en-US/fesco/Package_maintainer_responsibilities/)
document, but it's very weak (to someone coming from [RFC
2119](https://tools.ietf.org/html/rfc2119)-land, at any rate).  It says:

> Package maintainer should handle security issues quickly, and if they need
> help they should contact the Security Response Team.
  
("Security Response Team" is a broken link, which I've reported
[here](https://pagure.io/fesco/fesco-docs/issue/25).)

This effectively treats security bugs no differently than other bugs.  The
only recourse for maintainers not fixing bugs in general is the [nonresponsive
maintainer
process](https://docs.fedoraproject.org/en-US/fesco/Policy_for_nonresponsive_package_maintainers/),
which won't help if the maintainer is still active in the process but hostile
toward fixing/triaging their bugs.

So it has to go to FESCo.  FESCo presumably does not want to handle the
hundreds of tickets for all of these, which means that the status quo is
inadequate.

In short: no one is minding the store, and more worryingly, there is no way
for anyone to *start* minding the store.

# What I've done

I've reached out to some maintainers, including folks from mingw.  I currently
have a FESCo ticket ([#2333](https://pagure.io/fesco/issue/2333)) for getting
those resolved.

Reaching out to EPEL maintainers has proven unsuccessful on the whole.  From
my scattered sampling, these bugs aren't getting fixed because the default
package assignee is not interested in maintaining EPEL.  (Presumably someone
else did in the past, and they have vanished.)

I've also written this post, which I hope will spark a concerted effort to fix
the problem.

# Methodology

All information in this post is readily accessible to any Fedora contributor,
no special access required.

I used
[this bugzilla
query](https://bugzilla.redhat.com/buglist.cgi?bug_status=__open__&classification=Fedora&limit=0&list_id=10800885&order=priority%2Cbug_severity&query_format=advanced&short_desc=CVE-&short_desc_type=allwordssubstr).
I downloaded the data as CSV, then queried and filtered it using python.  I'm
sure there are better ways to do this, but I'm not a statistician.  I also
mostly write C.

Once I had downloaded the CSV, I imported it like so:

```python
import csv

with open("bugs-2020-01-28.csv", "r") as f:
    db = list(db.DictReader(f))
```

The csv module's interface is obnoxious.  It wants to give back an iterator
over the file, so we have to drain the iterator before the file can be closed.
(Otherwise it becomes unhappy.)  This leaves us with an object of type roughly
`List<OrderedDict<String, String>>`.  Really what I'd like is
`Set<Dict<String, String>>`, but neither `Dict` nor `OrderedDict` are
hashable, so Python doesn't allow that.

For determining age, I'm abusing the fact that it's January 2020 right now:

```python
old = [bug for bug in db if "CVE-2020" not in bug["Summary"]]
```

Mapping years:

```python
import re

from collections import defaultdict

years = defaultdict(int)
r = re.compile(r"CVE-(\d{4})-")
for bug in db:
    match = r.search(bug["Summary"])
    if match is None:
        continue
    
    year = match.group(1)
    years[year] += 1

for key in sorted(years.keys()):
    print(f"{key}: {years[key]}
```

EPEL:

```python
epel = [bug for bug in db if bug["Product"] == "Fedora EPEL"]
```

Components:

```python
components = defaultdict(int)
for bug in db:
    components[bug["Component"]] += 1

for c in sorted(components.keys()):
    print(f"{c}: {components[c]}")

def ecosystem(e):
    count = 0
    for c in components:
        if c.startswith(f"{e}-"):
            count += components[c]
    
    return count
```
