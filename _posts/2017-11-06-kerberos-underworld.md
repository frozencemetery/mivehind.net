---
title: Kerberos (from the underworld up)
tags:
  - tech
---

This is adapted from a talk I gave to MIT's computer club,
[SIPB](https://sipb.mit.edu/).  Slides are
[here](http://mivehind.net/kerberos.odp), and they have pretty pictures, but
your choice: I use slides as a visual aid, not as notes for what's going on.

## What is Kerberos, and how does it work?

> "Kerberos is a network authentication protocol. It is designed to provide
> strong authentication for client/server applications by using secret-key
> cryptography. A free implementation of this protocol is available from the
> Massachusetts Institute of Technology."
>
>     https://web.mit.edu/kerberos

Kerberos is a security software system.  When applications use it, Kerberos
provides authentication guarantees (we'll define that more further down).  It
also offers strong encryption.  This encryption is most commonly based on
passwords, but can also be backed by public keys (i.e., certificates and/or
smart cards) and OTP tokens.

Kerberos consumes very few resources: most operations it performs are AES.
This means, firstly, that it is quite fast: AES is implemented in hardware on
most x86_64 CPUs since 2008 (and is now on some ARM CPUs as well).  But it
also means that the server requirements are fairly low: a single KDC (Kerberos
Domain Controller; the machine that runs everything) machine can service
thousands of clients easily.

It's also pretty easy to use, and I will definitely get into that further
down.  Finally, if you're me, the mythology references are good for a smile
every now and then.

## What really happens when I `kinit`?

Superficially, very little:

```
rharwood@seton:~$ kinit
Password for rharwood@REDHAT.COM: 
rharwood@seton:~$ 
```

(where seton is, of course, my local machine).  Under the hood, though,
several things happen there:

- seton sends a message to the KDC (called an AS-REQ, since it is an
  Authentication Server REQuest) for rharwood@REDHAT.COM.
  
- Typically, the KDC replies with `KRB5KDC_ERR_PREAUTH_REQUIRED` - this means
  that the client needs to complete one of the (specified) challenges in order
  to prove their identity.
  
- At this point, `kinit` needs my password in order to complete said
  challenges, so it asks for it, and let's assume I type it correctly.
  
- seton completes the challenge, and attaches the result to an AS-REQ, which
  it sends to the KDC.
  
- The KDC replies (AS-REP, by analogy) with an encrypted credential for
  rharwood@REDHAT.COM
  
- seton decrypts and stores the credential.

(Note: the first two steps can be skipped if the machine acquiring credentials
already knows what the challenges are, which could happen if it had acquired
credentials recently.)

Alright, so it stores the credential.  Where?

```
rharwood@seton:~$ klist
Ticket cache: KEYRING:persistent:21259:krb_ccache_1PTtjIL
Default principal: rharwood@REDHAT.COM

Valid starting       Expires              Service principal
10/03/2017 22:32:14  10/04/2017 08:32:14  krbtgt/REDHAT.COM@REDHAT.COM
rharwood@seton:~$ 
```

This being my Fedora machine, it is stored in the kernel keyring.  21259
happens to be my uid on this system.  rharwood is of course me, and the
@REDHAT.COM part means that we're working with the REDHAT.COM realm (which has
specific KDC(s) and service(s) associated with it).

What's with the `krbtgt/REDHAT.COM@REDHAT.COM` thing though?  Well,
predictably it's a service principal.  Service principals look different than
user principals: instead of a username (like rharwood), typically they have a
'/' which separates the service (here, krbtgt) from where it's operating.  So
this indicates that I (rharwood) have a ticket (authorization) for
REDHAT.COM's "krbtgt" service.

What's krbtgt?  Hold that thought, I need to define more terms.

## How does Single Sign-On Work?

Single Sign-On (SSO) systems are those which enable a single user identity to
connect to multiple services.  The easiest example is probably websites that
allow you to sign in with your account from elsewhere ("sign in with...") as
opposed to creating a standalone account with that website specifically.

So how does this work in Kerberos?  Let's look at a different realm, this time
for Fedora development:

```
rharwood@seton:~$ kinit rharwood@FEDORAPROJECT.ORG
Password for rharwood@FEDORAPROJECT.ORG: 
rharwood@seton:~$ 
```

Specifically, I'm going to show the BrewKoji service.  This manages building
packages in Fedora for all architectures across a variety of build machines.
Like pretty much all the rest of the Fedora infrastructure, it uses Kerberos.
It also has a CLI, which makes it good for demonstration purposes, that
connects to the RESTful HTTP interface.  The `hello` command just asks it to
greet me, rather than actually performing an action:

```
rharwood@seton:~$ koji hello
hallo, rharwood!

You are using the hub at https://koji.fedoraproject.org/kojihub
Authenticated via GSSAPI
rharwood@seton:~$ 
```

but it clearly identified me.  And if we `klist`, there's change there too:

```
rharwood@seton:~$ klist
Ticket cache: KEYRING:persistent:21259:krb_ccache_MVuahmP
Default principal: rharwood@FEDORAPROJECT.ORG

Valid starting     Expires            Service principal
10/04/17 03:04:06  10/05/17 03:03:12  HTTP/koji.fedoraproject.org@FEDORAPROJECT.ORG
 renew until 10/11/17 03:03:12
10/04/17 03:03:21  10/05/17 03:03:12  krbtgt/FEDORAPROJECT.ORG@FEDORAPROJECT.ORG
  renew until 10/11/17 03:03:12
rharwood@seton:~$
```

So the krbtgt service ticket is present as expected from the `kinit`, but we
have a new service (for Koji): the HTTP service on koji.fedoraproject.org.
Let's walk through how we got there.

- First, my machine (seton) connected to koji.

- koji asked seton to identify my user with GSSAPI (which ends up being
  Kerberos; GSSAPI almost always is a Kerberos wrapper).
  
- seton asked the KDC for a service ticket for koji.  This is called a
  TGS-REQ - a request of the Ticket Granting Service.  As the name suggests,
  the Ticket Granting Service is itself a Kerberos service, which is where the
  krbtgt service ticket comes in: it's a ticket for that service, a Ticket
  Granting Ticket, or TGT.
  
- Based on the TGT, the KDC sends an (encrypted) service ticket to us.  This
  is called a TGS-REP.
  
- seton decrypts the service ticket.

- seton uses the ticket to prove to koji that I am me - that is, that the
  connection is authoratatively from rharwood@FEDORAPROJECT.ORG.
  
- koji picks a language (could be one of several here) and greets me.

## Authentication and Authorization

It's important to note that a successful *authentication* to the koji service
(or to any other service) does not imply successful *authorization*.  The two
are distinguished thus: *authentication* associates a session to a name (here,
my connect to koji with rharwood@FEDORAPROJECT.ORG)¸ while *authorization*
dictates what a name can do (rharwood@FEDORAPROJECT.ORG is authorized to
perform builds of the krb5 package, for instance).

Authentication can be performed, for example, based on passwords, or
public/private keypairs, or bearer tokens (like in OAuth: tokens which state
that the bearer authoritatively is a specific person, but must be presented in
their entirety for checking.  If these sound terrible it's because they are).

Authorization usually takes the form of rules (or rule lists), like sudoers
rules, or file permissions, or the policykit/logind session authorizations.

Kerberos is an authentication system.  Authorization must come from elsewhere;
typically it varies service-to-service, but in large scale setups it is often
backed in LDAP.

Kerberos is not an authorization system.  krb5 provides hooks in several
places for authorization to occur, but fundamentally, authorization is
something that one adds elsewhere (e.g., in LDAP; possibly even the same
backing store that a running krb5 is using).

More concretely, this means that an error like:

```
rharwood@conch:~$ touch foo
touch: cannot touch `foo': Permission denied
rharwood@conch:~$ 
```

is an authorization error, because (let's assume we're running on
[AFS](https://en.wikipedia.org/wiki/Andrew_File_System#Available_permissions),
though the details aren't extremely important except inasmuch as it has both
an access control list for directories and Kerberos integration):

```
rharwood@conch:~$ fs la .
Access list for . is
Normal rights:
  system:anyuser l
  rharwood.admin rlidwk
  rharwood rlidwka
  rharwood.mail rl 
rharwood@conch:~$
```

But wait!  I said this was an authorization error, but it looks like I'm on
the authorized list (rlidwka is all permissions).  What's up with that?

The missing piece is the linking of me, system user rharwood, with AFS's
concept of user rharwood.  We are missing the association between *name* and
*identity*.  So:

```
rharwood@conch:~$ kinit
rharwood@CLUB.CC.CMU.EDU's Password:
rharwood@conch:~$ aklog
rharwood@conch:~$ touch foo
rharwood@conch:~$ 
```

`kinit`, as before, acquires me a TGT.  And then `aklog`, which is a service
much like koji above, acquires a service ticket for AFS.  AFS can then use
this service ticket to associate my user session with AFS user rharwood, and I
can manipulate my homedir freely.

More specifically:

```
rharwood@conch:~$ tokens
Tokens held by the Cache Manager:

User's (AFS ID 1812) tokens for afs@club.cc.cmu.edu [Expires Oct  4 09:42]
   --End of list--
rharwood@conch:~$ klist | grep afs
Oct  3 23:42:44 2017  Oct  4 09:42:42 2017 afs/club.cc.cmu.edu@CLUB.CC.CMU.EDU
rharwood@conch:~$ 
```

which is to say - AFS has a token that indicates I am authorized as rharwood,
and we've acquired a service ticket for afs in the club.cc.cmu.edu cell in the
CLUB.CC.CMU.EDU realm.

If it seems redundant to have "club.cc.cmu.edu" in there twice (albeit with
different casing): check this out.

## Cross-realming

```
rharwood@conch:~$ aklog athena.mit.edu
rharwood@conch:~$ 
```

Excuse me?

```
rharwood@conch:~$ tokens
Tokens held by the Cache Manager:

Tokens for afs@athena.mit.edu [Expires Oct  4 09:55]
User's (AFS ID 1812) tokens for afs@club.cc.cmu.edu [Expires Oct  4 09:42]
   --End of list--
rharwood@conch:~$ klist | grep -i mit
Oct  3 23:56:16 2017  Oct  4 09:55:23 2017 krbtgt/ATHENA.MIT.EDU@CLUB.CC.CMU.EDU
Oct  3 23:56:16 2017  Oct  4 09:55:23 2017 afs/athena.mit.edu@CLUB.CC.CMU.EDU
Oct  3 23:56:16 2017  Oct  4 09:55:23 2017 afs/athena.mit.edu@ATHENA.MIT.EDU
rharwood@conch:~$ 
```

What I've done here is acquired an AFS credential for use in another realm.
(I picked ATHENA.MIT.EDU because this presentation was originally given to
MIT students.)

As before, this has two parts: the token cache manager has a AFS credential
(which looks different, because it's not my "home" cell), and some service
tickets.  The service tickets are the really neat part, though.  First, I have
a TGT for ATHENA.MIT.EDU in CLUB.CC.CMU.EDU - this means that I have license
to ask the CLUB.CC.CMU.EDU KDCs for tickets to the ATHENA.MIT.EDU realm on my
behalf.  And then the other two are service tickets for the athena.mit.edu AFS
cell - one of which is from the ATHENA.MIT.EDU realm, and issued using that
new TGT.

This has been accomplished using a *cross-realm* trust: the administrators of
the ATHENA.MIT.EDU realm have an agreement with us at CLUB.CC.CMU.EDU, and
have exchanged keying material, that makes this possible.  Many other AFS
cells have a similar setup, which means that AFS can easily be used for global
data sharing: user@mit.edu can grant user@club.cc.cmu.edu permissions to their
directory, and user@club.cc.cmu.edu can access away.

## Multi-realming

Many users (especially those with a separate test and dev environment) will at
some point need to simultaneously hold credentials for two realms at once.  I
encounter one at work:

```
rharwood@seton:~$ kinit rharwood@FEDORAPROJECT.ORG
Password for rharwood@FEDORAPROJECT.ORG:
rharwood@seton:~$ kinit rharwood@REDHAT.COM
Password for rharwood@REDHAT.COM:
rharwood@seton:~$ koji hello
안녕하세요, rharwood!

You are using the hub at https://koji.fedoraproject.org/kojihub
Authenticated via GSSAPI
rharwood@seton:~$ 
```

So right now, if we look at our ccache, we should have a service ticket for
koji in the FEDORAPROJECT.ORG realm, right?

```
rharwood@seton:~$ klist
Ticket cache: KEYRING:persistent:21259:krb_ccache_aLv5gM5
Default principal: rharwood@REDHAT.COM

Valid starting     Expires            Service principal
10/04/17 14:59:32  10/05/17 00:59:32  krbtgt/REDHAT.COM@REDHAT.COM
rharwood@seton:~$
```

Where is it?  Well, in krb5, credentials can be stored in what are called
collections: multiple ccaches grouped together.  By default, `klist` only
shows the ccache information corresponding to the default principal - and
since rharwood@REDHAT.COM `kinit` last, it's the current default.

Fortunately, we can easily ask it for more:

```
rharwood@seton:~$ klist
Ticket cache: KEYRING:persistent:21259:krb_ccache_aLv5gM5
Default principal: rharwood@REDHAT.COM

Valid starting     Expires            Service principal
10/04/17 14:59:32  10/05/17 00:59:32  krbtgt/REDHAT.COM@REDHAT.COM

Ticket cache: KEYRING:persistent:21259:krb_ccache_eeQRbHv
Default principal: rharwood@FEDORAPROJECT.ORG

Valid starting     Expires            Service principal
10/04/17 14:59:45  10/05/17 14:59:17  HTTP/koji.fedoraproject.org@FEDORAPROJECT.ORG
        renew until 10/11/17 14:59:17
10/04/17 14:59:22  10/05/17 14:59:17  krbtgt/FEDORAPROJECT.ORG@FEDORAPROJECT.ORG
        renew until 10/11/17 14:59:17
rharwood@seton:~$
```

and it pops right out.  Modern version of krb5 will perform the realm
selection automatically, and users shouldn't have to worry about it.

## Who uses Kerberos?

Well, hopefully you soon!

We've already talked about filesystems (like AFS; NFS as well), but there are
plenty of other consumers, such as: SSH, Web logins (either using SAML
portals, or with Apache or Nginx modules), REST endpoints, databases, and the
list goes on.  That'll happen when your technology has been around a while!

And there are three major implementations of Kerberos widely used today:
Microsoft's, as part of Active Directory; Heimdal Kerberos, standalone and
part of macOS Server; and MIT krb5, either standalone, part of
[Samba](https://www.samba.org/), or part of [freeIPA](http://freeipa.org/).
Readers who have made it this far can probably guess that I favor the MIT
implementation, which is the most actively developed these days.

But let's focus on using it for right now.  Kerberos is best experienced using
an interface we call the GSS-API (or GSSAPI, for "short").  Let's go to an
example.

### python-gssapi

As part of the [python-gssapi](https://github.com/pythongssapi/python-gssapi)
project, we have written a sandbox tool called
[gssapi-console](https://github.com/pythongssapi/gssapi-console).  It stands
up a full test krb5 environment for your own testing or enjoyment.  Check it
out:

```
rharwood@seton:~$ gssapi-console.py
GSSAPI Interactive console
Python 2.7.14 (default, Sep 17 2017, 18:50:44) 
[GCC 7.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information about
Python.

Functions for controlling the realm are available in `REALM`.
Session: /tmp/tmpszYOsC-krbtest
Mechansim: krb5 (MIT Kerberos 5), Realm: KRBTEST.COM, User: user@KRBTEST.COM, Host: host/seton.mivehind.net@KRBTEST.COM
>>> 
```

gssapi-console has set us up with a ccache containing credentials for
user@KRBTEST.COM, and a keytab with credentials for
host/seton.mivehind.net@KRBTEST.COM (this name will vary depending on your
hostname, of course).  This lets us do both the client side of a connection as
well as the server side.

Most of the time, the client sends first.  And to send, it needs to know the
identity of the recipient.  GSSAPI expresses this as a name, which is nothing
fancy - we've already seen it.

```python
>>> server_name = gssapi.Name("host/seton.mivehind.net")
>>> 
```

Look at that, our first GSSAPI call!  We've created a name that represents the
server we're going to connect to.

```python
>>> client_context = gssapi.SecurityContext(usage="initiate", name=server_name)
>>> server_context = gssapi.SecurityContext(usage="accept")
>>> 
```

For purposes of this example, the client and server are on the same machine
(so that I don't have to show socket code...), but of course in the real
world, they're usually separated.  Anyway, using the name object we just made,
we set up connection contexts for the client and sever, separately.

Now, for the actual handshake, the client and server pass a token back and
forth.  Usually this would of course be across a network, but:

```python
>>> token = client_context.step()
>>> token = server_context.step(token)
```

We keep passing back and forth until there is no new token to pass:

```python
>>> token is None
False
>>> token = client_context.step(token)
>>> token is None
True
>>> 
```

at which point the negotiation is complete:

```python
>>> client_context.complete
True
>>> server_context.complete
True
>>> print server_context.initiator_name
user@KRBTEST.COM
>>> 
```

Altogether, the connection setup code looks like this:

```python
>>> server_name = gssapi.Name("host/seton.mivehind.net")
>>> client_context = gssapi.SecurityContext(usage="initiate", name=server_name)
>>> server_context = gssapi.SecurityContext(usage="accept")
>>> token = client_context.step()
>>> token is None
False
>>> token = server_context.step(token)
>>> token is None
False
>>> token = client_context.step(token)
>>> token is None
True
>>> client_context.complete
True
>>> server_context.complete
True
>>> print server_context.initiator_name
user@KRBTEST.COM
>>> 
```

Again, in a real program, we'd be sending `token` across a network connection,
but otherwise this is exactly what this looks like.  We'd probably also want
to do some authorization checking on the initiator (i.e., the client), but we
have that information right there!

Now let's use it for something.  Cryptography is cool these days, right?

```python
>>> message = "I'm the best possible message!"
>>> encrypted_message = client_context.encrypt(message)
>>> encrypted_message
'\x05\x04\x06\xff\x00\x00\x00\x00\x00\x00\x00\x00\x1fb\xec\xfb\xc1\x91\xf5\x8c\x87\x94\x9f\x925\xf4\xda\xe0\x8d\x86}!9\x80\xa04\xf4<\xb4\xa4n!p\x0b\xc4v}8\x9e+[\x94\xfe\xb3.~\xa3\x80]m\xc2T\x15\xc2\xff\x18\x95\xce^\xb3\x86\xec\xf8\x99\xdd9\xc8!\xa4\x85WB)\x1b@"\xa0Jqc'
>>> server_context.decrypt(encrypted_message)
"I'm the best possible message!"
>>> 
```

It bears mentioning that we get this *for no additional cost* after our
authentication handshake.  Once the contexts are established, not only are the
client and server authenticated to each other, but they're ready to pass
encrypted messages back and forth.  And while visual inspection doesn't
*prove* that the message has been encrypted, I'm going to assert that it is
(AES/sha2, for the curious).  Again, client and server would most likely be
operating on separate machines in the real world, so it's safe to pass
`encrypted_message` across the network between them.

### libgssapi

The C interface (libgssapi) is very similar, though, being C, it's more
verbose.  The concepts map fairly directly between the two, though.  Remember
that since our client sends first, it is the "initiator", while the server is
the "acceptor".

- First, the client imports the server name - this is a call to
  `gss_import_name()`.
  
- Next, the client calls `gss_init_sec_context()`, which simultaneously sets
  up the client context and produces a token.
  
- The token passes across the wire to the server, which calls
  `gss_accept_sec_context()`.  Similarly, this sets up the server context, and
  *may* produce a token.
  
- Any further token exchange is passed through `gss_init_sec_context()` and
  `gss_accept_sec_context()` in the same way until there are no more tokens.
  
- At this point the contexts are fully established.

In both the Python and C interfaces, there are of course other functions that
can be called, and options that can be set, but they aren't necessary most of
the time (and certainly not for demo purposes).

For encryption, we call `gss_wrap()`, and `gss_unwrap()` (for decryption).

## Links

- MIT krb5 can be downloaded from your distribution,
  [their website](https://web.mit.edu/kerberos), or in development on
  [GitHub](https://github.com/krb5/krb5).
  
- python-gssapi is developed on
  [GitHub](https://github.com/pythongssapi/python-gssapi), as is
  [gssapi-console](https://github.com/pythongssapi/gssapi-console).  Both can
  also be downloaded from PyPi using pip.
  
- freeIPA can be found in most distributions,
  [its website](http://freeipa.org), or in development on
  [GitHub](https://github.com/freeipa/freeipa).
  
- Samba can be found in some distributions, or from
  [its website](https://www.samba.org).
