# TIL - Keeping track of small ideas

If you're like most developers, you have a wide range of "little things" that you do just infrequently enough that you never remember exactly how to do them.  "How do I open the filename under my cursor in Vim?", "How do I commit only part of a file in Git?", "How do I get sed to replace xxx with yyy in a series of files?", etc.  The sort of things that you know are possible, but just don't use often enough to commit to memory.

There are many techniques for remembering these, ranging from googling it every time you need it to writing it down in a lab notebook.  I recently came across an idea that's really growing on me, called TIL for "today I learned...".

The examples I've seen are kept in a github repo with a nice markdown index as the README.md file.  Each of the little tidbits of information are kept in their own markdown file in a directory indicating a category.  For example, you might have a `git` directory with a `partial_commit.md` file.

The example I first saw, [jbranchaud/til](https://github.com/jbranchaud/til), was organized this way.  He also was very consistent in placing a good title at the top of each topic file.  This consistency makes it very easy to automate the creation of the README file, so I've added that to my version (and created a pull request for the original author).  In my repo I've added the creation script as a pre-commit hook for git so this is done automatically for me each time I commit!

You can see the creation script [here](https://github.com/jima80525/til/blob/master/createReadme.py).

Please share your methods for tracking items like these that you've found useful in the comments below!
