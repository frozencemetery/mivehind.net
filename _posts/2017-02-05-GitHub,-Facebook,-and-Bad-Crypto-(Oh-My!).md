---
layout: post
---

(If you were hoping for me to take potshots at OpenSSL, there will be none of
that this week.  As a single item, this is worse, and besides, I've been
having a very pleasant interaction with the OpenSSL developers.  Even if their
Contributor License Agreement process is just as irritating as any other CLA
process.)

GitHub decided to look at the problem of token recovery, and have decided on
[an approach](https://github.com/blog/2308-new-and-improved-two-factor-lockout-recovery-process).
Given the title and lead-in, you can probably can tell already that I'm not
happy about it.  And to their credit: this is a difficult problem, and the
mechanics are fiddly.  They've set up a bug bounty program for any
specification or implementation errors, but I have a bug right here that they
will pay me exactly $0 for, won't acknowledge, and won't fix.

**The bug is that this specification should never have been written, and this
protocol should never be implemented.**

Them's fightin' words, alright.  I can back this up.  Surprise: this is my
niche.  And speaking of which, it may surprise them to know that centralized
accounts, federated identity, and OTP (one time pad) tokens are all solved
problems.  And they're solved together, too, by the beast whose name I shall
now speak: Kerberos.  My puppy (at least in RPM-land).

I won't talk too much about Kerberos here, both because I already do that a
lot and also because the article at
[your local library](https://en.wikipedia.org/wiki/Kerberos_(protocol)) is
pretty good.  (It's also a bit of
[a mess](/2016/11/27/the-fall-of-journalism/).)  Suffice it to say: a protocol
providing strong cryptographic guarantees about authentication as well as
automatic establishment of a secure channel between any two servers without
ever passing user keys across the internet in any form.  It's older than I am,
which makes it unpopular with the startup world.

### Tokens

The motivation for this new process, it seems, is that fixing lost tokens is
"hard".  This is somewhat intentional, it turns out: one is supposed to guard
the token, and it is supposed to be difficult to reissue to harden against
attackers.  And as a user experience, this of course is suboptimal: a user's
phone burns out, and then whoops, they can't log in anymore.

To go off on another tangent for a moment: there are three types of two-factor
auth token which are relevant here.  The first is conceptually the simplest:
a time-locked SMS is sent to your registered phone number, and one types the
digits into the login form.  Fine as far as it goes, but it requires that any
potential adversary not also be able to eavesdrop on one's SMS communication
at any point.

The second is what we often call "hard tokens".  These are devices about the
size of my thumb (usually on a keychain) on which there is typically a
six-digit display and a button.  One pushes the button, and it displays a
series of numbers that the user then types into the login prompt.  This works
because the server has a notion of what the token's state is, and can confirm
their agreement.  This one is actually pretty good, but the tokens themselves
are not cheap.  In particular, since most users have smartphones, the hard
token is often replaced with an app (if you are using Google Authenticator
which is closed source, please switch to the open source
[FreeOTP](https://freeotp.github.io/)).  This increases the attack surface by
requiring that the device itself be trusted.  More on this in a minute.

The third is relatively new, and is associated with helpful acronyms like
"FIDO" and "U2F".  These are physical tokens that you insert into a USB port
port, push a button, and it performs an entire challenge-response handshake to
show existence of the token, and thereby provide a second factor.  Nifty,
except for the part where **the browser is talking to hardware directly
now**.  Also the part where Mozilla Firefox still refuses to implement it,
which is especially irritating in the modern web because while there is an
addon that provides the functionality, everyone wrote their detection scripts
based on `User-agent`.  Shame.

So, three types of tokens.  And if I've written this correctly, the intended
reaction is that U2F tokens should seem the clear winner, browser gunk
notwithstanding.  And that's not even wrong.  But here's the thing: while
writing this article, I realized that I have lost my U2F token.  And then I
realized that I haven't used this token since a couple weeks after its
acquisition, and therefore it isn't tied to any accounts.  But that itself is
interesting.  It turns out that the only times I would use this token are for
GitHub logins and social media logins: basically, anything with an account
that's tied to my name.  All three sites.

The three sites being, of course, GitHub, Facebook, and Twitter.  Facebook,
while having what looks like nice 2fa integration, I predominantly use on
mobile, so I can't enable a u2f token at all, and a software token will get me
nowhere because being the same device, it's not a second factor at all.
Twitter does not have 2fa integration at all as far as I can tell, but I don't
care because I also mostly use that on mobile.

And then there's GitHub.  See, they noticed that you can't use u2f on mobile,
and decided that the best course of action was to require another token be
present.  This puts the u2f token on an equal power level with the other
token.  To emphasize: this means that anything you could do with a u2f token,
you can also do with the software token (on the same device!  See above) or
SMS token (these are used in the recovery process, so still relevant).  I
reported this at launch of u2f integration, and received the nicest "we will
not be fixing this and would prefer not to talk to you" email I've gotten in a
while.

### Back on track

I read through their more
[in-depth announcement](https://githubengineering.com/recover-accounts-elsewhere/)
as well as
[the spec](https://github.com/facebookincubator/DelegatedRecovery/blob/master/draft-hill-delegated-recovery.raw.txt).
Predictably, I have some thoughts.

- Step four in the process (from the announcement) is "Contact GitHub
  Support.".  In particular, "GitHub Support can then use this information as
  part of a risk-based analysis to decide if proof of account ownership has
  been established in order to disable two-factor authentication.".  So this
  means that an *actual human* is involved in this process.  Which means the
  whole thing is vulnerable to social engineering, on top of the other things
  I'm going to say below.
  
- "Forcing users to everywhere use an email address has privacy implications,
  potentially allowing service providers to collude to track individuals'
  activity across many domains." (from the spec).  This would be a lot more
  genuine if it were not coming from *Facebook*, kings of the real names
  policy (for which, by the way, I still know people who have had difficulty
  registering under their real name).  And um... both GitHub and Facebook
  require an email address to be associated anyway.  Everything about
  "anti-tracking" coming from Facebook feels like honey through the mouth of a
  snake.

- They worry about analytics scripts leaking information in login pages.  I
  have a suggestion.  It's really lightweight.  In fact, it's negative code.
  And bear with me a moment, I know this is hard, but: *what if you didn't put
  analytics scripts on login pages?*
  
- Fundamental misunderstanding of authentication providers, especially
  federated ones.  They seem to believe that such systems came into exist
  fifteen years ago (I'm twenty-four right now, and you'll remember that
  Kerberos is older than me), that users are unwilling to disclose their
  identity to services (how will you do login without this?  Also, *you're
  Facebook*.), and that caching doesn't exist.
  
- This bullet point is just to re-emphasize the previous one.  Seriously,
  we're trusting these companies with our data.
  
- icon-152px.  This is a required (MUST) field in the JSON messages that are
  passed around on the wire.  It is indicated to be "The URL of a 152x152
  pixel PNG file representing the issuer".  It is never mentioned again.  Its
  purpose is not explained.  The only possible uses I can come up with are
  showing pretty graphics to the user (eww) or for actual human verification
  (TERRIFYING).  So some other questions: why 152?  Why does it need to be
  square?  Why a PNG?  What is a "pixel PNG"?  What does it mean to be
  "representing the issuer"?  Does it need to be blue and look like the
  [Fedora logo](https://getfedora.org/static/images/fedora_infinity_140x140.png)?
  Also: it's the URL of a page.  So there's now a mechanism to point clients
  at arbitrary URLs, which is fun.

- It's just OAuth.  They even call out their own protocol as a simplification
  of OAuth.
  
- Let me lose any friends I made with the previous point by saying that OAuth
  is terrible and that passing around bearer tokens as your authentication is
  just wrong.
  
- It is stated that "Facebook only stores a token with an encrypted secret
  that is associated with a Facebook account and does not become valid until
  it's used in a recovery." (announcement).  This is true, but... Facebook can
  just initiate a recovery at any time.  Sure, there'll be a paper trail, but
  if it means a compromised tarball gets uploaded to a project, that stops
  mattering.  Especially if they were compelled to not disclose such
  actions...

- Potshot: why does the announcement call out SQL injection specifically as
  something they're worried about in designing a protocol that has nothing to
  do with SQL?  Was there a security buzzword quota?

- "At no point does GitHub exchange any personally identifiable information with
  Facebook. Likewise, Facebook does not exchange any personally identifiable
  data with us."  As far as I can tell, this is either a grave
  misunderstanding or an outright lie.  The identity information that they
  claim worry over *is passed around*; your identity is verified by Facebook
  to GitHub.
  
- Putting a "privacy-policy" field in your wire protocol does not fix this,
  and is also perplexing.  Is the browser supposed to do something with this?

- There was explicitly "No public review".  You ask us to trust your crypto,
  but won't let us help design it.  Supposedly, it was created by "someone
  well versed in this area".  The specification says Brad Hill of Facebook,
  who I am sure is a great person, but who has according to the internet never
  implemented anything cryptographic before.  The announcement also states
  that it was "reviewed by numerous experts in the field".  Who are unnamed,
  and do not appear on said specification.
  
- Are they going to make an RFC out of this?  It's formatted like they are,
  but I can't imagine this would get past the IETF through anything other than
  force of personality.  Maybe they just wanted to experience the joys (no) of
  writing SGML for xml2rfc?  If so, I will tell you for free: it is real bad.
  Don't write XML.
  
- So why was there no public review?  Since they won't say, I can think of
  only two reasons.  The first is that they honestly didn't know any better,
  which is somewhat sad, but that's the best I can do in order to keep good
  faith.  Because if I *don't* assume good faith, we're left with them not
  *wanting* outside input.  Concerns like: making sure no one else does it
  first, making sure no one tells you to use existing protocols and
  technologies before you roll it into production, making sure their
  implementation is the final authority, hiding artificial weaknesses (Dual
  EC-DRBG anyone?), and so on.  And I have to assume good faith.

- "GitHub values the security of our users' accounts" I don't believe you.
  Well, that's not quite true: I think you value maintaining users, and
  account security is taking a backseat to slick web interfaces and
  Not-Invented-Here.

- "We're also planning to support reciprocal Facebook account recovery in the
  near future."  Utterly terrifying.

### Final thoughts

Okay.  I had queued a post about how everyone keeps making free-software
GitHub clones, and what a monumental waste that is, but that's going to have
to wait.  I haven't changed my mind on it, but I can see much more clearly
what people are worried about with a proprietary provider, and it needs to be
edited for tone.  (Then again, what do I write that *doesn't*?)

<h4>So, this is I guess an open invitation.  If your identity model would be
improved by using Kerberos, by having a CA, the use of one- and two-way
trusts, single sign on, and the like: I will ssh into your box and run
`ipa-server-install` for you.</h4>

[And then you too can have those things.](http://www.freeipa.org/) And not
have to write more code or worry about doing wrong any of the things that went
wrong here.  And if encounter bugs, I will (be part of the group that will)
fix them for you.  Because that's how software project ecosystems work, done
right.  Not a vacuum.
