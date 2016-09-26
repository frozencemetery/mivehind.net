---
layout: post
---

I have a perfectly good package manager on my system.  But many of the
programming languages I work with graft package management capability onto
their buildsystems, and the result is a mess.  I'd much rather they be able to
build site packages for other package managers, but this battle appears to
have been lost long ago.

For my own reference (and hopefully that of others as well), here are some
hammers for making these language packagers integrate better.

## Python

I'm going from what I expect is most familiar to people to least, which means
Python gets to go first.  There are two tools I want to talk about here:
`pip`, which is almost always used, and `virtualenv`, which can be used in
conjunction with `pip`.

### virtualenv

`virtualenv` helpfully describes itself as a tool to "create virtual Python
instances".  What they mean by this is that it allows an installation
environment segregated from the global installation environment.  It's
actually quite nice for development.

`virtualenv` will install its own `pip` which knows to install Python packages
into the current virtualenv.  By default this environment is essentially
unpopulated, which means that everything will be installed from PyPI.  This is
a great behavior if you don't trust your distro to provide stable packages,
and a terrible behavior if you do.  Fortunately, this is togglable: the flag
`--system-site-packages` allows passthrough from the virtualenv to the
system installed python packages.  (Or, if it's easier to think about, the
virtualenv is pre-populated with the Python packages installed on your system
already.)

### pip

Run `pip install` as root and you'll get packages (and their dependencies)
installed from PyPI onto your system.  When working with a
**requirements.txt**, this is fine - just install each dependency from the
system package manager and then install the package with pip.  If you don't
have such a file, or if some of those dependencies themselves aren't packaged,
then it's more of a problem.  There don't seem to be any flags for dry-run or
pretend or anything like that.

The workaround I usually use is to set up a virtualenv with system
passthrough, try to install the package with pip, and see what it pulls in for
dependencies.  (`pip list` to show the installed packages is also useful
here.)  Then delete the virtualenv, install from the system package manager,
and only then call pip globally.

### RPM note

Because of `virtualenv`, the Python packaging is the *only* one I will discuss
here that it is not insane to use on Fedora/CentOS/RHEL.  The problem that you
will encounter with any of the others is that these three distros do not
believe in the **/usr/local** hierarchy, which means that not only will
`yum`/`dnf` be willing to uninstall packages that the language-specific
manager installed, but the language-specific manager will be willing to
uninstall packages installed from `yum`/`dnf`.  You can imagine how well this
goes.

## Ruby

Ruby package management is done through `gem`.  If the "rubygems-integration"
package is present (Debian), then `gem` and the system package management seem
to play nicely together - `gem list --local` will show things installed by
both `gem` and APT, as you'd expect.  I didn't check what happens if you don't
have that installed.

At first glance, `gem dependency` seem to do exactly what I'd want here, which
is to say, it prints the dependencies of a gem.  Weirdly enough, though, it
only does this for installed gems, which makes me wonder what it's intended
for.

Fortunately, there's a dry-run verb: `--explain`.  Per the documentation,
passing `--conservative` and `--minimal-deps` (what is the difference between
these?  The documentation sure doesn't say) will cause it to do... the thing
I'd've expected to be default... and not touch packages that are acceptable
already.  However, my experience suggests a caveat: when working with both
`--explain` and one of the "don't touch my stuff that's good enough" flags,
`--explain` sort of just ignores the other flag.  So you get the simulated
result as if it were going to upgrade some things that are already acceptable,
or, weirdly enough, install some things that are already present.  I really
don't know what's going on here.

## Haskell

Another language, a package manager that doesn't have an `uninstall`
verb.  (`gem` doesn't either, I just find it more painful with `cabal`
because I use ruby more.)  What it does, thankfully, have is a
simulate verb: `--dry-run`.

Fortunately, Haskell projects are the simplest of any so far here:
requirements need to be specified as part of the **projectname.cabal** file.
So calling out to the system package manager isn't too bad here.  And root
installations of packages will end up in the system package cache as well, so
dependencies can also be handled this way if desired.

A related tool that bears mentioning here is `ghc-pkg`.  To see the system
packages and their versions, one doesn't call `cabal`, but rather `ghc-pkg
list`.  And to check the integrity of the system package set, `ghc-pkg check`.
This latter is actually how one uninstalls pacakges: remove the related files,
and then use `ghc-pkg check` to make sure you got everything, followed by
`ghc-pkg unregister`.

## Rust

Rust doesn't have package management capability yet.  It will soon though.
That's not to say it doesn't do dependency management - it does - but rust
programs are currently compiled as an entire unit.  This means that currently
there's nothing *to* package.  Future expansion needed.

## Final thoughts

I'm not really happy about any of these, but I'm least happy with what ruby is
doing.  I feel like I had to fight the tooling to get it to do what I wanted
here, and (though all of them fail in this regard), there was of course no man
page for anything.
