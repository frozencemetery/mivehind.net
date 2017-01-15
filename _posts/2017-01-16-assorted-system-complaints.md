---
layout: post
---

There are two threads I want to pursue here:

### First sequence

To demonstrate this sequence of sadness, I need a user in a group.
Arbitrarily (by which I mean, as everywhere, not arbitrarily at all) I pick
myself and the audio group:

```bash
frozencemetery@kirtar:/tmp$ groups | tr ' ' '\n' | grep audio 
audio
```

I also need a user who is not myself to own this directory that I make, so I
pick mpd (again, not arbitrary at all):

```bash
frozencemetery@kirtar:/tmp$ ls -ld test
drwxrwxr-x. 2 mpd audio 40 Jan 15 15:25 test
```

And we make a file in said directory:

```bash
frozencemetery@kirtar:/tmp$ touch test/file
frozencemetery@kirtar:/tmp$ ls -l test/file
-rw-r--r--. 1 frozencemetery frozencemetery 0 Jan 15 15:46 test/file
```

So the first observation is that I can change the user and group on the file,
except when such would result in giving it away:

```bash
frozencemetery@kirtar:/tmp$ chmod g+rw test/file
frozencemetery@kirtar:/tmp$ chgrp shadow test/file
chgrp: changing group of 'test/file': Operation not permitted
frozencemetery@kirtar:/tmp$ chgrp audio test/file
frozencemetery@kirtar:/tmp$ chown mpd test/file
chown: changing ownership of 'test/file': Operation not permitted
frozencemetery@kirtar:/tmp$ sudo chown mpd test/file
[sudo] password for frozencemetery: 
frozencemetery@kirtar:/tmp$ ls -l test/file
-rw-rw-r--. 1 mpd audio 0 Jan 15 15:46 test/file
```

which is irritating, but not fatal except when both the target user and my
operational user do not share a group.

Next, I play with adjusting metadata.  Some time shenanigans:

```bash
frozencemetery@kirtar:/tmp$ touch test/file
frozencemetery@kirtar:/tmp$ touch -t 201601010000 test/file
touch: setting times of 'test/file': Operation not permitted
```

So when I only have group access to a file, I can set its last access time to
now, but not any other time.  This is irritating, because I can do this just
fine:

```bash
frozencemetery@kirtar:/tmp$ rm test/file
removed 'test/file'
frozencemetery@kirtar:/tmp$ touch test/file
frozencemetery@kirtar:/tmp$ touch -t 201601010000 test/file
```

though of course that results in

```bash
frozencemetery@kirtar:/tmp$ ls -l test/file
-rw-r--r--. 1 frozencemetery frozencemetery 0 Jan  1  2016 test/file
```

The reason for this is, per the man page:

> Changing timestamps is permitted when: either the process has appropriate privileges, or the effective user ID equals the user ID of the file, or times is NULL and the process has write permission for the file.
>  -- utime(2)

The error I want people to find this from is:

> rsync: failed to set times on "/path/name": Operation not permitted (1)

and the solution is to run the `rsync` command as the user who owns the path.

I discovered this by having my audio directory be `mpd:audio` and `ug+rwX`,
and then trying to `rsync` it around from my user (in the "audio" group).
This works, up until `rsync` needs to update times.  Then it will fail to
update the times, which seems harmless until one notices that it is copying
the files that need updating at every sync.

### Second sequence

For reasons I won't go into here, I needed to update from ESR firefox to
stable firefox.  This involves, as per usual, several irritating changes to my
setup.  This time, the update brings with it gtk3, which is my least favorite
change that I can remember.  Part of this is due to firefox being the first
major gtk3 application on my system, and I'll have my share of gtk3 complaints
in a moment, but some of the changes here are on firefox.

For instance: some themes that work with other applications (read:
virt-manager) do not work with firefox.  I do not know why.  Firefox also does
not respect the `gtk-application-prefer-dark-theme = true` setting in
**~/.config/gtk-3.0/settings.ini**.

Also, the absolute winner for most frustrating thing: it does not render
bitmap fonts anymore.  Support was explicitly removed.  So I had to convert my
bitmap font to a TTF, which it will render.  And occasionally it looks
terrible.

But I need to heap - and I really do mean heap - blame onto gtk3 here.  The
theme interface is not backward compatible with gtk2, which is well-known.
What is perhaps less well-known is that the interface isn't stable.  Themes
that worked with an older minor version of gtk3 will not necessarily work with
newer versions.  In particular, I have run into problems with menu rendering,
especially around spacing and highlighting.  The result is that I have found
two themes that work *at all* (by which I mean: no obvious rendering errors,
working in firefox, and dark): Arc-Dark (which I'm currently using) and
Breeze-Dark (which is extremely similar; they're both blue-on-black).

I miss the
[Nodoka variant](http://www.club.cc.cmu.edu/~rharwood/tmp/2014-07-22-225012_1920x1080_scrot.png)
I [made](https://gist.github.com/frozencemetery/3968411), mostly.

There are of course other issues I have with gtk3, but needing to set two
values in a config file is not the end of the world, especially considering
how poorly configured many desktop defaults on Linux are these days.

