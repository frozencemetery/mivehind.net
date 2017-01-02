---
layout: post
---

Walk through most Linux distro installers these days and the partitioner will
try as hard it can to get swap setup.  It takes about five clicks to get it
not to do that - and two of them on "WARNING: DANGEROUS"-style dialog boxes.
This means a few more configuration tweaks that need to be made for something
that is already delicate: installing a system.  And without not a sane
default, too.

Swap can be conceptualized as "overflow memory" - the space where pages are
evicted to when main memory is full, essentially.  On macOS and Windows, there
is a magic, quasi-invisible "swap file" that the operating system manages
transparently (for the most part); on Linux, a dedicated swap partition is
typically used instead.  But there is no reason one could not use a swap file
on Linux; in fact,
[Ubuntu plans to do just that](http://www.omgubuntu.co.uk/2016/12/ubuntu-17-04-drops-swaps-swap-partitions-swap-files)
by default.  (Yes, I'm late to the party.)

Now, I have cited a blog with the name "OMG UBUNTU!", so we cannot
realistically expect incisive journalism (nor can we from a blog with the
names "MIVEHIND" and "out.log").  But I would think they could do better than
this:

> What’s important here is that some form of swap is maintained, it doesn’t matter how the swap is implemented. Anyone who’s ever used or set-up a ‘no swap’ system only to then run out of memory will know it’s not a pretty experience!

So okay.  I have provisioned "a few" systems, and I have made a few mistakes.
(More than a few, but not the point.)  And yes, in some cases I have run out
of memory.  I think however that this statement - that "it's not a pretty
experience" - misses that there are two distinct ways to trigger an
out-of-memory situation on Linux.

Of note, cwhen a system runs out of memory, it is, yes, not very pretty: if
more memory is requested by a processes, then the kernel terminates processes
until the problem is resolved.  But while it may not be pretty, it is at least
*understandable*, and it is definitely
[readable](https://github.com/torvalds/linux/blob/master/mm/oom_kill.c#L975-L1053).

But let us consider the alternative.  If a system exhausts physical memory and
starts using the swap space, the result is even worse.  Everything slows to a
crawl: the speed of disk access rather than RAM.  The entire system lags,
essentially, while it thrashes the disk.  There are two ends to this
situation, and herein the distinction lies: either the kernel eventually kills
a process with large enough memory footprint (once swap space is exhausted as
well), or the system lurches on (spending most of its life in-or-near a
swapping state).

Keep in mind, though, that filling up swap space takes about an order of
magnitude more time than it did to exhaust physical memory (using the standard
recommendation of >2x swap space as physical memory).  So if we are in the
"runaway process" bucket, it will take a **very** long time before the swap
fills up and the OOM killer triggers.  During which the system will be
borderline unresponsive.

On the other hand, if one configures a system planning to use swap, I really
do not know what to tell you.  In most cases (i.e., servers, personal
hardware, and virtualization; pretty much everything except retro), memory is
not that expensive.  Really.  If you plan to use swap, you introduce
unpredictability into your machine, and that is the opposite of what I
personally want out of my systems.

The laptop and desktop crowd often advocate for another use of swap:
hibernation.  Hibernation ("suspend to disk") is the source of the 2x
multiplier on physical RAM for swap size, since it needs to write out all of
physical memory to disk.  Before I went swapless (which I have been for a very
long time), I did have my laptop set up to hibernate.  And I do not think I
ever used it.  Normal suspend ("sleep" or "suspend to RAM") fulfilled my power
needs in the rare case where I did not just leave it on with the lid closed.
And boot times on Linux these days are so fast that it is not worth
hibernating anyway.

Before we leave, I also need to take issue with the statement that it does not
matter how swap is implemented.  It matters a great deal.  With a swap
partition, one has committed all of that space *to swapping*; it cannot be
used for other things.  On the other hand, with a swap file, and a system that
never swaps, that space can be freely used for other purposes.  If one insists
on hibernating, this is also the clear way to go (especially for encrypted
LVM, the guides for which all seem to incorrectly recommend randkey-swap).

# Final thoughts

So with all that said, it seems as though I am advocating for never having
swap.  Indeed, I almost want to say so, but with the advent of SSDs I am not
entirely sure.  It is possible today to configure everything on a "normal"
(i.e., spinning) drive and then add another drive (fast SSD, for instance) as
swap.  If implemented correctly, this results in using the SSD as a cache for
the spinning drive; the theory, as put forth by Apple and others, is that this
will result in near-SSD speeds in most cases without sacrificing the capacity
(and cost) of traditional hard drives.  I have not yet used reliable SSDs, so
I cannot yet say for sure, but we will see.
