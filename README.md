# pipen-cli-init

A [`pipen`][1] cli plugin to create a pipen project (pipeline)

## Installation

```shell
pip install -U pipen-cli-init
```

## Enablig/Disabling the plugin

Installing this plugin will enable it, and uninstalling will disable it.

## Usage

```shell
❯ pipen init --help
Usage: pipen init [-h] [dir]

Initialize a pipen project (pipeline)

Optional Arguments:
  -h, --help  show help message and exit

Positional Arguments:
  dir         The directory to create the project in [default: ./]
```

## Example

```shell
> cd example-pipeline/
> pipen init
> # answer the questions
> # after the project is created, install the dependencies
> poetry install
> # run the pipeline
> poetry run python -m <pipeline_name>
> # or if you choose console_script to be True
> poetry run <pipeline_name>
```

If you want to publish the pipeline:

```shell
poetry publish --build
```

Then you can install it and run the pipeline globally:

```shell
> python -m <pipeline_name>
> # or if you choose console_script to be True
> <pipeline_name>
```

[1]: https://github.com/pwwang/pipen
