"""Provides the plugin"""

import re
import sys
from typing import Any, Mapping

from pipen.cli import CLIPlugin
from pyparam import Params

from .initing import (
    check_dir_empty,
    create_pyfiles,
    install,
    write_readme,
    write_pyproject_toml,
    TARGET_DIR,
)

PROJNAME_RE = re.compile(f"[A-Za-z][\w_-]*")

class PipenCliInit(CLIPlugin):
    """Initialize a pipen project (pipeline)"""

    from .version import __version__

    name: str = "init"

    @property
    def params(self) -> Params:
        """Add command"""
        pms = Params(
            desc=self.__class__.__doc__,
            help_on_void=False,
        )
        pms.add_param(
            "n,name",
            default=TARGET_DIR.name,
            desc="Name of your project, must be a valid python module name.",
            callback=lambda val: (
                ValueError("Not a valid project name")
                if not PROJNAME_RE.match(val)
                else val
            )
        )
        pms.add_param(
            "b,bin",
            type=bool,
            default=False,
            desc="Create executable script (named `<name>`) with installation, "
            "otherwise your pipeline should be running via `python -m <name>`",
        )
        pms.add_param(
            "r,report",
            type=bool,
            default=True,
            desc="Need to generate reports for your pipeline?",
        )
        pms.add_param(
            "install",
            type="choice",
            choices=["poetry", "pip-e", "dont"],
            default="poetry",
            desc=(
                "How to install the pipeline after creation:",
                "- `poetry`: Install using poetry. You can run your pipeline "
                "using poetry",
                "- `pip-e`: Install using `pip install -e`. You can your "
                "pipeline directly",
                "- `dont`: Do not install the pipeline."
            ),
        )
        return pms

    def exec_command(self, args: Mapping[str, Any]) -> None:
        """Execute the command"""

        if not check_dir_empty(args):
            sys.exit(1)
        write_readme(args)
        write_pyproject_toml(args)
        create_pyfiles(args)
        install(args)
