---
layout: post
tags:
  - tech
---

Apologies if this title brought you in expecting something technical.  You
should still read it.

## Software Evaluation Threads

```
THERE was a little girl,
And she had a little curl
  Right in the middle of her forehead.
When she was good
She was very, very good,
  And when she was bad she was horrid.
-- Henry Wadsworth Longfellow
```

All to often I encounter, as I imagine most people working on software do
these days, this specific kind of thread.  The scenario is always the same,
and unfortunately the outcome is always the same; I have yet to see a single
productive version of this.

Let me setup an example (that I hasten to add is not verbatim lifted from any
such exchange I have witnessed).

So the first message will look something like:

```
> We are evaluating the use of NüSoft's Prog™.
> -- Jeff E.
```

And the thread might go on for a bit, but eventually there will be a reply
like:

```
> When I tried to use Prog™, it set my bed on fire.
> -- Cozy N. Warm
```

Which seems reasonable to complain about, and is invariably followed by a slew
of:

```
> That's weird.  It worked fine for me.
> -- Wilma from Minnesota
```

and similar messages like

```
> Me too.  Prog™ is great; I used it every day at my last job.
> -- J. Olive Barton
```

until we're left with nothing but

```
> +1
> -- Mike Minestrone
```

and in the end no progress is had and we all go home and lament the futility
of convincing people on the internet that they are Wrong.

I submit that the reason these threads go anywhere - and, indeed, are never
useful - is because no information has been exchanged.  This may seem odd,
given that many messages have been exchanged, and there is data in a nonzero
number of them, but since no conclusions have been drawn, nothing has been
*learned*.

What I mean by that is that nothing can be stated from an exchange of this
nature about Prog™.  This isn't precisely true: one can easily observe that
Prog™ clearly works for some people, and clearly doesn't for others.  The
issue is that this isn't *new*: for any piece of software that isn't outright
broken, it will work for some people and fall short of the needs of others.
(It is perfectly valid to care about one's bed being fire-free, but others
sleep in hammocks and therefore have no beds to catch fire.)

In the end, it is in fact horrid.

### What went wrong?

```
One day she went upstairs,
When her parents, unawares,
  In the kitchen were occupied with meals,
And she stood upon her head
In her little trundle-bed,
  And then began hooraying with her heels.
-- Henry Wadsworth Longfellow [1]
```

Like many issues on mailing lists, this could be solved with more curation of
behavior.  Let's take it a message at a time.

#### Jeff E.

Jeff E. starts it off.  I want to commend Jeff E. for letting the community /
organization body know what's going on, but they've also set us up for failure
by not indicating the type of feedback being solicited.  What is the feedback
being solicited?  We'll get back to that.

Side note: I am not interested in assigning fault or blame.  I am interested
in causes of behavior, and in those only to prevent the behavior and to
encourage useful discussion.

I want to encourage Jeff E.'s post, but with more guidance.

#### Cozy N. Warm

Cozy is trying to do the right thing here.  They earnestly believe that there
is a problem with the Prog™ that makes its adoption not at all clear-cut.  I,
and many readers, am entirely willing to believe that their bed was set on
fire, but enough information just has not been provided.

To put it as succinctly as I can: reports of bugs are useless without bug
reports.

If Cozy encountered an issue and did not file a ticket, Cozy is part of the
problem.  The developer is likely unaware of the issue, or the information is
outdated and no longer relevant.

On the other hand, if Cozy has filed an issue, they ought to link to the
issue.  This can provide valuable insight: for instance, if it has been fixed,
Jeff E. may restrict to newer versions.  Alternately, there is value in
understanding how a project handles tickets.

This gets its own paragraph: if your project does not have a mechanism for
users to report bugs, it cannot be used.  Period.  This is bug #0.

I want to encourage Cozy's posts as they are clearly valuable, but they need
to have data.

#### Wilma from Minnesota

Wilma has produced a no-op, and one that very quickly becomes flamebait.  She
has added nearly nothing to the discussion.

Software working correctly is the status quo, the norm, the expectation.  We
assume this by default (or otherwise we do not use it).  When Jeff E. makes
the original post, they have presumably done their research: enough legwork
has happened to determine that Prog™ has the potential to address some
perceived deficiency.

I want to discourage Wilma's posts as they add nothing.  At *most* one per
thread so that we know it works for someone, if that's not clear.

#### J. Olive Barton

Stop.  No.  If Wilma added nearly nothing, you are *actually* added nothing.

Please, please do not make these posts.

#### Mike Ministrone

You have been added to my [killfile](https://en.wikipedia.org/wiki/Killfile).
I may write more on why this is later so I can link it to people when I do so.

### How do we do this properly?

```
Her mother heard the noise,
And she thought it was the boys
  A-playing at a combat in the attic;
But when she climbed the stair,
And found Jemima there,
  She took and she did spank her most emphatic.
-- Henry Wadsworth Longfellow, [1]
```

I believe that these discussions can be had productively, and I think that
much of the burden here lies on the original poster (Jeff E., in my toy
example).  I am not interested in whether it *deserves* to be on them, since
only the original poster and the mailing list moderators are in a position to
enforce thread content.

While I do want to approach this with a more modern mindset than Longfellow's
19th-century one (especially on corporal punishment and gender), some kind of
enforcement needs to take place at the threat of a flamewar.  This doesn't
have to be explicit, overt expression of authority (though it can be, if
that's the environment): something as simple as a reminder that a post is
inappropriate or flamebait combined with a reminder to the community not to
reply would suffice, for instance.

And in order to have productive thread curation, expectations must be overt
and upfront.  Jeff E. needs to state, in the original email, that the Cozys
need to cite their bugs, that the Wilmas should keep it down, and that the
J. Olive Bartons are just making noise.  (That Mike's post is not welcome is
something that I think should be implied everywhere where voting is not
solicited, but more on that perhaps in another post.)

Then perhaps we can have a productive discussion instead of throwing mud.  And
in the end when Jeff E. presents the summary, as I hope they would, concerns
can be mapped to appropriate resolutions.  In this way, posters can walk away
satisfied that their voice has been heard, instead of drowned out in by a herd
of "but it worked for me!".

## Citations

The full text of the poem "There was a little girl" was found at
[Bartleby](http://www.bartleby.com/360/1/120.html) accessed 28 August 2016 and
is in the public domain as far as I know.
