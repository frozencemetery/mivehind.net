---
layout: post
---

I don't like git.  Now that I've said that, I also don't like the way using git is
taught to new users.  It results in problems like this:

[![XKCD 1597 - Git](https://imgs.xkcd.com/comics/git.png "XKCD - Git")](https://xkcd.com/1597/)

I feel like the person in the alt text most of the time, and it's absolutely
not the fault of the people don't understand this thing.  I'm not going to
claim this "uses a beautiful distributed graph theory tree model (it doesn't),
or "pretty simple" (it's not); instead, I'm going to present the git tutorial
I wish someone else would've showed me.

One final note: there is more than one way to do most things in git.  I am
opting for the most cohesive and that which I find to apply to most
scenarios.

## Undo

One thing we are going to do is memorize a few shell commands.  My first Java
tutorial showed all of the boilerplate - the `class`, the `public static void
main(String[] args)`, and asked the reader to take it on faith that this would
all make sense later.  So I'm going to do that here, just this once.

The first thing you need to know is how to undo the previous action.  Undo
comes in two flavors: `git reset --hard`, and `git reset --hard HEAD@{1}`.
(How's that for obtuse boilerplate?)

The first is more of an "abort" - it's used when an "operation" in progress
has gone awry, or was the wrong operation.  (I'll define an operation more
formally in a bit.  If an operation is not in progress, this command is safe.)

The second is an undo proper: after a git operation has completed, to back it
out, you run the obtuse long thing.  Note that `git reset` itself counts as an
operation, so to redo, one effectively just undoes again.  Git does keep a
state log much farther into the past, so it is possible to undo more than one
operation, but I need to explain some other things before we get there.

## Hello, world

Beyond starting with how to fix it when it breaks, I also really appreciate
tutorials that use examples.  In order to perform examples, though, we will
need something to work with: a *repository* for our project.  To do this, we
will make our own using `git init`.  Here is one way it can be called:

```bash
frozencemetery@kirtar:~$ mkdir testrepo
mkdir: created directory 'testrepo'
frozencemetery@kirtar:~$ cd testrepo
frozencemetery@kirtar:~/testrepo$ git init .
Initialized empty Git repository in /home/frozencemetery/testrepo/.git/
```

Note that one can `git init .` in a directory that is not empty, and git will
not touch the existing files.  In fact, git tries to be as apathetic about the
world around it as possible; you can even move the repository around, or
rename it, and git won't care (it won't even notice).

That's all fine and good, but most of the time we don't work with repositories
created in this way.  Most of the time, "someone else" made the repository -
whether that person is another person running `git init` for their codebase,
or a piece of software (e.g., GitHub) running per user request.

How do we get this code?  Well, for example, to get the source for this
website, one could do this:

```bash
frozencemetery@kirtar:/tmp$ git clone https://github.com/frozencemetery/mivehind.net
Cloning into 'mivehind.net'...
remote: Counting objects: 277, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 277 (delta 0), reused 0 (delta 0), pack-reused 273
Receiving objects: 100% (277/277), 2.12 MiB | 3.14 MiB/s, done.
Resolving deltas: 100% (139/139), done.
frozencemetery@kirtar:/tmp$ cd mivehind.net 
frozencemetery@kirtar:/tmp/mivehind.net$ ls -A
about.md  _config.yml  css       .git        _includes   _layouts  _posts
assets    COPYING      feed.xml  .gitignore  index.html  LICENSE
```

And it's all there.  Be careful - there will have been new commits since this
writing, and not all outputs will match exactly.

## Dotfiles?

In the above example, there are two entries whose names start with a dot, and
so are invisible in normal `ls`.  The first is the ".git" directory.  This
contains internal git state - everything git knows about the repository.  It's
very interesting to look at what's in there, if you're me and are interested
in the inner workings of version control.  Otherwise I don't recommend it.

The other dotfile, ".gitignore", is more interesting.  As the name might
suggest, it is a list of filename (patterns) for git to ignore.  So if you
look at mine:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ cat .gitignore 
*~
out.html
```

What does it mean to ignore a file?  Well, git, as version control software,
has a notion of what files it "tracks".  Files can be in any of three states:
*tracked*, *untracked*, and *ignored*.  I use `git status` to compare this:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ echo "foo" > out.html
frozencemetery@kirtar:/tmp/mivehind.net$ echo "foo" > untracked
frozencemetery@kirtar:/tmp/mivehind.net$ echo "foo" > feed.xml 
frozencemetery@kirtar:/tmp/mivehind.net$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)
    
        modified:   feed.xml
        
Untracked files:
  (use "git add <file>..." to include in what will be committed)
          
        untracked
              
no changes added to commit (use "git add" and/or "git commit -a")
```

There's a lot going on in the output of that command, so let's go through some
of it (and we'll do more in a bit).

First, we edit the contents of, in order, an ignored file, an untracked file,
and a tracked file.  Then, when we ask git about the state of the world (`git
status`), it tells us nothing about the first file (because it's ignored),
that an untracked file exists (because we just made it), and that a file has
changed (modified).

Now, as a demonstration, here's what undo does:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git reset --hard
HEAD is now at e2840c0 [post] Write about numbers
frozencemetery@kirtar:/tmp/mivehind.net$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Untracked files:
  (use "git add <file>..." to include in what will be committed)
  
        untracked
    
nothing added to commit but untracked files present (use "git add" to track)
```

Note that it only undid the changes to the file(s) that git tracked - the
untracked file and the ignored file are left alone.

## Basic commit workflow

`git status` really likes to talk about commits, so I'll humor it.  But first:
what is a commit?  It sounds simple, but...

The answer is nontrivial, and requires understanding how git works internally
because it provides no abstraction over this concept.  In git, a *commit* is a
snapshot of the repository contents (in its entirety), at a particular point
in time, with a message, that has a notion of the commit that preceded it
(which git calls *parent*).  In order to accomplish this last bit, each commit
has an associated *commit hash* that is (hopefully) unique.  (It's currently
sha1, though I hope it changes for collision reasons.)

Git organizes commits into *branches*.  Branches are just readable pointers
for the hashes, and can be moved to point to a different hash.  (This will
make sense in a moment.)  The default branch is named master, so that is the
branch we are on now, as `git status` informed us.  More formally, *HEAD* is
pointed at the tip of the master branch, where HEAD is a pointer at to the
hash which reflects the repository state.

So let's say, for the sake of example, we wanted to include the "untracked"
file in my blog.  Well, the first thing we should do is switch to another
branch because most projects consider it bad practice to develop on master.
That would look like this:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git checkout -b new_file
Switched to a new branch 'new_file'
frozencemetery@kirtar:/tmp/mivehind.net$ git status
On branch new_file
Untracked files:
  (use "git add <file>..." to include in what will be committed)
  
       untracked
    
nothing added to commit but untracked files present (use "git add" to track)
```

`git checkout` is a command which manipulates both HEAD and the repository
contents simultaneously.  In this case, we have asked it to create a new
branch, called "new file", which points to the same hash as HEAD (which, one
will recall, is at the tip of master).  And once it's done that, `git
checkout` will switch HEAD to point to it and update repository contents to
match.

Since they point to the same hash, no changes are actually made to the
repository contents.  However, if we were switching to an existing branch
(call `git checkout new_file` instead), it is possible that there would have
been changes to repository contents.

Git requires committing changes to happen in two steps: first, we *stage* what
we want to commit, and then we actually commit it.  But we also can only
commit changes to tracked files.  Fortunately, the command for adding a file
to git's tracked file index and the command for staging are the same:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ mv untracked f
frozencemetery@kirtar:/tmp/mivehind.net$ git add f
frozencemetery@kirtar:/tmp/mivehind.net$ git status
On branch new_file
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)
  
    new file:   f

```

I renamed the file first because this will get really confusing otherwise.
But look at that: our file is ready to go.  If we wanted to make a multi-file
change, we could also run `git add` more times, but let's not for now.
Instead, we'll go ahead and make a new commit.  To do this, we just run `git
commit`.  There's no fancy syntax highlighting here because this command will
spawn an editor for you to type a message explaining your commit.  Nah, here
it is:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git commit
[new_file 902e6ed] HEY I MADE A COMMIT
 1 file changed, 1 insertion(+)
 create mode 100644 f
```

A brief note on commit messages: the git tooling - and most projects - expects
your commit messages to consist of a single, <50 character message.  This can
be followed by a <~78 character-wrapped paragraph separated by a blank line.
There can also be colon-delimted tags (think HTTP headers, if you're
familiar).
[Commit message styling is something people care a lot about.](https://chris.beams.io/posts/git-commit/)

Of course, we probably wanted to **see** this commit.  Not to worry; git
allows us to view the commit history in a branch with `git log`.  This will
open a pager if the history does not fit in the terminal, but the top will
look something like this:

```bash
commit 902e6edd93b9cf6f9de636a07a00c0c3c7f30151
Author: Robbie Harwood <ihate@spam>
Date:   Sun Feb 19 17:08:01 2017 -0500

    HEY I MADE A COMMIT
    
    HOW DO I TURN OFF CAPS LOCK AGAIN
    
    Resolves: #37

commit e2840c0c1cce1778261311378ca73ce8abfd89de
Author: Robbie Harwood <itsreal@bad>
Date:   Sun Feb 12 20:36:33 2017 -0500

    [post] Write about numbers

```

So, for each commit, it shows the hash, the message, (a few other things,) and
then the first parent is just the next one in the list.

## Pull requests and remotes

Git purists will say that pull request procedure is not part of git proper.
To which I say that, while perhaps true, it does the reader a disservice to
ignore it.  Since this is the direction most tools are heading, and because
this is how I handle the <s>victim</s> example repository, I assume something
that works like GitHub.

So we go into our tool and click the "*fork*" button.  (Please don't actually do
any of this to my website's repo unless you have noncontrived changes to
contribute.)  A fork is your own copy of a (generally read-only) upstream
repository, which therefore shares history and intends to contribute back
changes.  Once done, we need to tell git about this fork.  Git tracks
non-local versions of the repository as well as the local one; these are
called *remotes*.  So in order to add our fork, we would do something like
this:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git remote add my_fork https://github.com/my_user/mivehind.net
frozencemetery@kirtar:/tmp/mivehind.net$ git remote -v
my_fork https://github.com/my_user/mivehind.net (fetch)
my_fork https://github.com/my_user/mivehind.net (push)
origin https://github.com/frozencemetery/mivehind.net (fetch)
origin https://github.com/frozencemetery/mivehind.net (push)
```

At which point we can say `git fetch my_fork`, which will tell git to update
its cache of the my\_fork remote's state.  To go the other way, we use `git
push -u my_fork` to create the current branch on our fork and update it with
our contents.  (Thereafter, we can invoke `git push` on the branch, since git
tracks which remote a branch is tied to, or *tracks*.)

From there, it's back into the web interface to make a PR from our fork's
branch.

### Receiving a pull request

Suppose you were me, received this pull request, and decided to add it to the
repository.  Depending on how the project works, I would do one of two things,
which I will call the merge workflow and the rebase workflow.

Most web tools, GitHub included, favor the merge workflow by providing a
button to do it for you.  Supposing I wanted to do this myself, though, I
would first fetch your fork (add remote first), and then generate a *merge
commit*.  A merge commit is a special kind of commit that is identical to a
normal commit except that it has multiple parent commits.  The easiest way to
generate a merge commit is to run `git merge my_fork/new_file`, where my\_fork
is the remote and new\_file is the branch, which will create a commit uniting
the new\_file branch from the fork onto the current branch.  A merge commit
typically merges a smaller, development branch onto a main branch.  Many
people do not like merge commits because having multiple parents creates a
nonlinear history, which is more difficult to work with later.

This contrasts with the rebase workflow, which is harder to execute but
results in a cleaner repository history.  Here, confusingly, one also runs
`git merge`, but does it slightly differently: `git merge --ff-only
my_fork/new_file`.  If it all works, then the current branch looks as if the
commits in new\_file had happened on top of it originally.  That is, no merge
commit is generated.  I'll get into what happens for failure in both workflows
in just a moment.

As an example of this in the wild: the Linux kernel uses the rebase workflow
(without a web tool) for each subsystem, and then the subsystem maintainers
periodically ask Linus to pull their subsystem into the mainline kernel branch
using merge workflow.

## Conflicts and rebaseing

If there have been changes to origin's master branch since the fork's branch
was created, then both workflows may fail.  (Rebase will always fail; merge
will only fail if both branches have modified the same section of the same
file.)

`git merge`, in the merge workflow, will prompt the operator (that's us) to
fix the conflict: `git status` reveals what is wrong, and git sets off the
problematic regions of the file with "\<\<\<" and "\>\>\>".  `git add` the
files once fixed, and then commit when done.

The rebase workflow is so named because of the way these conflicts are
resolved.  Typically the problem of failure here is given back to the
contributor of the pull request, which I think is bad, but since it's common I
need to explain it.

First, get the changes to origin's master branch.  Then we run `git rebase` to
edit history.  This is a very dangerous operation.  Or rather, it would be, if
I hadn't opened with how to undo.  It looks like this:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git checkout master
Switched to branch 'master'
Your branch is up-to-date with 'origin/master'.
frozencemetery@kirtar:/tmp/mivehind.net$ git pull origin
(Your output will vary depending on the state)
frozencemetery@kirtar:/tmp/mivehind.net$ git checkout new_file 
Switched to branch 'new_file'
frozencemetery@kirtar:/tmp/mivehind.net$ git rebase -i master
```

Hey look, a wild new command appeared!  `git pull` is just a handy shortcut:
it runs `git fetch` followed by `git merge --ff` (which will not generate a
merge commit unless there is a conflict one needs to resolve).

The final invocation in that block performs what we call an *interactive
rebase*.  It will open an editor displaying the actions to be performed.
Here, we're just using it as a sanity check: it should show only commits from
the fork's branch, but sometimes it gets confused.  `git rebase` is a very
powerful history editing tool, and I'm not going to be able to explain it all
here.  Many people prefer not to work with it at all, and history editing is
actively discouraged in other version control systems (e.g., mercurial).

Save and close when you're done staring at the abyss, and git will carry out
the changes.  If there is a problem, or you requested it stop for editing,
`git status` now gives helpful prompts about how to proceed.  (There used to
be a much longer section here.)

## Reflog (or, undo explained)

Recall that git uses HEAD as a reserved name pointer to the checked out
repository state.  So check this out:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git reflog
902e6ed HEAD@{0}: checkout: moving from master to new_file
e2840c0 HEAD@{1}: checkout: moving from new_file to master
902e6ed HEAD@{2}: commit: HEY I MADE A COMMIT
e2840c0 HEAD@{3}: checkout: moving from master to new_file
e2840c0 HEAD@{4}: reset: moving to HEAD
e2840c0 HEAD@{5}: clone: from https://github.com/frozencemetery/mivehind.net
```

(If you've been following this tutorial closely, yours will not match mine.)

What are we looking at?  Well, it's the history of where HEAD has been.
HEAD@{0} is the same as HEAD - that is, the current state.  And HEAD@{1} is
the previous position, and so on.  Note that git records the operation,
including the type, as well as a truncated version of the commit hash.
(People, including tools such as GitHub will use these truncated hashes in
place of the full one; they really shouldn't since it makes collision even
more likely.  The kernel has had a non-malicious instance of truncated hash
collision already.)

But I've only explained half the story.  `git reset` is a command that moves
head.  Passing "--hard" causes it to also adjust the repository directory to
match; without "--hard" it will not change files on disk.  And the reason
"multiple undo" is nontrivial is that its own HEAD movement is recorded:

```bash
frozencemetery@kirtar:/tmp/mivehind.net$ git reset --hard HEAD@{1}
HEAD is now at e2840c0 [post] Write about numbers
frozencemetery@kirtar:/tmp/mivehind.net$ git reflog
e2840c0 HEAD@{0}: reset: moving to HEAD@{1}
902e6ed HEAD@{1}: checkout: moving from master to new_file
e2840c0 HEAD@{2}: checkout: moving from new_file to master
902e6ed HEAD@{3}: commit: HEY I MADE A COMMIT
e2840c0 HEAD@{4}: checkout: moving from master to new_file
e2840c0 HEAD@{5}: reset: moving to HEAD
e2840c0 HEAD@{6}: clone: from https://github.com/frozencemetery/mivehind.net
```

## Extra: notation

Git has many different ways to delimit commits and commit ranges.  If I've
written this well, you should be able to now read most of `man gitrevisions`.
Git has
[its own idiosyncratic documentation style](https://git-man-page-generator.lokaltog.net/)
that it's worth getting used to eventually.

In particular, I recommend understanding "~", "^", and ".."; one may also find
use for "..." on occasion.  It is also important to be aware of which commands
use "remote/branch" and which use "remote branch".  More on this at the end.

## Extra: working with release branches

Occasionally, one may wish to apply a specific commit from another branch onto
the current branch.  Supposedly there was debate about including this
functionality into git at all (though one can beat on the tool to do pretty
much anything, especially with `git rebase`), but I have found it very useful
in managing *release branches*.  A release branch is a branch which is
expected to be slower-moving than master; generally, it only receives new
commits for bugfixes, and eventually it stops being supported.

Typically, these bugfixes will land in the master branch first, and then the
stable branch maintainer will apply them.  The invocation is `git cherry-pick
-x commithash` (where commithash is of course the hash of the target commit,
or a pointer to it, or a commit range).  I recommend the use of "-x", which
will record the commit hash we cherry-picked from in the new commit.  Remember
that since commits include parent information, this will not be the same hash.

## Extra: stash

Certain git operations demand full control over the tree and will complain if
there are changes which have not been committed.  The easiest things to do are
of course commit the changes or discard them, but sometimes this isn't
possible.

Enter `git stash`.  Running this command creates a temporary commit with your
changes.  One can then perform the persnickety operation, and then run `git
stash pop` to restore the changes.

This is a very "hold my beer" kind of operation: its very common to push a
stash and forget to pop it later.  Since there are no commit messages logged,
these are almost always incomprehensible when discovered.  Incidentally, it is
possible to make multiple stash commits, and they function as a stack; I do
not recommend it.

## Final thoughts

This is pretty much all of the git I use regularly.  There is of course more
out there.  A lot more, actually:

```bash
frozencemetery@kirtar:~$ apropos ^git | wc -l
187
```

Historically, git has become extremely prevalent due to its speed.  Its user
interface is not intuitive at all; the user must be aware of its internal
workings.  The design did not believe in abstraction, and there are parts that
were very clearly
[not designed as part of the whole](http://stevelosh.com/blog/2013/04/git-koans/).
Please do not make software like this.
