---
layout: post
tags:
  - tech
---

# Why I dislike switch statements

In most coding styles (and in particular, in K&R, OTBS, and Linux), switch
statements are written like so:

```C
int func(int i) {
    switch (i) {
    case 1:
        do_something();
        break;
    case 2:
    case 3:
        do_something_else();
        break;
    case 4: {
        int j = i * 2;
        return j;
    }
    case 5:
        do_another_thing();
        /* Fall through. */
    default:
        return 2;
    }
    return i;
}
```

Of course this is a contrived example, but readers will hopefully agree it's
representative of the construct.

# Awkward

First, there are several things I consider clunky about using `switch`.

1. The different `case` "arms" are deindented to the same layer as `switch`.
   Conceptually this is odd because they're still within the `switch`.
   However, the alternatives aren't better: indenting the arms wastes another
   4 characters on the line (or tab width if you're like that), and
   half-indents are an excellent demonstration of why [argumentum ad
   temperantiam](https://en.wikipedia.org/wiki/Argument_to_moderation) is
   fallacious.
1. Instead of being delimited by braces (`{` and `}`), execution flow is
   instead delimited by `:` and `break`.
1. As in `case 2` and `case 3`, adding another value introduces another line
   in many styles.  Thus, using `switch` is invariably at least as much code
   as the equivalent `if/else` flow.
1. Each arm of the `switch` is not a separate scope.  This leads to the
   pattern in `case 4`, wherein an explicit scope is needed to declare `j`.
1. Because the `break` is needed to delimit cases, compilers warn on its
   absence - i.e., when control flow "falls through".  However, since this is
   desirable in some cases, they do not warn when it's commented as
   intentional.  Thus, the comment in `case 5` becomes syntactically
   necessary.
1. No ordering on arms is imposed.  In practice this is generally helpful, but
   it leads to the weird situation where `default` doesn't *have* to be the
   final arm.

Finally, `default` prohibits flattening control flow in a helpful way.
For example, consider this code:

```C
int func(int i) {
    if (i == 0) {
        return 1;
    } else if (i == 1) {
        return 0;
    } else {
        i = do_some_stuff();
        if (i == 3)
            return 2;
        else
            return -1;
    }
}
```

Ideally, we would like to rewrite this as:

```C
int func(int i) {
    if (i == 0)
        return 1;
    else if (i == 1) {
        return 0;
    
    i = do_some_stuff();
    if (i == 3)
        return 2;
    
    return -1;
}
```

By flattening the control flow, we make the code significantly easier to
reason about.  For instance, it's now very clear whether all paths through the
function lead to a `return`.

The need for `default` makes this pattern much less elegant.  The equivalent is:

```C
int func(int i) {
    switch (i) {
    case 0:
        return 1;
    case 1:
        return 0;
    default:
        i = do_some_stuff();
        if (i == 3)
            return 2;
        return -1;
    }
}
```

and to my mind it's debatable whether an empty `default:` arm helps that much.

# Interaction loops

More than the general awkwardness, though, I'm bothered by how `switch`
interacts with loops.  (And no, I'm not referring to [Duff's
Device](https://en.wikipedia.org/wiki/Duff%27s_device) which, while horrible,
shouldn't appear in modern code anyway because we have since optimized
`memmove()/memcpy()`.)

Consider code that looks like the following:

```C
int func(int i) {
    while (1) {
        switch (i) {
        case 1:
            continue;
        case 2:
            break;
        default:
            return 2;
        }
    }
    /* Point of interest. */
    return 0;
}
```

Control flow here is complex.  Consider what happens in each of the three
cases.  In particular, `switch` is "kind of" loop-like in that it services
`break`, but "kind of" conditional-like in that `continue` is handled by a
higher scope.  This makes trying to run code at the marked point of interest
surprisingly involved, as well as making it difficult to terminate the loop
itself.

Contrast with the this similar (but importantly different) code:

```C
int func(int i) {
    while (1) {
        if (i == 1)
            continue;
        else if (i == 2)
            break;
        return 2;
    }
    /* Point of interest. */
    return 0;
}
```

From inside the `if/else` stanzas, it's very clear how to get to the point of
interest, and `break` and `continue` behave in clear ways.

# Conclusion

Historically, the most important reason to use `switch` statements was that
the compiler could optimize them into jump tables.  These days compilers are
capable enough to perform this transformation where it's needed - in
particular, whether a construct is expressed as `if` or `switch` doesn't
prohibit it from being a jump table.

The other major reason I'm aware of to use a `switch` is for exhaustiveness
checking on `enum`s.  The theory is that the compiler can check that all
defined values for an `enum` are handled at any given point.  While true, this
typically doesn't matter:

1. Most of the time, not all `enum` values represent expected program states.
1. Compilers and static analysis tools also warn about missing `default:`
   branch, which negates the exhaustiveness check.
1. There are other, more-or-less equally clear ways to write `enum`-driven
   state machines (e.g., dispatch table, callbacks, continuation-passing
   style, etc.).

I'm not about to issue an ultimatum and say "don't use `switch`" or anything
similar.  These are just the reasons that I happen to not like it.  Certainly
Python not having a close equivalent should be demonstration enough that it's
not needed in the language.

And all that being said, when the idea of `switch` is generalized (into
pattern matching), I do prefer it to `if`.  Languages like Haskell (and to a
lesser extent, Rust) provide nicer constructs, but they're also reliant on
Algebraic Data Types (which Rust clarifies by treating them as generalized
`enum`s).
