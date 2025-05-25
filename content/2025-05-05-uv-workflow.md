Title: My New `uv` Workflow
----------------------

I've recently changed my python project workflow based on a great write-up by [Trey Hunner](https://treyhunner.com/2024/10/switching-from-virtualenvwrapper-to-direnv-starship-and-uv/). The workflow makes setting up and using virtual environments for several projects fast and easy. It is also useful if you've only got a single, main project you're developing, as it allows you to get to the project, activate the virtualenv, and be ready to work, all with a single command.

Trey did a great job of explaining the details of what `uv` is and why you might want to use it, so I won't go into too much detail here, other than to point out the `uv` is remarkably fast. It's enough faster that, like rust, it changes how you use the tool by allowing you to run it frequently without noticeable time added to your work.

Trey started with a workflow that was similar to what I was using (virtualenvwrapper+pyenv) and ported it over to use `direnv` and `uv`.  I have shamelessly copied his work, ported it to bash ('cause I'm old-school) and expanded it a bit.  Let's walk through how I use it.

## The Workflow

Before going into the details of how to set up this system, I'll walk you through what it looks like in operation. There are three commands, one used when creating a new project, one used in normal, day-to-day operations, and one primarily for debugging things.

### Setting Up a Brand-New Project

To set up a new project in this workflow, it's easiest to create an empty directory, change into that directory, and then run the `venv` command:

    :::sh
    > mkdir my_new_project
    > cd my_new_project
    > venv


The `venv` command will create a virtual environt for you and configure `direnv` to automatically activate this virtual environment when you change to this directory.  It also adds a mapping from this project name to this directory which will enable the `workon` command, described below.

There are a few options you can use for the venv command. You can use something other than the directory name for your project name:

    :::sh
    > venv this_name_is_better

You can specify which version of python you want:

    :::sh
    > venv --python=3.11

If you don't currently have that version of python installed, `uv` will auto-install it for you and then use it for the venv.

**NOTE:** Due to my lack of bash-magic, you *must* have the `=` in this option.  I hope to fix this at some point, but that may be by rewriting the tool in Python.

