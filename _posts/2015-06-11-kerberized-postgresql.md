Charlie recently wrote an
[excellent post](https://charlietechnotebook.wordpress.com/2015/06/10/kerberize-mariadb-and-enable-sqlalchemy-to-talk-to-mariadb-via-pythonon-centos-7-0/)
on Kerberizing mariadb and talking to it with SQLAlchemy.  This is using RPMs
I've constructed for development and as such contain code not yet upstream,
but once it is completed (I need to write the encryption part) will become
widely available.

I think this is great news for anyone running mariadb in a situation where
Kerberizing is helpful (such as OpenStack), but I want to speak to something
related: what about PostgreSQL?

# Towards a Fully Kerberized PostgreSQL

Adam has previously written on
[Kerberizing Postgres for Keystone](http://adam.younglogic.com/2013/05/kerberizing-postgresql-with-freeipa-for-keystone/)
and this post depends on that work.  However, his post is more focused on the
specific case of OpenStack, while I hope this post will be more broad in
scope.  Additionally, at the time of his post, Postgres only supported
Kerberos (GSSAPI) *authentication*; I have since written *encryption* support
as well.

## What?

Postgres is in an interesting place right now.  Before my changes, the only
encryption choice is to use OpenSSL and certificates.  While this is fine and
dandy for some use cases, if certificates are not already in use for database
connections, this can be a pain point to manage.

Kerberos is an authentication solution used in enterprise and enterprise-like
(read: multiple users and shared resources they wish to access) environments.
Applications can use Kerberos to offload their authentication to a centralized
(and replicatable) provider, the KDC, which manages Kerberos services.  The
easiest way to create a KDC is to use
[FreeIPA](http://www.freeipa.org/page/Main_Page).

Applications should generally (and typically do) consume Kerberos through
either the GSSAPI or SASL, which provide interfaces for the aforementioned
offloading of authentication as well as encryption (!).  Kerberos has a number
of other advantages as well, but for purposes of this post, it provides strong
authentication and encryption guarantees as well as avoiding the need for
certificate management (though it can still be used with certificates if
desired, which I will not go into here).

## How do I do this?

If you want GSSAPI encryption (as opposed to only authentication), you'll need
my patches which are on
[my GitHub](https://github.com/frozencemetery/postgres/).  The rest of the
instructions are the same since all GSSAPI authentication is opportunisticly
encrypted in my patches.

## Set it up

We'll be going on Fedora (somewhat arbitrarily, I pick fc22).  If you want to
follow along exactly, you'll also need a FreeIPA server, and your postgres
server will need to be enrolled as a client.

If you're running with distro packages, installing postgres looks like this:

    # dnf install postgresql{,-server,-contrib}
    # postgresql-setup --initdb
    # service postgresql restart

If you're running from source (i.e., using my patches, or maybe just felt like
it), it looks more like this after you've installed:

    # /usr/local/pgsql/bin/initdb -D /var/lib/pgsql/data
    # /usr/local/pgsql/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start

In both cases, you'll probably want a root user with corresponding database:

    # su - postgres
    $ createuser root -P # set a reasonable password
    $ createdb --owner=root rootdb

Now we need to, from the postgres machine, alert FreeIPA to our new service:

    # kinit admin
    # dnf install freeipa-admintools
    # ipa service-add postgres/«fully qualified hostname of postgres machine»
    # ipa-getkeytab -s «full address of ipa server» -p postgres/«postgres full address»@«YOUR DOMAIN» -k /var/lib/pgsql/data/pg.keytab
    # chown postgres:postgres /var/lib/pgsql/data/pg.keytab
    # chmod 660 /var/lib/pgsql/data/pg.keytab

That's a bit confusing what with all the substitutions.  For my setup, I ran:

    # kinit admin
    # dnf install freeipa-admintools
    # ipa service-add postgres/postgres.rharwood.biz
    # ipa-getkeytab -s freeipa.rharwood.biz -p postgres/postgres.rharwood.biz@RHARWOOD.BIZ -k /var/lib/pgsql/data/pg.keytab
    # chown postgres:postgres /var/lib/pgsql/data/pg.keytab
    # chmod 660 /var/lib/pgsql/data/pg.keytab

Hopefully that's a bit more clear.

Next, we need to get Postgres set up for speaking GSSAPI.  In particular, it
needs to know about the location of the keytab we created just now.  This is
stored in the file **/var/lib/pgsql/data/postgresql.conf**.  We need to set
the following:

    krb_server_keyfile = '/var/lib/pgsql/data/pg.keytab'
    listen_addresses = '*'

The first line is the location of the keytab postgres will use; the second is
what interfaces postgres will listen on.  That setting may not be applicable
for all use cases if you have multiple internal or external networks.

After that, we tell postgres what users are authorized to connect using
GSSAPI.  Two files control this: the first is
**/var/lib/pgsql/data/pg_hba.conf**.  For testing, I set

    host all all 0.0.0.0/0 gss include_realm=1

and comment out all other fields.  This allows any user to authenticate by
GSSAPI on any address, which is probably not what you want.  Adjust as
necessary.

Since we set `include_realm=1` above, we also need to tweak
**/var/lib/pgsql/data/pg_ident.conf** like so:

    kerb /^(.*)@RHARWOOD.BIZ$ \1

replacing `RHARWOOD.BIZ` with your realm as needed.  Combined with the
**pg_hba.conf** setting above, any user connecting from my realm is allowed to
connect on any address as long as they have a corresponding local user.

Speaking of which, let's apply those changes and create a user.  First,
restart postgres as above; again, if you're using distro packages this looks
like

    # service postgresql restart

and otherwise like

    # /usr/local/pgsql/bin/pg_ctl -D /var/lib/pgsql/data -l logfile reload

Now we should create a local user:

    # su - postgres
    $ createuser rharwood@RHARWOOD.BIZ
    $ createdb --owner=rharwood@RHARWOOD.BIZ rharwooddb

and as above, replace `rharwood` with your user and `RHARWOOD.BIZ` with your
realm.  Then restart postgres one last time.

## Seeing it in action

Finally, you'll probably want to test your connection, perhaps with wireshark
if you're verifying presence of encryption.  So:

    # su - rharwood # your user
    $ kdestroy -A
    $ kinit
    $ klist
    $ psql -h postgres.rharwood.biz -U rharwood@RHARWOOD.BIZ rharwooddb
    $ klist

In addition to encryption (if you're using my patches), you should also see a
difference in output of the two `klist` invocations of a service ticket for
the "postgres" service.

## Future work

Of course, these patches need to land upstream.  One major caveat of
opportunistic encryption as I'm doing here is that an attacker sitting in the
middle can cause encryption to not occur, and oberve and tamper with all
traffic freely.  ***This will not be the case in the final version merged
upstream.***  Instead, there will be (in pg_hba.conf on the server and a
parameter on the client) to require encryption; the connection will then fail
if the other end is not willing to encrypt.  This resolves the
man-in-the-middle concerns.

Eventually, I'd like this parameter to default to "require" rather than
"request" as it will at first; however, for backward compatability, it needs
to default to "require" at the present time.

## End

Thanks for reading!  If you have questions about using a Kerberized
configuration of Postgres (or, really, any other Kerberized software), or
about adding Kerberos (GSSAPI/SASL) support to other software, please do not
hesitate to ask (see contact page).
