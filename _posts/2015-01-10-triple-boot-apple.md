So you've got yourself some Apple hardware, and maybe you're like me.  Maybe
you don't want to just run one operating system: maybe you want to run ALL the
operating systems.  Maybe what you want is to

Triple Boot
===========

or even n-ary boot.  The reason I use "triple" is to denote the three
different classes of bootloaders in use: OSX, Windows, and GRUB.  (Increasing
the number of bootloaders drastically increases the complexity of the system;
I recommend sticking to as few as possible.)

I also mention Apple hardware above not to evangelize or even suggest the
purchase of such, but rather because running OSX on non-Apple hardware is
still somewhat of a grey area.  Staying cautious, I will not link instructions
for that here; I will instead suggest that if one really wants OSX, you can
[run it in KVM](http://www.contrib.andrew.cmu.edu/~somlo/OSXKVM/).

Prep Work
---------

First and foremost, make a backup of anything you care about.  This includes
ensuring you have the ability to re-install all operating systems, not just
their data.  (For OSX, the recovery partition is likely sufficient, but if you
know how to make a bootable image I suggest doing so.  I kept my 10.6 DVD
handy for this.)

Along with that, you will need a 1GB+ USB stick (4GB+ is even better), a
Windows install image (DVD; I'm using Win7), and a Linux install image (CD;
I'm using Debian Wheezy).  A wired internet connection is helpful but not
obligatory, as is an OSX install image (DVD or USB stick).

Please also read the entirety of this post before making any changes to your
drive(s).  Since all of this information is in my head, I can't guarantee that
I mention all of it before you'll need it.  Please accept my apologies and be
careful.

Partitioning
------------

Do this as early in the process as possible because it's the hardest to
change.  We will be messing with the partition table, which is a frail and
brittle thing to begin with, using multiple hammers.  There *will* be carnage
and casualties, either now or down the road when Windows gets upset that it's
not the first OS on the drive (this is a thing).

Decide on a partition layout before you do anything else.  Keep in mind that
certain configurations (e.g., all on one drive) may require bootloaders to
load each other which is incredibly delicate; you may wish to perform a
proof-of-concept deployment for your partition table before committing.  This
time around, I have put each OS on its own drive, though I have previously put
them all on the same drive (and used GRUB to load the Windows bootloader).

1. The best time to partition is right before OSX has been installed.  When
   you boot the installer, after choosing a language, enter Disk Utility, and
   create the layout you desire.  ***Do not create "free space" partitions***
   in Disk Utility; instead, make them another filesystem that you will later
   write over (e.g., FAT32).
2. Barring that, with OSX booted, certain parts of the partitioning scheme can
   be adjusted from Disk Utility (Applications -&gt; Utilities -&gt; Disk
   Utility).  This will not work for all configurations.
3. Boot Camp (see below) will optionally perform some minimal partitioning in
   the process of its operation.
4. Booting from the recovery partition of OSX (hold down the "option" key
   during boot, then select it when prompted) can provide a Disk Utility more
   capable than the one instide OSX.
5. If you have OSX install media, booting from it will provide a Disk Utility,
   as in the pre-install case.
6. As a last resort, the USB stick can be turned into a Recovery Partition of
   its own which can be booted to obtain Disk Utility as above.  (This is
   useful because Disk Utility will sometimes refuse to modify the volume from
   which it booted.)  The program to do this can be found
   [on Apple's website](https://support.apple.com/kb/DL1433).
7. I know of no other ways to repartition short of reinstalling OSX.

(For the curious: yes, I did use all six of the above in roughly the order
listed in order to tweak my partition configuration.  This guide is very much
the result of trial and error.)

Alright, go ahead and install OSX if you haven't.  Then it's time for

Installing Windows
------------------

Put your Windows install in the CD tray and plug in your USB (doesn't matter
what's on it; we'll be reformatting it momentarily).  Then open up Boot Camp
Setup Assistant (Applications -&gt; Utilities -&gt; Boot Camp Setup
Assistant).  It will ask a couple questions; make sure to check the box to
install drivers from Apple, as this is the reason for the USB.

If you are installing Windows to a different drive than OSX, when the machine
powers off before booting windows, remove the drive containing OSX.  This
avoids Windows trashing the partition table.

Windows will restart several times during installation because installations
aren't allowed to be simple.  When it finishes, open up the USB, go to the
"BootCamp" folder, and run the "setup" application.  This will take a few
minutes and install any drivers needed for your system and a bunch of others
you don't need.  Do not be alarmed if Windows does not understand your display
or graphics card during the installer; the drivers will be installed when the
application finishes.  It will require a restart.

At this point, switching between OSs will require holding down the 'Option'
('Alt') key during boot to use Apple's boot menu.

Installing Linux
----------------

This is oddly enough the trickiest part of the installation.  Apple systems
boot using EFI, but it's not the EFI you'll find on any other system.  They
switched to EFI booting between two versions of the specification, so it has
features of both.  The result is that Apple EFI is effectively a different
boot method in that if the boot process is not coded for it explicitly, it
will likely not work.

The result of the above is that I will not be creating an EFI-booting Linux.
If you wish to do so - and there are reasons, mostly hardware-related, why you
might want this - you will unfortunately have to look elsewhere; I'm happy
just having this working at all.

The key factor to booting non-EFI Linux (using BIOS emulation) is to have an
MBR present on the drive that Linux is booted from.  If Linux is the only OS
on the drive, then it's conceptually easier: just use an MBR on the drive.  If
it's also on a drive with an EFI-booting OS (OSX, Windows, etc.), then with
some trickery one can place an MBR onto a drive that uses a GPT.

If you're going the Linux-only drive route, then you need the drive to have an
MBR on it before you install Linux.  To do this with a Debian install image,
just use an Expert install (a regular install will not work, since d-i
defaults to GPT on Apple drives).  If you're not comfortable with that, or
using a different image, you can use `fdisk` instead.  You don't need to set
up the partitions themselves here; just ensure that it has an MBR.  Then
install your Linux as normal.

Otherwise, install Linux without overwriting the partition table.  This is why
it's important to partition everything out beforehand, allowing space for the
Linux volume on the OSX drive, for instance.  Then you need to sync the GPT
with the MBR that Linux has created.  The easiest way to do this uses a tool
called [rEFIt](http://refit.sourceforge.net/).  rEFIt's website has a notice
that it's no longer maintained (which is true) and recommends rEFInd instead
(I disagree with this).  rEFInd will not sync the GPT and MBR in the way we
need, so it's not useful.  Another way is to use the `gptsync` utility.

Finally, even if you're not installing Linux on the same drive, you may wish
to install rEFIt as a boot manager anyway.  It looks like the rEFIt
installation process may be borked under OSX 10.10, which is unfortunate; I've
heard tell that manually installing it will work, but I did not test it.
rEFInd may be capable of performing this task, but again, I have not tested.

My Setup
--------

I have a MacPro4,1.  The first drive is 80GB of OSX 10.10 only; the second
drive is 600 GB of Windows7 only; and the third drive is 600 GB of Debian
Jessie only.  I've swapped the graphics card for an ATI Radeon HD 5770 (read:
this works without EFI booting).  The wireless under Linux require the
proprietary driver (b43 does not support N on this card).  The only quirk I've
uncovered is that going directly from Linux to Windows without going through
OSX first results in the wireless not working, which can be fixed by booting
OSX and then the desired system.

Previously, I owned a MacBook3,1.  At the time I was unaware of how to get
Linux-only setups, so the first 20GB of its drive was an unused OSX 10.6, and
the remainder was Debian (initially Lenny, then later Squeeze and Wheezy).
b43 did not yet support the wireless card, so it was using wl, though the
graphics worked fine.  I did have it booting Windows as well, though this
introduced too much instability (Windows ate the partition table at one
point) and was quickly removed.

Acknowledgments
---------------

I did not write any of the tools mentioned in this post.  Much of this is the
result of my own trial and error, though I have also gathered information from
[the Arch wiki](https://wiki.archlinux.org/index.php/Macbook) and
[the Debian wiki](https://wiki.debian.org/MacBook) (to which I have added back
relevant portions of my findings).
