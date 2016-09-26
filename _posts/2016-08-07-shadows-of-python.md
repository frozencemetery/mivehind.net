---
layout: post
---

Note: Damien
[pointed out to me](https://mindstalk.dreamwidth.org/450941.html) that
there are elements of this explanation that are just not correct.  I
was going to edit this post, but I rather like his explanation, and
the Perl perspective is novel, so I'm going to leave this post alone
save for adding this link.

A while back, I accidentally introduced the following bug into my Python:


```python
import time

called = False
def f():
    global called

    if not called:
        called = True

        time = 5
        print "in if: " + str(time)
        pass

    print "outside if: " + str(time)
    return

f()
print "top-level: " + str(time)
f()
```

See the problem?  Me either, at first.


```bash
frozencemetery@kirtar:~$ python shadow.py
in if: 5
outside if: 5
top-level: <module 'time' (built-in)>
Traceback (most recent call last):
  File "shadow.py", line 19, in <module>
    f()
  File "shadow.py", line 14, in f
    print "outside if: " + str(time)
UnboundLocalError: local variable 'time' referenced before assignment
{1} (0) frozencemetery@kirtar:~$
```

Toolchains never let us have any fun.

## Time

This happens to come from the
[lurker](https://github.com/frozencemetery/lurker) soure tree.  As such, the
choice of `time` as a variable name isn't random; I was doing some parsing and
one of the fields contained a time.  So... `time`.

## Shadowing

If the above looks like it should run just fine, you think as I did.  This is
something entirely reasonable to do in most languages.  It's a behavior called
*shadowing*, wherein variable names refer to the closest (scope-wise)
definition of the variable.

It sounds fancy when I say it like that, as if I'm talking about some crazy
Haskell thing, which I am:

```haskell
x = 5

f =
  let x = 6
  in x

main = do
  putStrLn $ show f
  putStrLn $ show x

```
```bash
frozencemetery@kirtar:~$ runhaskell test.hs
6
5
frozencemetery@kirtar:~$ 
```

but it's also feature of C:


```C
#include <stdio.h>

int main() {
    int x = 5;

    if (1) {
        int x = 6;
        printf("inner x = %d\n", x);
    }

    printf("outer x = %d\n", x);
}
```
```bash
frozencemetery@kirtar:~$ gcc -o test test.c && ./test
inner x = 6
outer x = 5
frozencemetery@kirtar:~$ 
```

which is probably where I internalized it from.

### Disappointing snake

So Python just doesn't have this.  They hack around it some with the `global`
keyword, which you can see in the example code, but there are some additional
issues that `global` doesn't solve.

## Scope

We can't talk about shadowing without talking about scope, so let's, briefly.
*Scope*, or the area of source from in which it is valid to refer to a
variable, defaults to the function level.  That's why it's valid to do things
like this:

```Python
if cond:
    x = 5
    pass
else:
    x = 6
    pass
print x
```

and have `x` be visible when we hit the `print` statement.

This is somewhat odd to a C-programmer, though.  In C, scope roughly works by
checking each block - starting with the innermost - to find a binding of the
variable name in question.  That's how we can do things like the following
slightly modified version of the C code above:


```C
#include <stdio.h>

int main() {
    int x = 5;

    if (1) {
        x = 6;
        printf("inner x = %d\n", x);
    }

    printf("outer x = %d\n", x);
}
```
```bash
frozencemetery@kirtar:~$ gcc -o test test.c && ./test
inner x = 6
outer x = 6
frozencemetery@kirtar:~$ 
```

and have it be clear to the toolchain what we mean.

### Pataponthon

The combined result of the scoping and lack of shadowing is the bug we started
off with.  We `import time`, which places an object called `time` at the top
level.  Then, when we call `f()`, the `time` label is changed to apply to
something within the function, per function scoping above.  But when we leave
the function, it isn't changed **back**, because there's no notion of
shadowing.  You can't fix this with `global`.

I think the cleanest solution I can give is "don't do that" and also "I wish
python didn't work this way".

## Your honor?

But wait, how else could you handle modules and scoping?  Well, here's some rust:

File **time.rs**:

```rust
#[allow(dead_code)]
pub fn dummy() {
    ;
}
```

File **test.rs**

```rust
mod time;

fn main() {
    let time = 6;
    println!("{:?}", time);
}
```

```bash
frozencemetery@kirtar:~$ rustc test.rs && ./a.out
5
frozencemetery@kirtar:~$ 
```

And to complete the example, if we make a small change to **test.rs**:


```rust
mod time;

fn main() {
    let time = 6;
    println!("{:?}", time);
    time.dummy();
}
```

we get the expected


```bash
rozencemetery@kirtar:~$ rustc test.rs && ./a.out
test.rs:6:10: 6:15 error: no method named `dummy` found for type `_` in the
current scope
test.rs:6     time.dummy();
^~~~~
error: aborting due to previous error
{101} frozencemetery@kirtar:~$ 

```
