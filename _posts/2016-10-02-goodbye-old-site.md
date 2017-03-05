---
layout: post
tags:
  - tech
  - meta
---

Some readers (I have readers!) have pointed out that older posts had broken
images and links as the result of site layout changes.  This has now (to the
best of my knowledge) been fixed, but it did remind me that I wanted to make a
post about the transition.  Herein be tech and technical commentary.

## I'm sorry, stepcut

In [the first post](/2013/08/17/hello-world/) on this site (I really called it
hello world.  Let's just pretend that was ironic.), I spent most of the post
talking about the CMS I was using: clckwrks.  Reading the post doesn't really
make it clear *why* I was using that, especially since what I mostly had were
complaints.

I think I liked the idea of the Haskell web more than the execution.  It
needed more effort than I was willing to put in.  And today (when I looked; I
assume this happened a while ago) their website expired and has been
squatted.

The biggest problem for me, in hindsight, was that there were too many moving
pieces that I didn't expect to be moving.  To give an example, the entirety of
post content is written in Markdown (and in my post I have some Words about
the way they implemented that), yet all retrieval is dynamic.

The new site is built on the most boring, robust solution I could find:
[apache2](https://httpd.apache.org/) (httpd, for all you Fedora/CentOS/RHEL
folks) and [jekyll](https://jekyllrb.com/).  At
[Ian's suggestion](https://zenhack.net/2015/08/29/writ.html), I didn't even
write most of the CSS myself - I use a slightly modified
[writ](https://writ.cmcenroe.me/).  Hosting and OS are unchanged (it's even
the same VM, modulo a distribution upgrade).

So what'd that get me?

### RSS

The immediate catalyst was that I wanted an RSS feed, and clckwrks lacked any
notion of that.  At least... I think that's the case; it became increasingly
difficult to upgrade the site software due to running it out of VCS (darcs)
and breaking changes that kept being introduced.  Jekyll just gives me a
reasonable feed out of the box; I didn't even think about it.

### LE

Another thing that has happened since I first set up my blog (because let's be
honest, there isn't a whole lot else on this website) is
[Let's Encrypt](https://letsencrypt.org/).  I don't have anything original to
say about Let's Encrypt itself (okay, I can say "it's the best internet
technology development since Gopher" and that probably hasn't been said
before), but it does work well with apache.  Really well, in fact; I was in
the beta, and they had already scripted the apache install.  clckwrks didn't
even understand the concept of HTTPS.

### Broken links

Because the site's entirely static, it's checked into a git repo because of
course it is.  This is useful here because I can point at
[part of](https://github.com/frozencemetery/mivehind.net/commit/dd1ac76c1bd4ca9d83cfc3192df6545aee819000)
the link fixups I ended up doing.  The inability to name images in clckwrks is
honestly somewhat perplexing; "0" is not a meaningful name for this image
since it doesn't even include an extension (though clckwrks only supported
jpeg).  Hopefully this is the last bit of migration I'll have to do; in
hindsight I will miss having "slug" in
[all of my URLs](https://github.com/frozencemetery/mivehind.net/commit/bd2e1962c07b7fa4a99c482959ad8433b2bbe76a).

I did actually look into not breaking every link on the site at the time of
migration.  Unfortunately, clckwrks layout didn't correspond to something I
can make a rewrite rule for, so I elected instead to fix what I knew was
broken and let the rest emerge nebulously in the future.  Three and a half
years later, it finally has.
