from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from pathlib import Path
from pipen.cli._hooks import AsyncCLIPlugin
from copier import run_copy

__version__ = "1.1.0"

if TYPE_CHECKING:
    from argx import ArgumentParser, Namespace

TEMPLATE_PATH = Path(__file__).parent.joinpath("template")


class PipenCliInit(AsyncCLIPlugin):
    """Initialize a pipen project (pipeline)"""
    name = "init"
    version = __version__

    def __init__(
        self,
        parser: ArgumentParser,
        subparser: ArgumentParser,
    ) -> None:
        super().__init__(parser, subparser)
        self.subparser.add_argument(
            "dir",
            nargs="?",
            default="./",
            help="The directory to create the project in",
            type="panpath",
        )

    async def exec_command(self, args: Namespace) -> None:
        """Run the command"""
        dest_dir = await args.dir.a_resolve()
        print("✅ \033[1mCreating/Updating pipen project in:\033[0m")
        print(f"   \033[4m{dest_dir}\033[0m")
        print(
            "   (You can change the directory by running `pipen init <dir>`)"
        )
        # Run copier in a thread pool to avoid event loop conflicts
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            run_copy,
            str(TEMPLATE_PATH),
            str(dest_dir),
        )
