import re
import sys
from typing import TYPE_CHECKING, Any, Mapping

from pipen.cli import cli_plugin

from .initing import (
    check_dir_empty,
    create_pyfiles,
    install,
    write_readme,
    write_pyproject_toml,
    TARGET_DIR,
)

if TYPE_CHECKING:
    from pyparam import Params

COMMAND = "init"
PROJNAME_RE = re.compile(f"[A-Za-z][\w_-]*")

class PipenCliInit:
    """A pipen cli plugin to create pipen project"""

    from .version import __version__

    @cli_plugin.impl
    def add_commands(self, params: "Params") -> None:
        """Add command"""
        command = params.add_command(
            COMMAND,
            "Initialize a pipen project (pipeline)",
            help_on_void=False,
        )
        command.add_param(
            "n,name",
            default=TARGET_DIR.name,
            desc="Name of your project, must be a valid python module name.",
            callback=lambda val: (
                ValueError("Not a valid project name")
                if not PROJNAME_RE.match(val)
                else val
            )
        )
        command.add_param(
            "b,bin",
            type=bool,
            default=False,
            desc="Create binary executable (named `<name>`) with installation, "
            "otherwise your pipeline should be running via `python -m <name>`",
        )
        command.add_param(
            "r,report",
            type=bool,
            default=True,
            desc="Need to generate reports for your pipeline?",
        )
        command.add_param(
            "noinstall",
            type=bool,
            default=False,
            desc="Do not install the project after initialization. "
            "By default, the project will be installed using pip editable mode",
        )

    @cli_plugin.impl
    def exec_command(self, command: str, args: Mapping[str, Any]) -> None:
        """Execute the command"""
        if command != COMMAND:
            return

        if not check_dir_empty(args):
            sys.exit(1)
        write_readme(args)
        write_pyproject_toml(args)
        create_pyfiles(args)
        install(args)
