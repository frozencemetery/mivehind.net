---
layout: post
---

I've been a Pidgin user since back in my Mac OS days (technically an Adium
user there, since it is possible with MacPorts to run true Pidgin on Mac OS,
but that's not especially important).  I remember how convenient it was when
Adium added IRC support, and I could finally move all of my chats into one
client.  And the closeness between Pidgin and the
[OTR Project](https://otr.cypherpunks.ca/) is reassuring.  With all that said,
this post intends to provide what I found to be missing information for
purposes of converting from a Pidgin setup into a
[Bitlbee](http://www.bitlbee.org/)+[Weechat](http://www.weechat.org/) setup
(though most of the information here is not Weechat-specific).

### Why?

First, it is never bad to have alternatives.  Having alternatives prevents
users from becoming locked in to a specific project, and in many cases when
there are multiple projects performing the same task, new functionality can be
added to both without too much trouble so long as licensing issues do not
arise.

Second (and this is most important to me), starting with version 3, pidgin
will be using libwebkit.  (You don't have to take my word for it; go try to
build the source tree without webkit installed if you don't believe me).  I
see this move as akin to using a jackhammer to crack walnuts: sure, it can be
done, but jackhammers are much better at other things, and there is likely to
be collateral damage induced.  The potential collateral damage I see is not
webkit specific; rather, I see problems with using *any* library of that level
of sophistication as problematic, given
[this list](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=webkit), which is
webkit-only.  I would be happier if some other engine were used (as I remain a
[Firefox](http://getfirefox.com/) user), but that doesn't solve the problem,
as [this list](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=gecko) (and to
a lesser extent
[this list](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=firefox)) show.
A chat to me is very different from (and much simpler than) a web page.

Finally, despite my initial excitement over the addition of IRC support, I've
found this support to be somewhat underpowered compared to traditional IRC
clients.  Your mileage may vary depending on what your IRC usage looks like;
I've met users perfectly happy with Pidgin's IRC support, and those who feel
constrained by it.

### Bitlbee setup

A quick note here: I'm working in [Debian](http://www.debian.org/) here, and
have not verified upstream defaults or defaults in other distributions.  So
when I say "by default", it should be taken to implicitly be "by default *in
Debian*.

That said, once Bitlbee is installed, it will start an IRC server running on
port 6667.  I suggest firewalling this off unless you are installing on a
server and plan to make it multi-user.

Bitlbee will also drop privs from this started service to the "bitlbee" user,
which is created on install.  You don't really need to do anything with this;
just know it exists.

A couple settings are worthy of attention in /etc/bitlbee/bitlbee.conf.
First, by default, bitlbee refers to the machine it's running on as
"localhost".  It claims to be able to do detection, but I expect this is
somewhat stunted by my firewall.  Anyway, this is controlled by the "HostName"
setting (so, for me, `HostName = kirtar`).

Next, if you're running bitlbee on the same machine as your IRC client as I
am, there's really no point in having client/server PING/PONG happen.  Your
client will connect to a local bitlbee instance, so giving it the ability to
ping out is somewhat nonsensical.  If that fits your use-case, set
`PingInterval = 0` and `PingTimeOut = 0`.

### Moving connections

I've been saved actually writing content here by the existence of the
convert_purple.py script.  It comes bundled with bitlbee-common.  An
invocation to it looks something like

```bash
/usr/share/doc/bitlbee-common/examples/convert_purple.py -f .purple
```

It will spit out a sequence of commands to send root on the bitlbee network to
add your existing non-IRC accounts.

More information on this can be found
[on the Bitlbee wiki](http://wiki.bitlbee.org/ConvertPurple).

IRC accounts will need to be added manually into your IRC client (here
Weechat), though this is likely not complex for most clients.

#### Weechat-specific notes

Many servers, when connected to using Weechat, will complain about an
incorrect dhkey size.  The size of dhkey it expects is controlled by the
parameter `irc.server.<servername>.ssl_dhkey_size`, where <servername> is the
name of the server in question.

### Moving OTR

This is the most fiddly and complex part of the process.  Unless you for some
reason need the OTR keys you generated using Pidgin (e.g., you authenticated
with someone you don't see on a regular basis), I highly recommend you skip
this step and just regenerate your OTR keys in Bitlbee.

More information on Bitlbee OTR can be found
[on the Bitlbee wiki](http://wiki.bitlbee.org/bitlbee-otr).  I will emphasize
that (as they say on the wiki page) OTR should never be offered on a remote
and/or public server, since it provides a false sense of security.

#### Moving OTR trusted fingerprints

The trusted fingerprints file is stored for Pidgin at
**~/.purple/otr.fingerprints**.  It is stored for Bitlbee at
**/var/lib/bitlbee/<username>.otr_fprints** (look for
**/var/lib/bitlbee/<username>.xml** to make sure <username> is set
correctly).  However, there are a number of important differences between
these files:

1. Pidgin stores resource information in this file; Bitlbee does not.
2. Pidgin names their protocols oddly: "prpl-jabber" instead of "jabber", for
   instance.
3. Bitlbee does not distinguish between "verified" and "smp" fingerprints; it
   calls them both "affirmed".

So I used some sed magic to convert this file.  You'll probably want something
like

```bash
sed ~frozencemetery/.purple/otr.fingerprints -e 's/\/kirtar//g' \
  -e 's/\/jeska//g' -e 's/prpl-//g' -e 's/smp/affirmed/g' \
  -e 's/verified/affirmed/g' > /var/lib/bitlbee/frozencemetery.otr_fprints
```

Note that "kirtar" and "jeska" are my XMPP resources; substitute your own if
needed.

#### Moving OTR private keys

This process is much harder to script.  Once again, pidgin stores private keys
at **~/.purple/otr.private\_key** (yes, it is singular), and Bitlbee stores a
similar file at **/var/lib/bitlbee/<username>.otr\_keys** (plural).  Once
again, there are some important differences between these files:

1. Pidgin stores resource information in this file; Bitlbee does not.
2. Pidgin names their protocols oddly: "prpl-jabber" instead of "jabber", for
   instance.

As a side effect of (1), if you *change* the resource at some point, you will
end up with *multiple* OTR private keys seemingly for the same account.  As a
result, it is not easily possible to script this process; some trial and error
will be required.

My suggested procedure here is this.  First, generate a private key for each
account using Bitlbee's OTR.  Then, in this file, replace each key with the
version from Pidgin.  Find a buddy and for each key, check that you have moved
the correct key (if there is only one such possibility, you have moved the
correct key).

### Conclusions

It is frustrating that for a protocol as nominally standardized as OTR, there
is so much variety in how key files are stored.  I picked Bitlbee for OTR
because it was the only non-Pidgin client I could find that correctly uses libotr
directly (Weechat-otr uses a scary pure-python OTR re-implementation,
and irssi-otr (same project as xchat-otr) was found to be very crashy in
practice with an annoying habit of gobbling a core for no discernible
reason), and it's also somewhat disappointing that other clients have this
much trouble.  Even Pidgin cores the machine while generating keys, which
Bitlbee does not do so.

I'm very happy with my new setup.  Not only did it satisfy my three reasons
for leaving Pidgin, but I can also now run my chat client without starting X,
should I desire such.  Hopefully this post is helpful to someone attempting a
similar task.  Thanks for reading!
