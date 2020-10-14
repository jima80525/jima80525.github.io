Paginating output from a command line programs seems like it should be easy, but before you go and write it yourself (and discover all the fun of terminal types), I recommend the [Click](http://click.pocoo.org/5/) package.  Click is a handy little tool for creating command line applications.  While it looks like much of the package is devoted to command line args and subcommands, it also has a nice paging utility for relatively small amounts of text.

# How To

I was really impressed with how simple Click made paginating the display of a block of text.  If you discount some minor refactoring I had to do to make a function work with the click.command decorator, there were really only three changes needed:

1. add `import click`

2. add `@click.command()` decorator to my function

3. change the output section from a for loop printing each line to calling `click.echo_via_pager('\n'.join(lines))`


# Pros

Click is well put together, well documented, installed with pip, and worked easily!  I was definitely happy with it for my original task, which was paginating a few hundred lines of text.

# Cons

I ran another test with a second script, this time using a generator to process tens of thousands of lines of text.  The paginator in Click was definitely not designed for this use case and I couldn't make it work.

# Conclusion

I was quite happy with how easy Click made the simple task simple.  Looking at the documentation, it seems that there are a number of other features which will be handy for some of my bigger projects.  I'll definitely be pulling it in for some future projects and refactoring.  I hope to have a comparison of click and argparse in a future post.
