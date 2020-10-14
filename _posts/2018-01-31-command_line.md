# Command Line Args Libraries - A Comparison

Creating command line interfaces is a well-worn path.  There are a lot of libraries out there which will help you simplify the process.  In this post I'm going to do a brief rundown of a couple of these tools and my impresions of them.  I'll admit up front that my conclusions are entirely subjective (no surprise there), but I'll try to call my biases out as we go.

The packages we'll be looking at here are:

* argparse (part of stdlib)
* [click](http://click.pocoo.org/5/)
* [clize](http://clize.readthedocs.io/en/stable/index.html)
* [docopt](https://github.com/docopt/docopt/tree/master/examples)
* [fire](https://github.com/google/python-fire)
* [plac](https://github.com/micheles/plac)

## The task
For this comparison, I'm only going to evaluate a very straightforward set of options.  I do this for two reasons:

1. I think most situations are really only going to call for this.
2. It's the actual set of options I needed for the script I was working on.

The easiest way to share these with you is to show you the usage output from one of my tests.  This is from the click version:

    Usage: clicktest.py [OPTIONS] [LOGFILES]...

    Options:
      -l, --limit INTEGER  Smallest value shown
      -i, --include TEXT   Show only these comma separated commands
      -e, --exclude TEXT   Exclude these comma separated commands
      -h, --help           Show this message and exit.

Limit will be an integer and include and exclude will be strings.

For each of the libraries I'll be looking at, I'll show the relevant code and an example of how the LIMIT field is displayed.  The full source for all of the tests is at this repo.  (TODO add github repo)

## The Contenders

### Argparse

Argparse is the option to beat, primarily because it's included in the standard library.  It handles this job well, is a little verbose and generates a good usage output.

Here's the code:

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="*", help='log files to process')
    parser.add_argument("-l", "--limit", type=int, default=0,
                        help='Smallest value shown')
    parser.add_argument("-i", "--include", type=str,
                        help='Show only these comma separated commands')
    parser.add_argument("-e", "--exclude", type=str,
                        help='Exclude these comma separated commands')
    args = parser.parse_args()
    print('limit = {0}'.format(args.limit))

This code has a couple of great features; It's fairly obvious what it is doing, and it has no dependencies on other modules.  On the flip side, it's fairly long and all of the arguments are returned in an object which must be dereferenced, though some might call this an advantage.

There's another issue with argparse.  It does not handle out of order parameters well at all.  The test example allows for multiple `input` arguments. With most of the other libraries, you can specify these whereever you want on the command line, including sprinkled between the options.  Argparse needs them all put together.  Not a huge deal, but a minor limitation.


### Click

Click has a lot of followers and for good reason.  It does much more than just command line argument parsing.  It has a large array of utility features that can come in handy when doing CLIs; bash aliasing, user prompting, paginating, and many more.

The code to get these options in click is done with decorators and looks like this:

    @click.command(context_settings=dict(help_option_names=['-h', '--help']))
    @click.option('-l', '--limit', type=int, default=0, help='Smallest value shown')
    @click.option('-i', '--include', help='Show only these comma separated commands')
    @click.option('-e', '--exclude', help='Exclude these comma separated commands')
    @click.argument('logfiles', type=click.File('r'), nargs=-1)
    def main(limit, include, exclude, logfiles):
        click.echo('limit = {0}'.format(limit))

You'll note that parameters all come in as paramters to your function which is handy.  Also note the use of the `click.echo` function instead of `print`.  This is one of the utilities and behaves just like print except it fixes a few corner cases for you (printing Unicode, etc).

This is still fairly explicit in what it's doing like argparse, but seems to move the options out of the function and into the decorators which provides a nice separation.

Click does have one oddity (at least in the version I was testing) in that while it  does support --help, it does not support the -h option automatically.  The first line of the code above is the magic to get it to accept -h in addition to --help.  This seems like a strange oversight, but I suspect they wanted to cut down the opportunity of option collision.

Also, in my limited time to evaluate Click, I was unable to figure out how to customize the help message for the arguments.



### clize

Clize is the takes simplification to the next level.  If you don't care about the help string shown for each parameter, parameter types, or default values, it will just use introspection and treat all of the parameters as command line options or arguments.

Clize uses a clever combination of type annotation and docstrings to produce the desired functionality.

Here's the same functionality using clize:

    def main(*input:clize.Parameter.REQUIRED, limit:'l'=0, include:'i'='',
             exclude:'e'=''):
        '''
        process log files

        :param input: log files to process
        :param include: Show only these comma separated commands
        :param exclude: Exclude these comma separated commands
        :param limit: Smallest value shown
        '''
        print('limit = {0}'.format(limit))

You can see the type annotations are used not only to set properties of arguments but also to specify the short options.  The docstrings are then parsed to provide the extended information for each item in the list.

While I think this is really clever, I dislike having the option information spread across two different locations.


### docopt

Docopt is a beautiful idea on the surface of it: Use the docstring for your script to both document and define the command line options and arguments and to generate the usage message.

    '''
    Usage:
        docopttest.py [options] [<logfiles>...]
        docopttest.py (-h | --help)

    Options:
      -l, --limit=<int>          Smallest value shown
      -i, --include=<cmd,...>    Show only these comma separated commands
      -e, --exclude=<cmd,...>    Show only these comma separated commands
      -h, --help                 Show this message and exit.
    '''
    import docopt

    def main(args):
        print('limit = {0}'.format(args['--limit']))

As you can see, the docstring for the script very clearly specifies what the usage message will be.  No surprises there.  This makes it very easy to get the usage message to look just how you want it.

I've heard from several other developers that they really like docopt.  I have to admit that this is the one I found the least intuitive to use.  I will also admit that I suspect this reflects more on me than it does on docopt.  It took me a while to figure out how different parts of the string were significant, how to make the logfiles argument accept more than one filename, for instance.

The best quote I've read about docopt: "it's great if you like to write documentation".

### fire

Fire is a relatively recent addition to this space from Google.  It stands out as the one least designed for creating plain command line tools.  It appears to be targeted at several other spaces: creating REPLs, exploring code functionality, moving bash functionality to python, etc.  It is really compact and is quite clever (some would say 'magic' in a disparaging way).

Here's the same code using Fire:

    def main(*logfiles, limit=0, include='', exclude=''):
        print('limit = {0}'.format(limit))
        ... rest of function deleted ...

    if __name__ == '__main__':
        fire.Fire(main)

As you can see, it really does a great job of getting a function (or any object) as a command line script.  Unfortunately, it skips several things which seem obvious.  I could not find a way to get short options, so to set the limit you need to use `--limit` instead of `-l`.  I also disliked that getting the usage strings is quite non-standard.  You must use a  raw `--` to tell fire that the rest of the options are for it, and then do `--help`.

That said, fire is fairly new and clearly under development.  It's a great idea, but it feels 'not quite ready for prime time'.

### plac

Plac was really a pleasant surprise.  It has a stated goal "to have a learning curve of minutes for its core features" and really lives up to that.  Like several of the other options, plac uses annotations to encode its features.


    def main(
        include: ('Show only these comma separated commands', 'option', 'i')=None,
        exclude: ('Exclude these comma separated commands', 'option', 'e')=None,
        limit:   ('Smallest value shown', 'option', 'l', int)=0,
        *input:  ('log files to process')):
        print('limit = {0}'.format(limit))

As you can see, it makes for a really terse description of the command line options.  Each annotation is actually a 6-member tuple, but not all need to be specified (obviously).  In the example above, you can see that the limit option uses the fourth member of the tuple.  This is the 'type' field and is just a callable which will take a str as input.  (The other two positions are for enumerating specific choices for an option and for changing the META description in the usage output.)

## Conclusion

I was surprised by the number and quality of options available for doing something that, frankly, is already reasonably well covered by the standard library.  Given a personal project to create a command line utility, I would have a tough choice between plac and click.  I suspect I'll likely go with click as it had some other nice features, but we'll see next time I'm in that position.

Unfortunatley, for the project I was originally looking at, I decided that using argparse was the best option.  Not needing another module to load was going to make this script far more usable to my coworkers than having easier command line option code.

