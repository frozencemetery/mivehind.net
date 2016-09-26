---
layout: post
---

So this week I thought I'd share a bit of change in my life.  It's not
earth-shattering or anything, but it's certainly different for me.
I'm not actually a Luddite (even as I use the term jokingly when
describing, e.g., my hatred of JavaScript), but I do often think we
over-rush change.  In particular, I think we lose good things about
the "old ways" in our rush to adopt the newest toys.  For instance,
right now as I write this I'm also ripping CDs on the same computer.

But that's not what I'm going to talk about here, though I do enjoy talking
about CDs and music.  This post is about an instance of the opposite problem:
when holding on to the old ways is doing more harm than good.  That makes it
sound more grandiose than it actually is.  This post is about setting up my
(first) smartphone, the mechanical details, and some small reactions to it.

## Burn it to the ground

The new device (I'm going to work very hard not to call it a toy, as it's
increasingly not just a first world thing anymore) wholly replaces two
existing pieces of technology, in addition to the new things it brings.

### Phone

This is the obvious one: a dumbphone.  I have owned two previous phones, and
in both cases they have been replaced when they are physically no longer
working.  I got the first one in seventh grade, when I started spending more
time away from home: this meant it was a tracking device in two ways, not just
the usual government one.  It lasted through (I want to say two) battery
replacements over seven years until it died *during* my interview process at
Red Hat.  The second one didn't last as long - one battery replacement and
about five years, if my math is right - and it's not hard-dead in the same
way, but it's close.

Obviously the new phone makes calls and tracks me, so functionality is wholly
superseded.

### Rockbox

For a couple years now I've also owned a used device (happens to be an iPod
because of price and disk size) on which I ran the
[Rockbox](http://www.rockbox.org/) unstable port.  It plays music - even my
Music Nerd™ formats (Vorbis) - and has worked surprisingly well, modulo a few
crashes.  I did manage to get the new device to play music, though it took a
surprising amount of effort due to the size of my library.  More on that
presently.

### New device

I don't want to plug a particular manufacturer, but suffice it to say that the
device has the following features:

- android (happens to be 6/Marshmallow; more later)
- unlockable bootloader from manufacturer
- works on my cell provider of choice
- 3.5mm TR*S jack
- enormous microSD capability

I'm also indebted to my friend A.J., who knows more about (ab)using mid-line
technology than anyone else I know, and patiently explained a lot of the
ecosystem to me.

#### Unlock bootloader

As I mentioned, the manufacturer allows bootloader unlocking (which translates
into eventual rooting of the phone).  One catch: gotta turn it on in Android.
And it's hidden in developer mode.

I'm sure someone thought this piece of interface was Very Clever, but to turn
on developer mode, you go into Settings, then all the way at the bottom About
Phone.  Then you tap on the Build number ten times.  After the first five, it
starts displaying a countdown of "You are # clicks away from becoming a
developer", which makes me wonder why they even bothered.  (Side note: I'm
pretty sure it's five, but I can't actually test because when I click on it
now it tells me that "No need, you are already a developer".)  The whole thing
just seems juvenile.

Developer mode on, you go into Developer Options and enable OEM unlocking.
From there, I just installed the appropriate parts of the Android SDK
(requires Debian testing; the right bits aren't in Debian stable at the
moment) and followed the manufacturers instructions and signed away all my
rights to them ever fixing the phone for me.  Not that they ever would.

Then after a factory reset and activating the phone again (why even...), I can
actually start setting it up properly.

#### Encrypt phone

Not much to say here.  I did this before adding data to the phone to save time
re-encrypting it later.  Into Settings, then Security (under Personal for some
reason and not Device) and encryption controls are right there.

For an entertaining digression, I did some back-of-the-envelope calculations
on the maximum amount of entropy available for the various forms of unlocking:

- First, there's PIN.  The maximum number of digits is 17; there are ten
  possibilities for each digit.  I'm going to be lazy and call the upper bound
  on number of possibilities 10^18, which is almost 60 bits.

- Next, we have the pattern unlock.  This one actually is the most complex to
  calculate well; I tried to snipe Kit into doing it, but she wasn't having
  any of it.  There's a 3x3 grid of dots; you can start anywhere (though
  orientation matters) and go from any dot to any other dot as long as you
  don't repeat.  The weird caveat is that you can't jump over dots: that is,
  you can't go corner to corner since you'll go through one on the side along
  the way.  Ignoring that last property, it's a bit over 9 factorial for the
  number of possibilities; call it 10 factorial to gratuitously overestimate.
  Nearly a whopping 22 bits.

