---
layout: post
---

Under the category of "mildly interesting", I've been playing with my terminal
emulator again.  Let me tell you about it.

### History

For the past several months, I've been using rxvt-unicode (or urxvt, as it is
more commonly known) as my terminal emulator.  Among other nice things, urxvt
supports the use of up to 88 colors (the standard being 16).  

#### Sidetrack

Unfortunately, urxvt kept (because rxvt, its parent project, also kept) some
rather obnoxious quirks from xterm, such as the method for configuration.
Editing **~/.Xresources** is fine (until I inevitably forget to run `xrdb
-override ~/.Xresources` and the system state can be best technically
described as "confusing", due to daemonization).

But there's more.  urxvt's relationship with perl approaches worship, going
beyond making the emulator extensible in perl to embedding a perl emulator
within the terminal itself.  I'd be able to entirely look the other way if the
key were something reasonable, unlike what they chose: *M-s*.

To rebind a key for urxvt, one needs to customize a variable in
**.Xresources**; in this case, the variable is `URxvt.keysym.Meta-s`.  But
restoring the behavior of "please pass this key through" is not as simple as
setting the key to blank.  Rather, it needs to be set to the appropriate
escape sequence (think `URxvt.keysym.Control-Up: \033foo`).

If anyone arrives here due to a similar problem, I resolved the conflict by
setting `URxvt.perl-ext-common` to not include "default", which causes it to
no longer embed the perl interpreter.

### Pretty Pictures

Since I was already thinking about terminal emulators, I decided to do an
experiment.  In the course of trying to fix the above problem, I had installed
xterm.  I also installed a 256color build of urxvt and subsequently noticed
that urxvt and xterm (at least in emacs) don't handle 256colors the same way:

[<img src="http://mivehind.net/media/get-medium/0"
alt="xterm (256) versus urxvt-256" align=center />](http://mivehind.net/media/get-medium/0)

Bizarre.  Please note that these pictures are large; click on them for more
detail.

Anyway, for comparison's sake, here's a shot that includes 88-color urxvt:

[<img src="http://mivehind.net/media/get-medium/1"
alt="xterm (256) versus urxvt-88 and urxvt-256" align=center />](http://mivehind.net/media/get-medium/1)

And one more, this time including a libvte emulator as well:

[<img src="http://mivehind.net/media/get-medium/2"
alt="xterm (256) versus xfce4-terminal (16 color, libvte) versus urxvt-88 versus urxvt-256"
align=center />](http://mivehind.net/media/get-medium/2)

The emulator in question (xfce4-terminal) does support 256 colors, but
somewhere in the chain of termcaps and emulating xterm, that information is
lost.  Colortest does show a 256 color grid, but no other application seems to
realize that the emulator is, in fact, full 256 capable.

#### Setup Details

The source file is
[Selection.hs, part of my pwman project](https://github.com/frozencemetery/pwman/blob/master/src/Selection.hs).
Each terminal is running a separate emacs instance, bypassing my configuration
(`emacs -q`) on my laptop (Debian Wheezy).  I have
[magit](https://github.com/magit/magit) installed, and this file is under
version control (which is the source of the modeline).

Thanks for reading; hope you found it interesting!
