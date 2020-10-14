# Using the Linux 'script' command 

While working on a different project, I recently discovered the 'script' command in Linux.  It captures all of the input and output from a shell session.  This can be really handy if you want to write a blog post that involves a lot of commands.

I did find that there were a few shortcomings in the tool's interaction that took a bit to work around: my prompt is fairly complicated and causes the script log to look funny, and all of the cool settings I've built over the years to colorize commands really make a mess.

## Fixing the prompt for script

My bash prompt is set in my .bashrc file. The problem I found is that while I really like my normal prompt, I want to use a trimmed down version of it when I'm capturing scripts.  In order to do this, I've modified the portion of of my .bashrc to set a different prompt if I'm in the script command.  I did not find a way to automatically determine if I was running script or not, so I ended up using an environment variable to determine which prompt to set (more on this later).

The prompt-setting portion of the bashrc now looks something like this:

```bash
if [ -z ${RUN_SCRIPT+x} ]; then 
   # general purpose prompt setting code here
   # Also I call fortune and a few other things 
   # that I don't want to run in script
else
   PS1='[SCRIPT]\w: '
fi
```
For those of you unfamiliar with the vagaries of setting prompts in bash, the `\w` portion get replaced with the current directory.  If you're in the `~/coding/project` directory, this line will set the main bash prompt to:

    [SCRIPT]~/coding/project: 

## Cleaning up the special characters

Once I got the prompt figured out, I noticed that several commands colorize the output which generates special characters in the captured output.  While your normal terminal knows how to deal with these characters, it looks pretty goofy in the captured output.

Doing a bit of "research" (a.k.a. Google), I found a quick Perl script that will strip those characters out.  As I mentioned above, I want to set an environment varaible before I run script (and unset it when I'm done), so I was already thinking about creating a bash function.  This function is the perfect place to run this cleanup script on the output.  Here's what the function (which lives in my .bashrc) looks like:

```bash
function runscript { 
   # set the name of the output file, default 'typescript'
   if [ -z ${1+x} ]; then 
      NAME="typescript"
   else
      NAME=$1
   fi
   # set env variable to flag special prompt creation
   export RUN_SCRIPT='foo'

   # run script and capture the shell output 
   script $NAME

   # use regex in Perl, col, and mv to clean up the output
   cat $NAME | perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' | col -b > $NAME-processed
   mv $NAME-processed $NAME

   # unset env variable to flag special prompt creation
   unset RUN_SCRIPT
}
```
Walking through this, we set the `$NAME` variable to either the default (typescript) or the first command line argument.  Then we export the environment variable we'll use to control the prompt creation and run the `script` command.

After `script` returns, we use the magic perl script.  I'm not going to dive into the details of the regex, as it's fairly gnarly and, frankly, not that interesting once it works.  Finally, I move the `-processed` file back to the original requested filename.

That's it!  With that in my .bashrc, I can now use the `runscript <filename>` command and it logs all of the output with my custom prompt and without the colorizing characters!

If you'd like more details on the 'script output cleanup' issue, I'd recommend [this SuperUser post]( https://superuser.com/questions/236930/how-to-clean-up-output-of-linux-script-command).

If you'd like more info on how to configure your prompt in bash, check [here](https://www.cyberciti.biz/tips/howto-linux-unix-bash-shell-setup-prompt.html).

I hope this was helpful!