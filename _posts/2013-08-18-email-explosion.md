---
layout: post
tags:
  - tech
---

Recently, I stopped being able to read mail sent to my CClub email address on
my local machine.  This was problematic, since I receive more than half of my
email on this address, and rely on my local email client to handle it
efficiently.  All programs involved were extraordinarily unhelpful about what
was wrong, though I have now solved the issue.  Here's how.

### My Local Email Setup ###

My email client is [notmuch](http://notmuchmail.org/) (specifically, the emacs
interface).  It is a tag-based client that reads local maildirs.  To deliver
these maildirs, I used offlineimap to transfer the email over secured
(kerberized) IMAP.  To send outgoing mails, notmuch/emacs hands off to
[msmtp](http://msmtp.sourceforge.net/), again secured with the GSSAPI.  The
`offlineimap && notmuch new` sequence was run as a cronjob (with errors not
being discarded).

### Remote Email Setup ###

CClub has three servers configured round-robin for SMTP, one of which doubles
as the IMAP server.  Because it was the standard at the time the machine
setups were designed, they all run qmail for MTA, and the IMAP server runs
Dovecot, configured to serve IMAP.  Delivered mail is stored in the user's
home directories (at `~/Maildir`), which are located in
[AFS](https://en.wikipedia.org/wiki/OpenAFS) (recalling that the initial 'C'
in "CClub" stands for for "CMU"), unless the user chooses to forward their
email to another address (which I have purposefully not done, though almost
all other users do).

### Failure Mode ###

I noticed that something was wrong when people started mentioning emails to
lists that I was on that, somehow, I had not seen.  I tested sending mail from
my CClub account to another account, and that worked without trouble;
offlineimap had not been throwing any errors, either.  At some point in
disbelief that I hadn't gotten any new emails in days, I ran notmuch by hand,
expecting that it had ignored files.  In the process, I ran offlineimap by
hand as well, and noticed that it was taking a long time (upward of 40
minutes) to sync my email.  And after those 40 minutes, why, I still had no
new mail.  I ran it again as verbosely as possible, and nothing peculiar
caught my eye; every so often, it would append "Hang in there!" to a string,
and that was about it.  Eventually it would exit.  With no new messages.

At this point, I picked up the lead pipe labeled "root" and started swinging.
I waded into the jungle of the IMAP server, wishing all the while I had a
machete instead of a pipe.  The first casualty was kern.log, where I
discovered many entries that looked like

>Jul 16 04:37:30 hostname kernel: afs: Tokens for user of AFS id 0 for cell our.cell.addr have expired

Or rather, I would have, had I gone to kern.log first, and not used `dmesg`.
`dmesg` doesn't show the timestamps, you see.  Once it was decided that those
were irrelevant, I went after dovecot.log.  Except that there was more than
one.  This isn't out of the ordinary, but... maybe it's better if I show what
I saw.

```bash
imap:/var/log# ls -lh dovecot*
-rw------- 1 root root  18M 2013-07-16 05:01 dovecot.log
-rw------- 1 root root  53M 2013-07-07 00:55 dovecot.log.1
-rw------- 1 root root 8.5M 2013-05-17 21:06 dovecot.log.2.gz
-rw------- 1 root root 9.3M 2011-09-14 09:32 dovecot.log.3.gz
```

I opened up dovecot.log first, and it was full of

> dovecot: 2013-07-07 03:26:02 Error: IMAP(myusername): rename(/afs/club/usr/myusername/Maildir/new/number.othernumber.imaphost, /afs/club/usr/myusername/Maildir/cur/number.othernumber.imaphost:2,) failed: File too large

`tail -f` while I connected with offlineimap showed first that the kern.log
entries were unrelated, and second that the spew of errors into dovecot.log
happened every time I attempted to download my messages.

I looked at a random one of these messages (7k in size), and verified that
dovecot was set to allow files this large (it was).

### What Went Wrong ###

This is the command that finally explained everything.

```bash
root@imap:/afs/club/usr/myusername/Maildir/cur$ ls | wc -l
31706
```

So why is that a problem?  Well, looking at a random assortment of entries in
that directory, they're all about 31-35 characters in filename length.  The
problem, as spelled out on
[this post](https://lists.openafs.org/pipermail/openafs-info/2010-August/034177.html)
to the OpenAFS mailing list, is that there are too many files in this
directory.

If you're reading this and are worried about how many files your mail
directory is taking up on disk, don't be.  I looked.  If you're using a modern
file system that's not AFS (including ext3, ext4, btrfs, and a number of
others), realistically the files per directory maximum is not something that
is likely to be hit.  Of course, my words should be taken with caution here,
for the AFS developers likely said the same thing about AFS.

### Resolution ###

The key to keeping this from happening again is to stop storing mail on the
imap server.  This means deleting messages as they are downloaded.
Unfortunately, offlineimap does not support this.  Fortunately,
[getmail](http://pyropus.ca/software/getmail/) does.  And it's even easier to
configure.  (Side note: when I ran `getmail` for the first time against the
CClub IMAP server, it *immediately* told me that something was wrong with the
server, which offlineimap had never done.  So maybe it wasn't so unfortunate
that I had to switch after all.)

Unfortunately, getmail would only download a few messages before the server
offered it messages that it couldn't deliver (because it had to "rename" them
from new to cur), and would spew errors to dovecot.log before exiting again.
I'm sure there's a more elegant solution than what this, but I just ran
getmail in a loop all night until it had downloaded all of the messages.  Five
minutes after I woke up, it finally finished.  (Remember, I had ~32,000
messages in just the cur directory.)  Then I cleared the directories on the
imap server.

I won't go too deeply into the notmuch side of the fix; I've written the steps
needed on the [notmuch website](http://notmuchmail.org/howto/#index6h2)
already (section "Automatically retagging the database").

And if nothing else, I now have can relate the one case where the system
designer should have used mbox instead of maildir.
