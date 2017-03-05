---
layout: post
tags:
  - tech
---

It's going to be difficult to keep the tone of this one in check, but let's
see what I can do.  I had an earlier draft of this post in which I justified
every point in terms of mutual respect, but in the shower it occurred to me
that it might be more effective if I presented it in terms of self-interest
instead.  (The theory being that this may more accurately represent the
foundations of the behaviors observed.)

To back up for a moment: I want to talk about how people exchange plain text
over the internet.  Like many social interaction problems in technology, this
one is hard for no clear reason.  I'm far from the first person to write about
these, though perhaps one of the first to present it in this perspective.  But
basically: if one can't be considerate, at least maybe one can be
self-interested.

### Naked Pings

This one makes very little sense to me.  The behavior I'm referring to looks a
bit like this:

    < Anick> Bnick: ping
    < Bnick> Anick: pong
    < Anick> Bnick: are you there?  I have a question
    < Bnick> sure, what's up?
    < Anick> [asks actual question]

A slightly more common variant excludes lines three and four, which makes
sense because they're entirely a waste of time.  But that's the crux of my
point here: the whole exchange is a waste of time.  It happens to be for both
parties, but for a self-interested Anick, the time between starting the
exchange and getting an answer is reduced if the whole "ping/pong" thing is
eliminated.  It's not clever, it's not entertaining, and it's not somehow more
"polite".

A note: this one seems to occur almost exclusively in chat (and almost never
in email).  Perhaps it has to do with the effort of sending messages?

### Asking to Ask

Again in IRC-style presentation:

    -> Anick has joined #project
    < Anick> hey can I ask about project?
    < Bnick> Anick: sure, go ahead
    < Anick> [asks actual question]

This one is similar to the previous - there's an unnecessary layer of
indirection that just wastes everyone's time.  It's not *better* somehow to
ask for permission here: either the question is on-topic, at which point it's
appropriate to ask (this costs two round-trips), or it's not (at which point
it's no more round trips than if Anick had just asked the question).  Save
time and get answers faster by eliminating excessive exchanges!

### Scoping

But it is important to scope properly.  In general, one should send one's
message to the narrowest possible scope; this keeps noise down, which means
faster answers!  As an example, if there is a company mailing list, everything
sent to said mailing list should be relevant to pretty close to the whole
company.  Otherwise one just builds ill-will, and make it more likely that
their recipients will just ignore what is being asked.

This has a manifestation in chat as well: when to use private queries.  One
doesn't need to know someone to query them: in worst case, they will respond
with the the correct channel (or other place) to ask the question.  Of course,
one shouldn't be asking random people random things, but if one knows who the
project author is, and they don't have a discrete channel, for instance, it's
perfectly appropriate to ask them things.  (And of course, I shouldn't have to
say this either, but here we are.)

But on the other hand, if they do have a discrete channel, one will want to
involve the rest of the population of that channel.  More expert eyes means
the problem is resolved faster.

### Attachments

Don't send large files over a text protocol, period.  Not over email, not over
IRC, and so forth.  If there's any doubt, host it.  It means people will get
the message faster, both because they download it faster and because not
everyone needs said file.

#### Formatting

Formatting is somewhat a special case of attachments for implementation
reasons, so feel free to pretend it has a heading of its own if that's
clearer.  But basically: unless the formatting really adds something (for
instance, if it's a new interface mockup), there shouldn't be any markup.
This includes, most importantly, HTML.  Please don't send HTML email; it slows
everything down, including getting the responses needed.

### I Go for Broke

And finally, keep conversation clear and free of clutter.  This will let
others read and understand it faster, which of course means faster responses.
(See the pattern here?)  When replying to email, trim everything that isn't
important, and just reply to the bits that are.  That means posts should look
like this:

    > stuff other person said, which can be of varying size
    >
    > sometimes multiple paragraphs, but order isn't important

    and then the new post's stuff

and should pretty much never include the entirety of the being replied to.
Clarity, increased reading speed, faster response.  The idea is conveyed, I
think; may all your problems be soluble.
