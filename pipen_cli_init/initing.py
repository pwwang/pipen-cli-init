import logging
import tarfile
from pathlib import Path
from typing import Any, Mapping

import toml
from cmdy import bash, pip, poetry
from liquid import Liquid
from rich.logging import RichHandler

HERE = Path(__file__).parent
TARGET_DIR = Path(".").resolve()

logger = logging.getLogger("PIPEN-CLI-INIT")
logger.setLevel(logging.INFO)
_handler = RichHandler(show_time=False, show_path=False, markup=True)
_handler.setFormatter(
    logging.Formatter("[[magenta]%(name)s[/magenta]] %(message)s")
)
logger.addHandler(_handler)


def check_dir_empty(args: Mapping[str, Any]) -> bool:
    """Make sure the current directory is empty"""
    if len(list(Path(".").glob("*"))) > 0:
        logger.error("Directory is not empty.")
        return False
    return True


def write_pyproject_toml(args: Mapping[str, Any]) -> None:
    """Write pyproject.toml"""
    logger.info("Creating pyproject.toml ...")
    with HERE.joinpath("deps.toml").open() as fdep:
        deps = toml.load(fdep)

    if not args.report:
        del deps.report

    pyp = {
        "build-system": {
            "requires": ["poetry-core>=1.0.0"],
            "build-backend": "poetry.core.masonry.api",
        },
        "tool": {
            "poetry": {
                "name": args.name,
                "description": "A pipen pipeline.",
                "authors": ["ABC <abc@example.com>"],
                "version": "1.0.0",
                "dependencies": deps,
                "dev-dependencies": {},
            }
        },
    }
    if args.bin:
        pyp["tool"]["poetry"]["scripts"] = {
            args.name: f"{args.name.replace('-', '_')}.pipeline:main"
        }

    with TARGET_DIR.joinpath("pyproject.toml").open("w") as fpyp:
        toml.dump(pyp, fpyp)


def write_readme(args: Mapping[str, Any]) -> None:
    """Write an sample README.md file"""
    with TARGET_DIR.joinpath("README.md").open("w") as frm:
        frm.write(f"# {args.name}\n")


def create_pyfiles(args: Mapping[str, Any]) -> None:
    """Create python files

    __init__.py: python __init__ file
    __main__.py: main file for `python -m` to run
    pipeline.py: The pipeline entry file
    args.py: CLI arguments handling
    processes.py: The processes
    scripts: The scripts for processes
    reports: The report template if `args.report` is True
    """
    logger.info("Creating module directory ...")
    pydir = TARGET_DIR / args.name.replace("-", "_")
    pydir.mkdir()

    tpldir = HERE / "templates"

    logger.info("Creating __init__.py ...")
    initpy = pydir / "__init__.py"
    initpy.write_text("")

    logger.info("Creating __main__.py ...")
    mainpy = pydir / "__main__.py"
    tplmainpy = tpldir / "main.py.tpl"
    mainpy.write_bytes(tplmainpy.read_bytes())

    logger.info("Creating pipeline.py ...")
    pipelinepy = pydir / "pipeline.py"
    tplpipelinepy = tpldir / "pipeline.py.tpl"
    pipelinepy.write_bytes(tplpipelinepy.read_bytes())

    logger.info("Creating args.py ...")
    argspy = pydir / "args.py"
    tplargspy = Liquid(tpldir / "args.py.tpl")
    argspy.write_text(
        tplargspy.render(
            progname=args.name
            if args.bin
            else f"python -m {args.name.replace('-', '_')}"
        )
    )

    logger.info("Creating processes.py ...")
    processespy = pydir / "processes.py"
    tplprocessespy = Liquid(tpldir / "processes.py.tpl")
    processespy.write_text(tplprocessespy.render(report=args.report))

    scriptsdir = pydir / "scripts"
    scriptsdir.mkdir()

    logger.info("Creating script for process Example ...")
    hwscript = scriptsdir / "Example.sh"
    tplhwscript = tpldir / "Example.sh.tpl"
    hwscript.write_bytes(tplhwscript.read_bytes())

    if args.report:
        reportsdir = pydir / "reports"
        reportsdir.mkdir()

        logger.info("Creating report template for process Example ...")
        hwreport = reportsdir / "Example.svelte"
        tplhwreport = tpldir / "Example.svelte.tpl"
        hwreport.write_bytes(tplhwreport.read_bytes())


def install(args) -> None:
    """Install the project, so we can run the pipeline via
    the binary (named `<args.name>`) or `python -m <args.name>`
    """
    if args.install == "dont":
        return

    if args.install == "poetry":
        poetry.install()

    else:
        logger.info("Installing the pipeline ...")
        logger.info("- Runing poetry build ...")
        poetry.build()

        logger.info("- Exacting files from the build ...")
        version = poetry.version(s=True).stdout.strip()
        targz = Path("./dist") / f"{args.name}-{version}.tar.gz"
        targz = tarfile.open(targz)
        targz.extractall(Path("./dist"))

        logger.info("- Linking setup.py ...")
        setuppy = Path("./setup.py")
        if setuppy.exists():
            setuppy.unlink()
        setuppy.symlink_to(
            Path("./dist") / f"{args.name}-{version}" / "setup.py"
        )

        logger.info("- Installing using pip ...")
        instcmd = pip.install(upgrade=True, e=True, _=["."], _raise=False)
        if instcmd.rc != 0:
            logger.warning("  Failed with pip installation directly")
            logger.info("- Running the installation command directly")
            cmd = instcmd.stderr.splitlines()[1].strip()
            if not cmd.startswith("command: "):
                logger.error("  Cannot extract command:")
                for err in instcmd.stderr.splitlines():
                    logger.error(f"  {err}")
                return
            cmd = cmd[9:]
            bash(c=cmd)
