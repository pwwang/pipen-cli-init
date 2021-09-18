# pipen-cli-init

A [`pipen`][1] cli plugin to create a pipen project (pipeline)

## Installation

```
pip install -U pipen-cli-init
```

## Enablig/Disabling the plugin

Installing this plugin will enable it, and uninstalling will disable it.

## Usage

```
❯ pipen init --help

DESCRIPTION:
  Initialize a pipen project (pipeline)

USAGE:
  pipen init [OPTIONS]

OPTIONAL OPTIONS:
  -n, --name <STR>                - Name of your project, must be a valid python
                                    module name. Default: pipen-cli-init
  -b, --bin [BOOL]                - Create executable script (named <name>)
                                    with installation, otherwise your pipeline
                                    should be running via python -m <name>
                                    Default: False
  -r, --report [BOOL]             - Need to generate reports for your pipeline?
                                    Default: True
  --install <CHOICE>              - How to install the pipeline after creation:
                                    Default: poetry
                                    - poetry: Install using poetry. You can
                                    run your pipeline using poetry
                                    - pip-e: Install using pip install -e.
                                    You can your pipeline directly
                                    - dont: Do not install the pipeline.
  -h, --help                      - Print help information for this command
```

This tool will create a project under current directory (requires empty). The python module will be created at `./<name>`. If `<name>` has dash (`-`) in it, it will be replaced with `_`.

To run your pipeline, you can do:

```
> python -m <name>
```

If your pipeline is not installed (`--install dont`), you have to run it under your project directory. But if you want to run it anywhere, you have to install it using `--install pip-e`.

If you don't want to pollute the global environment, you can use `poetry` to install it. This will create a virtual enviornment, and install the dependencies there. To run you pipeline:

```
> poetry run python -m <name>
```

Or enter poetry shell first and then run your pipeline:

```
> poetry shell
(poetry shell)> python -m <name>
```

If you want to install a executable script for your pipeline, use `--bin`.
Then you can run your pipeline directly:

```
> <name> --help
```



[1]: https://github.com/pwwang/pipen

