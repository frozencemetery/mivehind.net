---
layout: post
tags:
  - tech
---

This is the first (success) post for a project I've been tinkering with.
Essentially I'm trying to build a KVM switch, except I don't feel the need to
limit myself to USB/DVI/etc.

This week I was able to make the core circuitry for headphone (i.e., 3.5mm
TRS) work.  But let's not get too far ahead.

## Parts

The specialized parts I'm working with are these:

![3.5mm plug and socket components](/assets/2016-09-25-contestants.jpg)

Helpfully, none of them fit on the breadboard I'm using, but it's okay because
neither do the wires I'm using.  You'd never know they all came from the same
supplier.

## To work

Three leads are soldered onto each component.  TRS (Tip Ring Sleeve)
connectors have, as the name might suggest, three paths: a ground, and two
signals.  They're designed such that, when one inserts the plug into the
socket, the ground is the first piece of the plug to make any contact (i.e.,
ground on the most outward part of the socket and the sleeve of the plug).
Arbitrarily, left channel is on the tip, which leaves right in the only ring.

For the sockets I'm using (which are in fact TRS sockets, not TRRRS as the
pins might suggest), there are two extra pins such that the left and right
channels are the outermost.  The manufacturer claims that this is for
stability, but since it won't stay on a breadboard anyway, I don't know why
they bothered.

For the plugs, I found it necessary to wrap each solder joint in electrical
tape before re-covering because otherwise they tended to shift and
accidentally make contact.

## The result

Here's my final, working circuit:

![Flawless, masterful creation](/assets/2016-09-25-product.jpg)

I tested this by playing audio from both my computer and phone
simultaneously.

The magic here is the ground switching.  Having it be a single switch to move
between inputs was a design goal, and this is accomplished by moving the
grounds around.  (Ground is black; there is no excuse for the other colors.)
This results in an incomplete circuit for the "off" input, despite the two
signal channels remaining wired in.

And as long as two inputs are connected, it works great.  That's not to say it
doesn't work great for the single input case as well - it does - just that
there's a somewhat odd behavior there.  If you plug in one input but not the
other and send audio through, the expected thing happens and we get audio out;
however, if we move the switch to the nonexistent input, you *still* get audio
out, just at a much reduced volume.  If one wanted a true killswitch, I
believe this device could be connected to absolute ground, but that would
require plugging it in and I'd really rather not.

## Future work

I don't want to give away too much of my failures, but I do have these USB
connectors sitting on my desk...
