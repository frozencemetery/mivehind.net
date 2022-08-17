---
layout: post
tags:
  - tech
  - security
---

# shim A/B booting support PoC

I've implemented a proof-of-concept for "A/B booting" of shim itself.
Concretely, this means that when a shim fails to boot, an older version will
be tried as a fallback.  This aims to increase the stability and reliability
of shim updates.  Booting the older shim is a stop-gap and not something we
want systems to be regularly doing, so the situation is detected and reported
for admin attention.

This is a proof-of-concept, and additional features/changes are not only
possible but likely.

("fallback" is a term with many meanings in this context, so we attempt to
avoid its use.)

## Trying it out

On Fedora rawhide, install this COPR:

```
dnf copr enable rharwood/shim-ab-enable
dnf update
```

This updates the shim packaging to be wired up with the A/B logic.

However, it doesn't actually provide a second shim (the "B" part of "A/B").
Once the system is updated with the shim from the first COPR, install the
second COPR:

```
dnf copr enable rharwood/shim-ab-second
dnf update
```

Now there are two versions of shim installed on the system.

## Boot counting

Firmwares don't operate on BLS entries, and so this looks different than boot
counting at that level of the stack.  However, in all cases the operation of
recording when a boot succeeds lives in userspace (since the system must have
booted).  It is also possible to detect failures of the "A" loader that fall
through to booting the "B" loader.  In this proof-of-concept, the decision on
what action to take is left to the admin, though it would be easy to script
additional behavior.

This proof-of-concept implements both detections, logging results and a
warning when the "A" loader has failed.

(To simulate "A" loader failure: remove or rename the shimx64.efi/shimaa64.efi
files in the ESP and the latest /usr/lib/shim*, then reboot the system.
Alternately, use efibootmgr to switch the order of primary and fallback.)

## Technical details

The "A" shim uses the existing location in the ESP (e.g.,
\EFI\fedora\shimaa64.efi) and UEFI boot entry.

The "B" shim also lives in the ESP, and its name ends with _b (e.g.,
\EFI\fedora\shimaa64_b.efi).  We do not think 8.3 names are required for these
files.  A new UEFI boot entry is created for it, currently called "Fedora
fallback", and placed immediately after the "A" entry ("Fedora") in the boot
order.  This could be renamed to something else if that’s preferred.

On system update, the shims are rotated - that is, the old "A" shimx64.efi
becomes the "B" shimx64_b.efi, and the new shimx64.efi is dropped into place.
Because the same filenames are used, boot entries are not typically modified
on update.  It is therefore technically possible (though discouraged) to make
an older shim the primary "A" boot target.

The shim files themselves are stored in /usr/lib/shim-ARCH-VERSION-RELEASE
(where ARCH is the UEFI architecture name, like x64 or aa64).  This allows
userspace boot logging to determine which version of shim was booted, not just
whether it was "A" or "B".  (It also allows reuse of these files without
granting read access to the ESP or unpacking RPMs, which is a feature that has
been requested elsewhere.)

Boot logging is kicked off by shim-booted.service, which is currently a
requirement of multi-user.target.  This runs a python script (shimctl) which
logs to /var/log/shim_boots.  The same script is also used for updating shims.
