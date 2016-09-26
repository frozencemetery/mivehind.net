---
layout: post
---

This is the first in what will probably end up being a series of posts
on the harder-to-search-for pieces of configuration I've applied.  My
configurations typically live
[over here](https://github.com/BUILDS-/Config-File-Cache/tree/master/frozencemetery),
and thankfully I don't intend to go through all of it, just the
complex portions.

## Why even

As this is the first post like this I've written, it's mostly from
things that happened in the last few hours.  Though I guess if I had
to state a theme, it'd be emacs.  And themes.

### gtk3 saga

This is neither the time nor the place for this particular rant, but
it bears mentioning that I do not like gtk3.  Thankfully, I have only
one application on any of my systems that makes use of it
(virt-manager, for the curious; it's otherwise a reasonable program).
I've been living with the default theming for a while now because it's
only the one program, but today I got tired of that.

There are a couple visual theme selectors for gtk2; I used
lxappearance for a while, which was nice because it didn't tie into a
Desktop Environment.  However, there doesn't seem to be an unafiliated
one for gtk3, so I'm editing files (in this case,
*~/.config/gtk-3.0/settings.ini*) by hand.

My current file looks about like this:

```ini
[Settings]
gtk-theme-name = Breeze
gtk-key-theme = "Emacs"
gtk-font-name = Terminus 10
gtk-application-prefer-dark-theme = true
gtk-can-change-accels = 1
gtk-menu-popup-delay = 0
gtk-primary-button-warps-slider = false
```

Most of these are what you'd expect, though I do want to call out
specifically `gtk-application-prefer-dark-theme` for being awesome.
Reading this website has probably already conveyed my opinions on
color and contrast.

What I really want to spend time on, though, is not what's there but
rather what's missing.  Scrollbars, to me, are purely a marker of
where I am on the page: I will rarely drag them around, and almost
never click on the bar itself.  So one can imagine my irritation that
there is no way to tell gtk3 to always show them.  No, they're hidden,
unless an application decides to do otherwise.

The only solution is to set a magic environment variable, probably in
one's shell rc file, like this:

```bash
export GTK_OVERLAY_SCROLLING=0
```

### weechat doesn't use readline

Right up front: weechat doesn't agree with what I (and
bash/readline/emacs) think underscore means in a string.  To me, it's
a separator; if I type "my_thing", it's because I'm joining together
the words "my" and "thing", and I would like to manipulate it as such.
For reasons unclear to me, weechat treats them as one word for the
word manipulation commands (i.e., M-b, M-f, M-bksp, etc.), which I
find confusing and jarring.

As configurable as weechat is, there's no question that there's a fix,
and it's pretty simple; just run
`/set weechat.look.word_chars_input alnum`.  That's not the problem; I do have
a complaint though.  See,

```
Option "weechat.look.word_chars_input":
  description: comma-separated list of chars (or range of chars) that are considered part or words for command line; each item can be a single char, a range of chars (format: a-z), a class of wide character (for example "alnum", see man wctype); a "!" before the item makes it negative (ie the char is NOT considered part of words); the value "*" matches any char; unicode chars are allowed with the format \u1234, for example \u00A0 for unbreakable space (see /help print for supported formats)
  type: string
  values: any string
  default value: "!\u00A0,-,_,|,alnum"
  current value: "alnum"
```

weechat is self-documenting, which means that if you know what option
you're looking for you can get nice doc text out, like that.  (For the
curious, `/help weechat.look.word_chars_highlight`).  In this case, it
even helpfully explained what the default is doing.  No, the problem is
that the higher level explanation of how line editing - and word
parsing - works is just nonexistent.  Weechat's website has some basic
documentation - getting started, FAQ, the most common settings to
tweak - but I have no idea how I was supposed to find this option.
Searching the configurables for "word" or "delim" is decidedly
unhelpful.

### zsh doesn't use readline

I'm not (yet?  We'll see) a zsh user; instead, I'm in that evaluation
period where I've got it installed in parallel and am comparing ease
of various tasks.  That said, I don't understand some of the decisions
that zshle (a readline "reimplementation", as far as I can tell)
makes.  In particular, bash/readline/emacs and zshle seem to disagree
on what non-alphanumerics cause word boundaries and what do not, as
above, though the character disagreements are different.  In fact, the
list of characters they disagree on is listed
[in their source](https://github.com/zsh-users/zsh/blob/6d6b63c884a7484334a22671d2bd6ca138bb8751/Src/zsh_system.h#L440),
but I have no idea how one is supposed to find this because it's
impossible to search for.  In an attempt to fix that, put this in your
*~/.zshrc* to restore some amount of sanity:

```sh
autoload select-word-style
select-word-style bash
```

This will ensure zsh emulates readline correctly for word boundary
delimiters.  (And hopefully I've got enough of those and similar words
in this post that it may be found and useful to someone later down the
line.)

## Final thoughts

I don't really have an overarching point here, except maybe that I
wish people cared more about their configuration documentation.  Good
config docs separate frustrated ex-users from happy tinkerers, who may
become future developers.  And speaking of happy tinkerers, it
frustrates me when a feature seems contentious - scrollbar autohiding,
for one, or really anything to do with recent firefox UI changes, to
pick something I haven't talked about above - but is not easily
configurable.  Less of that, please (especially when the codepaths
already exist); it's insulting to the userbase.
