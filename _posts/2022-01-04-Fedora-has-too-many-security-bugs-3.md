---
layout: post
tags:
  - tech
  - security
---

(Previously [part 2](/2021/05/10/Fedora-has-too-many-security-bugs-2) and
[part 1](/2020/01/28/Fedora-has-too-many-security-bugs/).

Right now, there are 1917 open CVE bugs against Fedora.  This is a decrease
of 172 from last year - so again, we report good news.  Gratitude toward
maintainers who have been reducing their backlog.

Year breakdown:

    2005: 1
    2011: 1
    2012: 4
    2013: 4
    2014: 5
    2015: 17
    2016: 71
    2017: 227
    2018: 341
    2019: 225
    2020: 311
    2021: 710

While the bug that was last year's tail (a 2009 bug) has disappeared, the tail
is now much longer with the addition of the 2005 bug.  The per-year deltas
are:

    2005: +1
	2006: N/A
	2007: N/A
	2008: N/A
	2009: -1
	2010: N/A
	2011: -1
	2012: -5
	2013: -1
	2014: ±0
	2015: ±0
	2016: -1
	2017: -25
	2018: -26
	2019: -35
	2020: -390
	2021: +302
	
(N/A is reported where neither last year's run nor this year's run had bugs in
that year bucket, while ±0 indicates no change in the number year to year.
The 2021 change is somewhat expected since there's a lag between CVEs being
assigned numbers and being disclosed.)

Unfortunately, the balance has shifted back toward EPEL: EPEL has 1035 of the
1917 total, a change of +77.  This has outsized impact because EPEL is much
smaller than non-EPEL Fedora.

For ecosystems, the largest ones I see are:

	mingw: 99 (-41)
	python: 95 (-14)
	nodejs: 85 (-14)
	rubygem: 20 (-7)
	php: 13 (-6)

and it's nice to see a reduction on all of them.

Finally, to close as before, there have been no changes to Fedora policy
around security handling, nor is there a functioning Security Team at this
time.  Obviously no one should be forced into that role, but if anyone wants a
pet project: the incentive structure here is still wrong.

For completeness, since bugzilla has changed a bit, here's my script operating
on the CSV file:

```python
#!/usr/bin/python3

import csv
import re

from collections import defaultdict

with open("Bug List 2.csv", "r") as f:
    db = list(csv.DictReader(f))

print(f"total bugs: {len(db)}")

years = defaultdict(int)
r = re.compile(r"CVE-(\d{4})-")
for bug in db:
    match = r.search(bug["Summary  "])
    if match is None:
        continue
    year = match.group(1)
    years[year] += 1

for key in sorted(years.keys()):
    print(f"    {key}: {years[key]}")

epel = [bug for bug in db if bug["Product  "] == "Fedora EPEL"]

print(f"epel #: {len(epel)}")

components = defaultdict(int)
for bug in db:
    components[bug["Component  "]] += 1

# This spews - but uncomment to identify groups visually
# for c in sorted(components.keys()):
#     print(f"{c}: {components[c]}")

def ecosystem(e: str) -> int:
    count = 0
    for c in components:
        if c.startswith(f"{e}-"):
            count += components[c]
    return count

print(f"mingw ecosystem: {ecosystem('mingw')}")
print(f"python ecosystem: {ecosystem('python')}")
print(f"nodejs ecosystem: {ecosystem('nodejs')}")
print(f"rubygem ecosystem: {ecosystem('rubygem')}")
print(f"php ecosystem: {ecosystem('php')}")
```
