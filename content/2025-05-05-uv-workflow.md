Title: My New `uv` Workflow
----------------------

I've recently changed my python project workflow based on a great write-up by [Trey Hunner](https://treyhunner.com/2024/10/switching-from-virtualenvwrapper-to-direnv-starship-and-uv/).

Trey did a great job of explaining the details of what `uv` is and why you might want to use it, and also set up some scripts for zsh to recreate a workflow that is quite similar to what I've been using for several years.

I have shamelessly copied his work, ported it to bash ('cause I'm old-school) and expanded it a bit.

## The Workflow

Before going into the details of how to set up this system, I'll walk you through what it looks like in operation. There are three commands, one used when creating a new project, one used in normal, day-to-day operations, and one primarily for debugging things.

To set up a new project in this workflow, you first need to `cd` to the project's directory. It doesn't matter if it already exists, usually for me it does, but it can be an empty directory, too.

Once you're in the project directory, you then use the `venv` command (which is shown below in a custom bash script) to create the virtual environment, set up `direnv` to use this directory, and install the `requirement.txt` file if it's present.

The `venv` script also does a little bookkeeping in the background to help with the second command, the day-to-day one, `workon`.

To use the `workon` command (again, shown in the next section), you simply type `workon` followed by the name of the project. The command will change to you to project's directory and activate the virtualenvironment for you.

Finally, for completeness (and to help me debug things while setting this up), there is the `rmvenv` which attempts to remove all traces left by the `venv` command.

## The Setup

To get this workflow to operate, you will need to install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) **and** [`direnv`](https://direnv.net/docs/installation.html).

From there you can add the code snippet below to your `.bashrc` file (or however you like to have these things) and source that file.

In his article, Trey also goes into detail about using `starship` which I also use, but I feel that, while that's pretty cool, it's not completely necessary to getting this workflow running.

If you're interested in making your prompt look cool with python venv and version info, I'd recommand starship and Trey's article referenced above.

Without further ado, here's the code, which can also be found [here](https://github.com/jima80525/bin/blob/ae2dee4a786dd264b07092021ef2092dfec3c198/bashrc_to_copy_to_home_dir#L91)

```bash
# direnv functions to give venv and workon commands from:
# https://treyhunner.com/2024/10/switching-from-virtualenvwrapper-to-direnv-starship-and-uv/
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

    if grep -Fq ${venv_name} ${projects_file}; then
        echo "Error: a project named ${venv_name} already exists" >&2
        return 1
    fi

    # Create venv
    if ! uv venv --seed --prompt "$venv_name" "$@" .venv; then
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
        pip install -r requirements.txt
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
```
