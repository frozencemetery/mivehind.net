---
layout: post
---

Let me tell you about the latest dubious idea I've carried through to
completion.  I promise that thare's actual motivation for what I'm about to
show, but that doesn't make it substantially more aboveboard.  If you really
want to know them, they're at the end.  Anyway, let's talk about

Making a Fedora chroot inside Debian
====================================

First, some precautions.  Be careful about kernel versions: the kernel version
provided by your Fedora release needs to be <= the one provided by your Debian
release else badness may result.  What I'm describing here is not an effective
sandbox; it is instead useful for presenting an alternate interface to an
existing system (i.e., the Fedora interface to an existing Debian).  Do not
rely on it for security properties because it doesn't really have any.

Prep work
---------

Let's start off with some basics.

    $ mkdir fedora

We need a place for the filesystem to live.  All commands for the rest of the
guide will be given relative to the parent of the *fedora* directory.

    # aptitude install yum

Here's the first piece of magic: Yum is packaged for Debian.  So are RPM and a
couple other related tools, which will get pulled in here.  There's also a
tool called Rinse that we could be using in theory, but its repositories are
out of date and it doesn't seem to work.

Download all the things
-----------------------

To use Yum, we need to give it repository links to pull from.  This is a
modified version of a repo from fc20 which notably removes all version
substitution; you can also set the appropriate settings in /etc/yum/vars if
you prefer.

    $ cat /etc/yum.repos.d/fedora.repo
    [fedora]
    name=Fedora 20 - x86_64
    failovermethod=priority
    #baseurl=http://download.fedoraproject.org/pub/fedora/linux/releases/20/Everything/x86_64/os/
    metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-20&arch=x86_64
    enabled=1
    metadata_expire=7d
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-20-x86_64
    skip_if_unavailable=False

    [fedora-debuginfo]
    name=Fedora 20 - x86_64 - Debug
    failovermethod=priority
    #baseurl=http://download.fedoraproject.org/pub/fedora/linux/releases/20/Everything/x86_64/debug/
    metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-debug-20&arch=x86_64
    enabled=0
    metadata_expire=7d
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-20-x86_64
    skip_if_unavailable=False

    [fedora-source]
    name=Fedora 20 - Source
    failovermethod=priority
    #baseurl=http://download.fedoraproject.org/pub/fedora/linux/releases/20/Everything/source/SRPMS/
    metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-source-20&arch=x86_64
    enabled=0
    metadata_expire=7d
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-20-x86_64
    skip_if_unavailable=False

Okay, let's deploy a system.  Ready?

    # yum --nogpg --installroot=`pwd`/fedora install yum fedora-release rxvt-unicode-256color

Alright, in order then.  We need **--nogpg** because we don't have the Fedora
keyring.  **--installroot** specifies what directory Yum should use instead of
*/* as a base.  We need to install Yum because it will be in the chroot.
fedora-release gets us necessary fedora components.  Finally,
rxvt-unicode-256color is my terminal emulator, and for unknown reasons Fedora
doesn't provide a package which contains all terminfos.

Tweaks
------

Most people like their chroots to be able to access the Internet:

    # cp /etc/resolv.conf fedora/etc/resolv.conf
    # cp /etc/hosts fedora/etc/hosts

Then we can actually resolve IPs.

    # echo 20 > fedora/etc/yum/vars/releasever

This sets up your Fedora to be fc20; substitute 20 as needed.

Let's go!
---------

Finally, let's make a deployment script:

    $ cat enter_fedora.sh
    #!/bin/sh -xe

    mount --bind /proc fedora/proc
    mount --bind /sys fedora/sys
    mount --bind /dev fedora/dev
    mount --bind /dev/shm fedora/dev/shm
    mount --bind /dev/pts fedora/dev/pts

    chroot fedora/ || true

    umount fedora/dev/pts
    umount fedora/dev/shm
    umount fedora/dev
    umount fedora/sys
    umount fedora/proc

And away we go:

    # ./enter_fedora.sh

Enjoy your chroot!

Once you're inside
------------------

You should probably update your Fedora installation now that you have it:

    yum clean all
    yum update

Why did you do this?
--------------------

Disk access times.  For large, complex buildjobs that run test suites, I see
large speedups from this approach.  Coupled with ccache, it reduces run times
by about a third over running in a VM (libvirt/kvm + virtio).
