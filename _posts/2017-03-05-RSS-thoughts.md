---
layout: post
tags:
  - tech
  - meta
---

First, there have been a few layout changes to the site.  Hopefully they will
improve usage on mobile (at least, that was the goal).  I'm tired of thinking
about styling, which suggests that I probably have too much and need to start
over.

Second, I encountered what I believe to be my first RSS feed behind Cloudflare
this week.  Since I pull RSS over Tor, Cloudflare decided that I must be evil,
and served me a CAPTCHA.  How is one going to maliciously abuse a static page?
And, more importantly, how is an RSS feeder (especially one that runs on the
command line like mine does) supposed to handle feeding the user a CAPTCHA?

Next, each post on this blog (yes, including this one) has been retrofitted
with tags.  This turned out to be the easiest way to generate filtered streams
to dump into blog aggregators.  (If you are from one of these aggregators:
hello!)  I don't really want my content filtered normally, so I'm not
advertising these on the site at the moment.  I may change this stance in the
future, but for the moment they can be found if you look for them.

Jekyll (the framework I use for this site) has handling of tags which I would
describe as "least effort".  As far as I can tell, each page has a list of tag
attributes, and then the site aggregates (at build time) a mapping of tags to
pages.  With a little bit of work, I've got each post displaying this
information as well.  I don't know if this information is actually useful,
since I don't know if I want to enable easy filtering based on it, but it does
seem a shame to hide it.

And to close out this post with an excuse for a pun: I have a bird aggregator
device in the back yard now.  I can watch it from my desk which is nice, but
in the winter at night I mostly just notice that it's running low.
