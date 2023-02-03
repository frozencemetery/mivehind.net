---
layout: post
tags:
  - tech
  - security
---

## Create and enroll a key

First, we'll need some packages:

```
dnf install pesign mokutil keyutils
```

(Package names are the same on most major distros, though of course your
package manager won't be the same.)

Next, we create a key for signing.  This uses efikeygen, from the pesign
project; I prefer efikeygen because it also creates an NSS database that will
be useful for pesign later.

```
efikeygen -d /etc/pki/pesign -S -TYPE -c 'CN=Your Name Key' -n 'Custom Secureboot'
```

Replace Your Name Key with your name, and Custom Secureboot with a name for
the key that you'll remember for later steps.  For -TYPE, replace with -m if
you only plan to sign custom kernel modules, and -k otherwise.

(Note that this will set up the key for use in /etc/pki/pesign, which is
convenient for pesign later, but it can also be placed elsewhere, like on a
hardware token - see efikeygen(1) for more options.)

Next, export the public key and import it into the MOK (the Machine Owner
Keystore - the list of keys trusted for signing):

```
certutil -d /etc/pki/pesign -n 'Custom Secureboot' -Lr > sb_cert.cer
mokutil --import sb_cert.cer
```

Again, replace Custom Secureboot the chosen name.  mokutil will prompt you for
a password - this will be used in a moment to import the key.

Reboot, and press any key to enter the mok manager.  Use the up/down arow keys
and enter to select "enroll mok", then "view key".  If it's the same key you
generated earlier, continue, then "yes" to enroll.  The mok manager will
prompt you for the password from before - note that it will not be echoed (no
dots, either).  When finished, select reboot.

To check the key imported okay, we can use keyctl.  Output could look
something like this:

```
~# keyctl show %:.platform
Keyring
1072527305 ---lswrv      0     0  keyring: .platform
1013423757 ---lswrv      0     0   \_ asymmetric: Microsoft Windows Production PCA 2011: a92902398e16c49778cd90f99e4f9ae17c55af53
 246036308 ---lswrv      0     0   \_ asymmetric: Your Name Key: 31fe6684706ff53faf26cec7e700f84aa0fd22ae
 919193603 ---lswrv      0     0   \_ asymmetric: Red Hat Secure Boot CA 5: cc6fa5e72868ba494e939bbd680b9144769a9f8f
 341707055 ---lswrv      0     0   \_ asymmetric: Microsoft Corporation UEFI CA 2011: 13adbf4309bd82709c8cd54f316ed522988a1bd4
```

where the important part is that your key is among those listed.  (The
Microsoft keys are the "normal" anchors for secureboot, and the Red Hat one is
present because this is a RHEL machine.)

### Unenroll a key

If you want to unenroll a key you added, just do

```
mokutil --delete sb_cert.cer
```

This will prompt for the password, and reboot through mok manager as before,
except this time select the option to delete the key.

## Sign a kernel

Kernel signatures are part of the vmlinuz file.  Unfortunately, the process
differs between x64 (or amd64, or x86\_64, or whatever you want to call it)
and aarch64.  First, x64 because it's simpler:

```
pesign -c 'Custom Secureboot' -i vmlinuz-VERSION -s -o vmlinuz-VERSION.signed
pesign -S -i vmlinuz-VERSION.signed # check the signatures
mv vmlinuz-VERSION.signed vmlinuz-VERSION
```

Replace VERSION with whatever suffix your vmlinuz has, and Custom Secureboot
with whatever name you chose earlier.

On aarch64/aa64, things are slightly more involved because the signature is
pre-compression.  Not to worry, though:

```
zcat vmlnuz-VERSION > vmlinux-VERSION
pesign -c 'Custom Secureboot -i vmlinux-VERSION -s -o vmlinux-VERSION.signed
pesign -S -i vmlinux-VERSION.signed # check signature
gzip -c vmlinux-VERSION.signed > vmlinuz-VERSION
rm vmlinux-VERSION*
```

## Sign a kernel module

First, prerequisites - the signing tool.  On Fedora/RHEL-likes:

```
dnf install kernel-devel
```

while on Debian-likes I believe this is part of linux-kbuild, and therefore
pulled in by linux-headers.

The sigining tool uses openssl, so we need to extract the key from the NSS
database:

```
pk12util -o sb_cert.p12 -n 'Custom Secureboot' -d /etc/pki/pesign
```

Replacing Custom Secureboot as before.  This will prompt for a password, which
will encrypt the private key - we'll need this for the next step:

```
opensl pkcs12 -in sb_cert.p12 -out sb_cert.priv -nocerts -noenc
```

This is exporting an unencrypted private key, so of course handle with care :)

Signing will be something like:

```
/usr/src/kernels/$(uname -r)/scripts/sign-file sha256 sb_cert.priv sb_cert.cer my_module.ko
```

where my_module.ko is of course the module to be signed.  Debian users will
I think want a path more like /usr/lib/linux-kbuild-5.17/scripts/sign-file.

To inspect:

```
~# modinfo my_modile.ko | grep signer
  signer:         Your Name Key
```

where Your Name Key will be your name as entered during generation.

To test, `insmod my_module.ko` and to remove `rmmod my_module`.

# Sign a grub build

This is fairly straightforward - the signatures live in the .efi files, which
are just PE binaries, which live in /boot/efi/EFI/distro_name (e.g.,
/boot/efi/EFI/redhat).

```
pesign -i grubx64.efi -o grubx64.efi.signed -c 'Custom Secureboot' -s
pesign -i grubx64.efi.signed -S # check signatures
mv grubx64.efi.signed grubx64.efi
```

where Custom Secureboot is once again the name you picked above.  Note that
x64 is the architecture name in EFI - so if you're on aarch64, it'd be aa64,
etc..
