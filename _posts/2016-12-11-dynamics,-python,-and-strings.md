---
layout: post
---

This week I'm going back to a technical post because
[two](https://mindstalk.dreamwidth.org/461722.html)
[friends](https://zenhack.net/2016/12/11/on-python.html) both did it and that
is a bandwaggon I can't not hop on.

Dynamic languages have as their main feature that they are un(it)-typed - that
is, depending on your perspective, either every value has the same type (and
so typechecking always succeeds), or the language has no types (and therefore
there is no typechecking step).  For my purposes, since I have a PL
background, it makes more sense to consider every value to have the same type;
unit-typed, rather than un-typed.

This is important because I want to talk about what that type is.  (Yes, yes,
I know it's top.  That's not a useful view here.)  Because while in a sense
it the superset (supertype?) of the features found in all other types in the
language, dynamic languages care much more for the interfaces presented rather
than the actual signature.  One complete view of the system is that the only
things one can do with a value are to use it as an argument to a function.

Where one gets these "function" things is a bit of a thorny point: some
languages first-class them, and some do not.  In Python, for instance, a
function is something that implements the `Callable` interface, which means it
has a `__call__()` method.  So objects have associated methods, but that
doesn't quite break this view because method dispatch can be overridden.  And
since python has run-time duck typing, it's turtles all the way down.  Quack.

Slightly more formally, the unit type in Python is Object (Python also calls
these `class`es).  Ruby, Perl5 and other object-oriented dynamic languages will
behave similarly, which makes sense because they have "object" right there in
the name (though they don't have the same dispatch handling as Python, and
Perl has some actual pre-runtime checking with `use strict` and friends).
Lisps tend to have something akin to a function as the unit type (anything
that can have `eval()` called on it, which is a bit more complicated, but
close enough).  Either way, Lisp is spacy and awesome, and someday someone
will make a typed lisp I like.

And then there's shell (by which I mean, POSIX shell and things like it; new
shells like scsh and xonsh are not invited to this particular party).  The
shell doesn't really have a single unit type.  This is partly an accident of
specification (it wasn't intended in the same way that the object-oriented
languages were built around object), but the language is built around strings
and their manipulation.  There is also this function-type that
feels grafted on: functions don't behave anything like strings.  There are
also arrays, and command builtins, functions, and programs all behave
differently, and a whole host of other language oddities.

And there are of course
[many other scripting languages](https://en.wikipedia.org/wiki/Category:Scripting_languages),
and I am not about to go through them one-by-one.  For instance, AWK behaves
very similarly to shell from this perspective, and AppleScript has unit type
dictionary which is novel.  However, neither are very common anymore, and by a
similar token, I do not know most of the languages on that list.

I suggest that the ideal dynamic language has a unit type of string.  This is
largely a result of my own experience (mostly with shell and Python, sadly).
But I think it makes some sense: when one wants to start building layers of
abstraction (with objects, or functions, or however else), it is time to go
get a typechecker.  When performance starts to matter, string is no longer the
ideal type, and one needs a compiled language anyway.  But if one is doing
substantial string manipulation, the language should absolutely support that,
and provide the nicest (not necessarily the fastest) abstractions for that.
(And if it wants to graft some funcionality on for building those libraries,
that is maybe a price worth paying.)

These days, even for prototyping, I no longer reach for a dynamic language
because I do not enjoy debugging my prototypes when they have runtime
failures.  Most of my programs (which, coincidentally, never see the light of
day) never pass beyond using shell (without many functions) and AWK; those
that do either move into C (systems logic that must perform), or a subset of
Python2 that never uses `class` (and rarely uses function either).  Perhaps
one day Rust will replace some of that as well.  I can hope, at any rate,
because the only language on that list I actually like from a design
perspective is AWK.