You can use any of the options available to [`uv venv`](https://docs.astral.sh/uv/reference/cli/#uv-venv).

If you want to use options **and** use an non-default project name, the project name **must** come at the end. Again, this is due to lack of bash-ability on my part.

### Setting up an Existing Project

If, instead of a brand new project, you want to use this on an existing project, say one you're going to clone from github, the process looks pretty much the same:

    :::sh
    > git clone the_project
    > cd the_project
    > venv

This does everything described above with the additional step of looking for a requirements.txt file and, if it exists, running `uv pip install -r requirements.txt`, thus setting you up to work immediately.

### Working on a Project

Most of the time you're not setting up projects, you're just working on them. This is where the real benefit of this tooling  comes into play.

When you open a new terminal, you are placed in your home directory, which is very likely not where your project lives (or at least it shouldn't be). This workflow has the `workon` command which uses a simple database to map project names to their directories.

To start working on a project, you type:

    :::sh
    > workon the_project

This will change you to that directory and, by the magic of direnv, activate the virtual environment automatically, so you're ready to work!

Note that the setup below also includes tab comletion for `bash` which allows you to type `workon <tab><tab>` to see a list of possible projects.

You can switch projects at any time using the `workon` command. You do not need to deactivate the current venv or activate the new one, `direnv` takes care of all that for you.

### Removing Projects

If you want to remove a project, you can use the `rmven <project-name>` command which removes the name from the database of projects and also remove the direnv and venv settings. You should do this from the project directory.

**USE THIS COMMAND WITH CAUTION!**  It has not been tested extensively.

## The Setup

To get this workflow to operate, follow these steps:

1. Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) **and** [`direnv`](https://direnv.net/docs/installation.html).
2. Create a `~/.config/direnv/direnvrc` file with the following content shown below.  This tells `direnv` how you want it to deal with python programs and is referenced by the setup script we will create in the next step.
3. Add the large code block below to your `~/.bashrc` file.

If you like a fancy prompt on your command line, I recommend `starship` which I also use. Trey does a good job of explaining it's configuration in the article referenced at the top.

Here is the contents of `~/.config/direnv/direnvrc`:


    :::sh
    layout_python() {
        VIRTUAL_ENV="$(pwd)/.venv"
        PATH_add "$VIRTUAL_ENV/bin"
        export VIRTUAL_ENV
    }


Here's the `.bashrc` code:


    :::sh
    venv() {
        local venv_name
        local projects_file="$HOME/.projects"
        local dir_name=$(basename "$PWD")

        # If there are no arguments or the last argument starts with a dash, use dir_name
        if [ $# -eq 0 ] || [[ "${!#}" == -* ]]; then
            venv_name="$dir_name"
        else
            venv_name="${!#}"
            set -- "${@:1:$#-1}"
        fi

        # Check if .envrc already exists
        if [ -f .envrc ]; then
            echo "Error: .envrc already exists" >&2
            return 1
        fi

        if grep -Fq "^${venv_name} " ${projects_file}; then
            echo "Error: a project named ${venv_name} already exists" >&2
            return 1
        fi

        # Create venv
        if ! uv venv --quiet --seed --prompt "$venv_name" "$@" .venv; then
            echo "Error: Failed to create venv" >&2
            return 1
        fi

        source .venv/bin/activate

        # Create .envrc
        echo "layout python" > .envrc

        # Append project name and directory to projects file
        echo "${venv_name} = ${PWD}" >> $projects_file

        # Allow direnv to immediately activate the virtual environment
        direnv allow

        if [ -f requirements.txt ]; then
            # Install requirements if requirements.txt exists
            uv pip install -r requirements.txt
        fi

    }

    workon() {
        local project_name="$1"
        local projects_file="$HOME/.projects"
        local project_dir
        # Check for projects config file
        if [[ ! -f "$projects_file" ]]; then
            echo "Error: $projects_file not found" >&2
            return 1
        fi

        # Get the project directory for the given project name
        project_dir=$(grep -E "^$project_name\s*=" "$projects_file" | sed 's/^[^=]*=\s*//')

        # Ensure a project directory was found
        if [[ -z "$project_dir" ]]; then
            echo "Error: Project '$project_name' not found in $projects_file" >&2
            return 1
        fi

        # Ensure the project directory exists
        if [[ ! -d "$project_dir" ]]; then
            echo "Error: Directory $project_dir does not exist" >&2
            return 1
        fi

        # Change directories
        cd "$project_dir"
    }

    rmvenv() {
        # Remove a virtual environment
        local venv_name
        local projects_file="$HOME/.projects"
        local dir_name=$(basename "$PWD")

        # If there are no arguments or the last argument starts with a dash, use dir_name
        if [ $# -eq 0 ] || [[ "${!#}" == -* ]]; then
            venv_name="$dir_name"
        else
            venv_name="${!#}"
            set -- "${@:1:$#-1}"
            workon $venv_name
        fi

        # Check if .envrc already exists
        if [ -f .envrc ]; then
            echo "Removing .envrc"
            rm .envrc
        fi

        if [ -d .venv ]; then
            echo "Removing .venv"
            rm -rf .venv
        fi

        if [ -d .direnv ]; then
            echo "Removing .direnv"
            rm -rf .direnv
        fi

        if grep -Fq ${venv_name} ${projects_file}; then
            echo "Removing ${venv_name} from ${projects_file}"
            sed -i "/^${venv_name}/d" ${projects_file}
        fi
    }

    _workon_completions()
    {
      local projects_file="$HOME/.projects"
      # This little bit of nasty pulls the first word from each line of .projects
      x=$(awk '{ print $1 }' $projects_file)
      local suggestions=($(compgen -W "$x" -- "${COMP_WORDS[1]}"))

      if [ "${#suggestions[@]}" == "1" ]; then
        # if there's only one match, we remove the command literal
        # to proceed with the automatic completion of the number
        local project=$(echo ${suggestions[0]/%\ */})
        COMPREPLY=("$project")
      else
        # more than one suggestions resolved,
        # respond with the suggestions intact
        COMPREPLY=("${suggestions[@]}")
      fi
      return 0
    }

    # complete -o nospace -F _workon_completions workon
    complete -F _workon_completions workon

    # cuts down on the direnv chatter when running `workon`
    export DIRENV_LOG_FORMAT=
