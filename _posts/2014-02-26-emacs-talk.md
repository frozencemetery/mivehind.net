---
layout: post
---

This writeup comes from a presentation I gave on behalf of the CMU Computer
Club.  This was the second time I gave this talk, th first time as a guest
lecturer for 15-131: Great Practical Ideas in Computer Science at CMU.  If you
are not interested in emacs, this post is probably not for you.

Emacs Talk Notes
================

> A novice of the temple once approached the Master Programmer with a
> question: "Master, does Emacs have the Buddha nature?" the novice asked.
>
> The Master Programmer had been in the temple for many years and could be
> relied upon to know these things. He thought for several minutes before
> replying: "I don’t see why not. It’s bloody well got everything else."
>
> -- [Collection of Emacs Koans](http://www.emacswiki.org/emacs/EmacsKoans)

A Quick Note for OSX Users
--------------------------

This is a fix for a problem that affects users of Mac OS X only.  All other
users should skip this section.

Apple has decided that by default in the OSX terminal emulator (Terminal.app),
the Alt (Option) key does not send the proper key signal to the terminal.  To
fix this, you will need to do the following:

1. Open Terminal <br> ![](http://mivehind.net/media/get-medium/3)

1. Load the Preferences... dialogue <br>
   ![](http://mivehind.net/media/get-medium/4)

1. Click on the "Settings" section <br>
   ![](http://mivehind.net/media/get-medium/5)

1. Click on the "Keyboard" tab <br>
   ![](http://mivehind.net/media/get-medium/6)

1. Check the "Use option as meta key" checkbox <br>
   ![](http://mivehind.net/media/get-medium/7)

Congratulations, you now have set what should have been a default.

## Getting Started

First things first, open up a terminal and type `emacs`.  You should see a
screen welcoming you to emacs.  One thing that should catch your interest is
on the left side: instructions on how to open the tutorial.  For clarity's
sake, I will repeat them here: to open the tutorial, press **Control**, tap
**h**, release **Control**, and tap **t**.  (In emacs notation, this is denoted
**C-h t**.)  I will not run through the tutorial here, and the topics that the
tutorial and I cover will be nonidentical sets.  It is worth running through
the tutorial at least once, even if you are already an experienced emacs
user.

Beyond the tutorial, there are two commands and a website that you should be
aware of.  First, the [Emacs Wiki](http://www.emacswiki.org/) (from where the
opening quote came!) is an excellent collection of all things emacs.  Chances
are that if you are doing something with emacs, someone has done it before and
posted there on how to do it, and if not, you can edit it and add your own
experience!

The command **C-h k** (followed by a key command) will give information about
what will happen when that key command is entered.  So, for example, **C-h k
C-h k** will give information about giving-information command.  In
addition to a description of what the key does, it tells you what *command*
the key will run (describe-key, in this case).  In fact, if we know the name
of the command we wish to run but not the key sequence (or it is not bound to
a key sequence), we can run the command anyway by hitting **M-x** and then
typing the key sequence.  So, for example, **M-x describe-key** would perform
the same action as **C-h k**.  (The logic for this naming is help: key.)

Additionally, if we know the name of a command but would like to know where it
is bound, we can use the sequence **C-h w** and type the name of the command
to ascertain its whereabouts.  So, for example, **C-h w describe-key** will
tell you that it is bound to **C-h k**.  (The logic for this naming is help:
whereis.)

The content in this splash screen buffer is just text; although we cannot edit
it, we can still move the cursor within the buffer.  Now, your first instinct
here might be to try to use the arrow keys, and while emacs is friendly and
will accommodate this instinct, since this is a talk for advanced users I'm
going to encourage you to learn the emacs idioms for movement.  So: to go
forward a character, press **C-f**, and to go backward a character press
**C-b**.  To go to the next line, press **C-n**, and to go to the previous
line, press **C-p**.  Note the major advantage here that at no point do your
hands shift position to move the cursor as would be required for the arrow
keys.

We can also navigate by word instead of by character.  To do this, we use
**M-f** to go forward a character, and **M-b** to go backward a character.
But wait, what does the capital M mean?  Well, the short version is that it
corresponds to the Alt key (Option, if you're an OSX user and fixed the bug),
and that you can also use the escape key (but really shouldn't unless you are
on a keyboard without an Alt key because of how far off the home row it is).
The longer version (and you should feel free to skip this) is that it
corresponds to whatever your terminal emulator takes as "modifier" key.
Historically, there actually was a Meta key, and it sat under to the left of
the control key (which was under the thumb) on the Symbolics Lisp machine
keyboards at MIT like this one:

[![Space Cadet Keyboard](https://upload.wikimedia.org/wikipedia/commons/4/47/Space-cadet.jpg)](https://en.wikipedia.org/wiki/Meta_key)

One more thing before we move on.  If you ever mistype a command and want to
cancel it, you can hit **C-g** (this is the key sequence to generate a Bell
Character at a prompt, if you have ever done that).  There is also an undo
feature, but we'll get to that in a bit once we've gone over editing.

Acknowledge the Enemy
---------------------

Many of you may know that there was a similar talk on vim last week.  I
wouldn't mention it, but they took some shots at emacs that should be
addressed.

First, emacs commands are not random.  They are designed to both allow for the
huge number of commands that can be used in emacs (and it is huge) while being
easy to remember.  Most are chosen to use letters associated with their action
('f' for forward, etc.).  They are also fully rebindable, but I'll get to that
later.  The system for multipart key sequences can be thought of as a
heirarchy: we enter the first sequence (e.g., **C-h**) to indicate what class
of action we want to perform (help), and then specify this action (**t** for
the tutorial).  Another multipart form we'll see in a moment starts with
**C-x**, which refers to files and buffers.

Second, the vim talk asserted that most of the user's time is spent performing
editing tasks: navigating around files, searching for things, etc., and
therefore we want a distinct system of modes.  While I can't say whether this
is right or wrong, I have observed that most of my work switches very rapidly
between "writing" (where I insert characters) and "editing" (where I move
around and delete things).  Having an expensive context switch as vim does
doesn't make sense for my workflow, and I believe does not make sense in the
general case either.

There are also some key differences between the advice I will give you about
using your editor and what was said last week.  For instance, "plugins" for
emacs are wonderful, and fun to write, and I won't tell you to stay on the
home row while simultaneously telling you to reach for escape all the time
(I'll just do the former and not the latter).

Editing files
-------------

One of my vim user friends was attempting to edit a file in emacs a few years
ago.  So he opened the file using `emacs filename`, and then stared at the
screen for a second, his hands hovering over the keyboard.  Then he asked "How
do I type?".

Of course, we told him that there's no mystery here, no layer of indirection,
nothing confusing about it in any way: you just type.  So he proceeded to add
to the file, and all was good.  Until he made a typo.  Again his hands hovered
over the keyboard, and again he stared at the screen for a second, and then he
asked "How do I... not type?".

He was still using the vim model, where you have to go into another mode to
make changes to existing text.  We explained to him that in emacs, you just
make the changes: press **&lt;backspace&gt;** if you want to delete the
previous character, or **&lt;del&gt;** to delete the next character.  We even
told him about **M-&lt;backspace&gt;**, which deletes the previous word, and
**M-&lt;del&gt;**, which deletes the next word.

When he was done, he knew enough to save with **C-x C-s**, but when it came
time to exit he just gave up, which was a bit of shame because I had a great
metaphor involving goats prepared to explain the difference between killing a
buffer with **C-x k** and exiting emacs entirely with **C-x C-k**.

More Editing
------------

Some other useful commands you might enjoy are **C-a** (go to beginning of
line, 'a' being the first letter of the alphabet) and **C-e** (end of line).
In pure text modes, they also have cousins **M-a** and **M-e**, which go to
the beginning and end of sentences, respectively.  When dealing with matched
punctuation (like parentheses, angle brackets, square brackets, or curly
braces), **C-M-b** and **C-M-f** go backward and forward respectively to the
matching symbol.  Note also that when the cursor is placed on one of these
symbols, its partner will be highlighted.

Often when editing code, it is useful to split the editor window into multiple
panes.  To accomplish this, emacs uses a model strikingly similar to the
`fork()`/`exec()` model found in the unix world.  That is, the current view is
split horizontally using **C-x 2** or vertically using **C-x 3**, and then
one of the two resulting buffers is switched to another view, either by
opening a file with **C-x C-f** or by switching to a different open buffer
with **C-x b**.  When it's time to finish split viewing, the currently focused
buffer split can be undone with **C-x 0**.  However, if there are many splits,
it may be easier to use **C-x 1**, which makes the currently focused buffer
the only visible buffer, destroying all splits.  Finally, if you have multiple
buffers visible through splitting, you'll probably want to move between them,
which you can do with **C-x o**.

Within emacs, there exist mechanisms for buffers to communicate with each
other.  (This isn't precisely true and how it works is complex, so I won't go
into how it works, just how to use it.)  An extremely useful consequence of
this communication is the ability to integrate REPLs.  A REPL
(Read-Eval-Print-Loop) is what we refer to more commonly as an interpreter
session.  Examples include `ghci`, `sml`, `python`, `ipython`, `sbcl`, and
many others.  (Emacs is itself in this category, but more on that later.)  To
launch a "captive" python repl, with a python file open, one invokes **M-x
run-python** (other repls similar).  The view will be split, and a buffer
containing the repl will appear.  It can be used as normal (with the exception
that the up and down are now bound to **M-p** and **M-n** so that the cursor
can move freely in the buffer) repl, but that's not where the magic is.  With
cursor in the python file, type **C-c C-c**.  This loads the code into the
python repl, and makes it accessible (or reports errors).

It's worth noting that compiled languages are not left out of the fun; on the
contrary, they have a different feature.  Emacs integrates with many build
systems, including the venerable Make.  It can parse the compiler output from
`make` and determine whether and where any errors occurred in the source
files.  To use this process, invoke **M-x compile** to run `make`.  Then - and
this is probably my favorite emacs feature - on any errors, press **C-x `** to
jump to them in the source file.  It's beautiful, it's fast, and it doesn't
involve multiple terminals.

More Motion
-----------

So I've introduced here a lot of content-sensitive motion, but what about more
traditional motion?  Don't worry, I've got you covered.  Emacs will respond as
you expect to pageup and pagedown events, but like with the arrow keys,
there's a better way.  **C-v** scrolls the buffer down (it points down), and
**M-v** will scroll the buffer up (down is the cousin of up).  **C-l** is an
especially interesting command: press it once to center place the current line
at the bottom, again to place it at the top, and a third time to center the
current line.  We've even got keys to go to the top and bottom of the buffer:
**M-<** and **M->**, respectively.  When dealing with a block structure,
**M-{** goes to the top of the previous block, while **M-}** goes to the
bottom of the next block.

Emacs does of course also have searching features.  To search for text, press
**C-s**, and then start typing the search string.  This will search forward
for text, but for doing the same thing in reverse, you'll want **C-r**.  To go
to the next occurrence of a match, press whichever search key was used to
start the query again; to switch the direction of the search, press the other
search key to invert it.  When searching, **C-g** will cancel the search and
restore the cursor position, while any other control sequence will end the
search at the current position (and perform the indicated action).

Find and replace is **M-%**.  Think of this as substitution: the string on the
top is substituted for the one on the bottom.  You will be prompted for the
search string and the replace string, and then interactively walked through
the replacement process (with replace all being an option).  You can even
include newline characters: press **C-o** to insert a newline after the
cursor.  (Be careful here: Unix, Windows, and pre-OSX Mac OS *each* use a
different convention for delimiting the end of lines.  **C-o** is appropriate
for Unix systems only.)

Couscous might be the food so nice they named it twice, but undo is the
feature so important it has four different bindings.  They are: **M-x undo**,
**C-x u**, **C-_**, and **C-/**.  The last binding is likely the most
convenient to type, but some keyboards do not send this key event properly
(and yes, I have actually encountered this), so it is also bound to **C-_**.
In possibly the most entertaining design decision in hindsight, **C-_**
suffers from the *same* kind of problem as **C-/**, and so it is bound *again*
to **C-x u**.

Anyway, undo works like a stack.  You pop commands off of the stack and
de-apply their changes to the buffer.  One interesting aspect of this design
is that there is no explicit "redo" command; instead, perform an action (such
as moving forward a character), and then undo.

Another interesting data structure that pops up is the circular list for
"copy/paste".  In order to select a region in emacs, we manipulate what emacs
calls the "mark" (think of it as an anchor).  Press **C-&lt;space&gt;** to
drop the mark; the region is then the text between the mark and the cursor.
Many commands act on regions, such as the command to add to the circular list,
**M-w**.  The circular list is called a "kill ring" in emacs speak, and
**M-w** can be thought of as a copy command.  Its cousin, **C-w**, is more
like cut: it puts the selected region into the kill ring as well, but then
deletes it from the file.  Finally, the paste analogue ("yank", in emacs
speak; note that this means something *different* in vim) is **C-y**, which
will insert the current item from the kill ring.  To scroll through items in
the kill ring, first insert with **C-y**, and then traverse with **M-y**.
Many commands that you might expect to interact with the kill ring, such as
**C-k** to kill the region from the cursor to the end of the current line and
**M-&lt;blackspace&gt;**, will place their regions on the kill ring.

Customizing Emacs
-----------------

Emacs comes out of the box ready to go, but that does not mean that it is
perfect for you immediately.  It is very easy to customize emacs: since the
entire core of the editor is a Lisp interpreter, configuration happens in
Lisp.  (Trust me when I say that this is vastly superior to writing vimscript;
ask a vim user if you don't believe me.)  Plugins and extensions are numerous
and wonderful; I encourage you to explore and tweak settings in emacs to your
heart's content.  YOU DO NOT NEED TO KNOW LISP TO CONFIGURE EMACS.

In order to do that, though, I need to tell you where some things live.
(Non-unix users, you're on your own here; I don't know your preference storage
conventions.)  The core emacs configuration file lives at ~/.emacs by default,
though some users (like me) store it at ~/.emacs.d/init.el instead.  Both
work; do not do both, pick one.  Changing between them is easy (just move the
file).  This file is monolithic, though it can include other files because
Lisp.  However, you do not need to edit this file directly if you do not wish
to do so; instead, there is an interface invoked by **M-x customize** that
can handle this process for you.  (It has buttons and everything.  Try it if
you don't believe me!)

On beyond Z
-----------

As my usage of emacs has increased, my attachment to the keybindings has also
increased.  Fortunately, enough applications implement enough emacs keys that
most of the time I can use shortcuts without thinking.  (This is largely due
to readline, which is used in shells among other places, defaulting to "emacs"
keybindings.)  One particular offender is Firefox (or Iceweasel, if you're a
Debian like me), which uses more Windows-like bindings.  (Note here that the
emacs keybindings predate the *existence* of Windows by years, so they're not
"traditional" in any way.)  However, there exists an extension called
[Firemacs](https://addons.mozilla.org/en-US/firefox/addon/firemacs/) that aims
to bring these keybindings to the Mozilla browser.  If that's not enough,
there exists another browser called [Conkeror](http://conkeror.org/) which
attempts to bring the full emacs/vi experience to the Mozilla platform.
Chromium users are out of luck, but then, Chromium is barely customizable
anyway; Safari even less so.  And if you're using Internet Explorer: please
stop.

I'd like to finish this off by calling attention to some of the many
unexpected things that users can do with emacs.  Emacs comes bundled with an
email client (gnus), though there are two others available (mew and
wanderlust), and I use yet another (notmuch, which also has a vim and cli
interface).  There are several IRC clients: erc and rcirc, among others,
though there is also a weechat interface and a libpurple interface.  Emacs
will automatically reformat code for you with **&lt;tab&gt;**, and reflow text
to fit within your line length limits (mine are 78) with **M-q**.  **M-x
tetris** will help you waste time, as will **M-x dunnet** (a text-based
dungeon adventure game in the vein of Adventure and Zork), while **M-x
doctor** (an Eliza-like) will help you with your problems.  Emacs can split
itself into a client and server when launched with `emacs --daemon` and
connected to with `emacsclient`.  Emacs can edit remote files over a number of
protocols, including ssh, and contains a full-featured file browser capable of
descending into archives and editing them and the files they contain.  Emacs
is even hip to [modern humor](https://xkcd.com/378/): **M-x butterfly** is a
real command (I'll let you try it and see what it does with the promise that
it's not dangerous).

So does emacs have Buddha nature?  I'm not a Buddhist, but it really does have
everything else.