- Finally, we have password.  This one's easy again: 17 character maximum, no
  non-ascii non-printable characters permitted (so 94 possibilities for each
  digit).  Again with the lazy upper bound: 94^18, so almost 118 bits.  This
  is the clear winner.

Onward.

#### Add SD

Storage is weirdly cheap now to me who grew up when 1.44 MB floppies ruled the
land and CDs were still high-end.  A 128 GB SD card that has data transfer
rates of about 80 MB/sec costs $40 - and is smaller than my thumbnail.

Android Marhsmallow has a new feature over previous versions of Android: the
ability to "format as internal" a SD card.  That is, instead of being a
removal item, it is treated as part of the system storage: so applications can
write there and enjoy its high speed, but the SD card cannot, they warn, be
used with other devices.

(This is not quite true.  It's just dm-crypt, so if you know the keys and are
handy at the command line, you can load it just fine.  It may be a better
approach than what I did for the next step.)

The final thing to do is move system data that's on the (actual) internal
storage onto the microSD.  This seems inconsequential, but it actually causes
the system to change what it presents as the system data store.  This has
consequences for mounting it.

#### Mount it

The device doesn't really export a filesystem per se (because that would be
Hard) but rather speaks a network protocol called MTP.  (It will also speak
PTP, but will only export the **Pictures/** directory over this protocol, so
it's basically useless.)

However, the operation I'm trying to do here is to rsync my entire music
library (all ~75 GB of it) onto the SD card.  So I really do need a
filesystem.  The obviously named mtpfs doesn't work (it likes to crash instead
of mounting), but jmtpfs works just fine.

```bash
mkdir ~/mnt
jmtpfs ~/mnt
# rsync data here
fusermount -u ~/mnt # unmount when done
```

Looking inside the mounted phone, what you see will depend on whether you
moved data onto the SD card or not.  If not, you will see a volume called
**Internal Storage** the size of the phone's (actual) internal store.  If you
did, you will see a volume called something like **ManufacturerName SD
card**.  The phone seems to not provide access to both, which is irritating
and took rather a long time to figure out.

The real difficulty comes in getting the rsync command right.  Normally when I
rsync, as I imagine is true for most casual users, it's happening over SSH.
So we want flags like `-z`, for compression, and a whole host of other
things.  These work fine because the underlying filesystem - and the SSH
interface - behave in a reasonable manner.
[MTP does not](https://github.com/kiorky/jmtpfs/blob/master/README#L76-L95).
In particular, there is: no such thing as a rename, no such thing as a partial
write, and no way to query the other end for a checksum (which rsync really
wants to do).

So to start with, we need some standard rsync flags: `-rvP --delete`.
Recursive, verbose, partial files (not strictly needed) and delete extraneous
(for modifications and temp file clearing).  To that we need to add some flags
to work around MTP: `--inplace` (since moving files isn't a thing rsync can
do) and `--size-only` since we can't query for checksums easily.  Then there
are some flags we carefully leave out: `-z` for compression slows everything
down, and `-a` just adds a whole host of things we don't want.  It ends up
looking something like this:

```bash
rsync -rvPO --inplace --size-only --delete \
    /var/lib/mpd/music/ ~/mnt/Foo\ SD\ card/Music/
```

You probably want to make sure your phone's music player is completely off (no
background processes or anything) while this is happening, otherwise it may
aggressively scan for new files as they come in and that will make its little
head explode.  Figuratively.  The CPU heat is real though.

#### root it

You can do this at pretty much any point after unlocking the bootloader, so
I'm going to put it here because it's pretty standard.  I used TWRP into
SuperSU, which I think is pretty standard; other people have written better
guides elsewhere that are probably device-specific to some degree.  The result
is that applications can ask for root - like my terminal emulator - and I get
a dialog box about granting it (and setting some policy on that).  It's
actually fairly uninteresting.

### The future

That's mostly it.  There are a couple things I haven't gotten working, mostly
around scrobbling (i.e., last.fm submission): the official application for
this is frankly terrible (crash heavy), and doesn't distinguish podcasts from
regular music.  (And while I have no problem with the world knowing that I
enjoy the audio stylings of Click and Clack, that data is not for last.fm.)

There are many things I like about this: the portability of the device is
incredible, having my calendar in my pocket is really useful, and there are
useful tools people have written.  But in the spirit I opened with: this is
also a severe step backward.  More of my data is going to Google now (and my
cell service provider, who aren't great people either), and that's been hard
for me to come to terms with.

I think this is more of a forward step than a backward one, but that doesn't
mean I'm not going to miss the way things used to be.  It's really the only
game in town.
