"""
Command line interface driver for snakemake workflows
"""
import argparse
import os.path
import snakemake
import sys
import yaml
import time
import shutil
import errno

# read from __init__.py
from . import __program__
from . import __version__
from . import __email__
from . import __date__
from . import __author__

# global vars
thisdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.join(thisdir, "..")
cwd = os.getcwd()

# non-standard lib: For color handling on the shell
try:
    from colorama import init, Fore

    # INIT color
    # Initialise colours for multi-platform support.
    init()
    reset = Fore.RESET
    colors = {
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": "",
    }
except ImportError:
    sys.stderr.write(
        "colorama lib desirable. " + 'Install with "conda install colorama".\n\n'
    )
    reset = ""
    colors = {"success": "", "error": "", "warning": "", "info": ""}


def alert(atype, text, log, repeat=False, flush=False):
    if repeat:
        textout = "{} [{}] {}\r".format(
            time.strftime("%Y%m%d-%H:%M:%S"), atype.rjust(7), text
        )
    else:
        textout = "{} [{}] {}\n".format(
            time.strftime("%Y%m%d-%H:%M:%S"), atype.rjust(7), text
        )

    log.write("{}{}{}".format(colors[atype], textout, reset))
    if flush:
        log.flush()
    if atype == "error":
        sys.exit(1)


def success(text, log=sys.stderr, flush=True):
    alert("success", text, log, flush=flush)


def error(text, log=sys.stderr, flush=True):
    alert("error", text, log, flush=flush)


def warning(text, log=sys.stderr, flush=True):
    alert("warning", text, log, flush=flush)


def info(text, log=sys.stderr, repeat=False, flush=True):
    alert("info", text, log, repeat=repeat, flush=flush)


def print_logo():
    try:
        from pyfiglet import figlet_format

        text = figlet_format(__program__, font="slant")
    except ImportError:
        text = "\n\t\t{}\n\n".format(__program__)
    sys.stdout.write("{}\n".format("*" * 60))
    sys.stdout.write(text)
    sys.stdout.write("version: {}  date: {}\n".format(__version__, __date__))
    sys.stdout.write("Using executable at: {}\n".format(thisdir))
    sys.stdout.write("{}\n\n".format("*" * 60))


def parse_cmdline():
    description = "An Snakemake command line interface for metafunc."
    version = "version {}, date {}".format(__version__, __date__)
    epilog = "Copyright {} ({})".format(__author__, __email__)

    parser = argparse.ArgumentParser(
        prog=__program__, description=description, epilog=epilog,
    )

    parser.add_argument("--version", action="version", version="{}".format(version))

    subparsers = parser.add_subparsers(dest="subparser_name")

    p_config = subparsers.add_parser("help", description="Print help.",)
    p_config = subparsers.add_parser(
        "setup",
        description="Generate a directory with example files "
        + "for a metafunc run.",
    )
    p_config.add_argument(
        "-n",
        "--name",
        dest="directoryname",
        default="example",
        help='Directory name (not full path). [default: "example"]',
    )

    p_run = subparsers.add_parser(
        "run", description="Run metafunc analysis."
    )
    p_run.add_argument(
        "configfile",
        metavar="CONFIG-FILE",
        help='Config-file. Generate example with "metafunc setup"',
    )
    p_run.add_argument("-n", "--dry-run", action="store_true")
    p_run.add_argument("-f", "--force", action="store_true")

    # if no arguments supplied print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args, parser


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def main(sysargs=sys.argv[1:]):
    print_logo()
    args, parser = parse_cmdline()

    if args.subparser_name == "help":
        parser.print_help()
        desc = """
Description
-----------

Run `metafunc setup` to generate an example directory with
resources to make a metafunc run.

Enter the directory and edit the config.yaml file to your
project requirements.

Run `metafunc run config.yaml` from within the created
directory.
"""

        sys.stdout.write(desc)
        sys.exit(0)

    elif args.subparser_name == "setup":
        dest = os.path.join(cwd, args.directoryname)
        sys.stdout.write(f"{__program__} setup:\n")
        sys.stdout.write(
            "\tExecution time: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        sys.stdout.write(f"\tDestination: {dest}\n")
        sys.stdout.write("{}\n".format("*" * 60))
        # test if already there
        if os.path.exists(dest):
            error(f'Destination example directory at "{dest}" already exists. EXIT.')

        src = os.path.join(thisdir, "example")  
        copyanything(src, dest)
        success(
            f"Example directory for a metafunc "
            + f'run created at: "{dest}".'
        )
        return 0
    elif args.subparser_name == "run":
        # first, find the Snakefile
        snakefile_this = os.path.join(thisdir, "Snakefile")
        snakefile_parent = os.path.join(parentdir, "Snakefile")
        if os.path.exists(snakefile_this):
            snakefile = snakefile_this
        elif os.path.exists(snakefile_parent):
            snakefile = snakefile_parent
        else:
            msg = "Error: cannot find Snakefile at any of the following locations:\n"
            msg += "{}\n".format(snakefile_this)
            msg += "{}\n".format(snakefile_parent)
            error(msg)

        # next, find the workflow params file
        if not os.path.exists(args.configfile):
            error(f"Error: cannot find configfile {args.configfile}\n. EXIT.")

        sys.stdout.write(f"{__program__} run:\n")
        sys.stdout.write(
            "\tExecution time: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        sys.stdout.write(f"\tSnakefile: {snakefile}\n")
        sys.stdout.write(f"\tConfig-file: {os.path.abspath(args.configfile)}\n")
        sys.stdout.write("{}\n".format("*" * 60))

        config = yaml.safe_load(open(args.configfile))

        # run snakemake
        status = snakemake.snakemake(
            snakefile,
            configfiles=[args.configfile],
            printshellcmds=True,
            dryrun=args.dry_run,
            forceall=args.force,
            use_singularity=config["use_singularity"],
            singularity_args=config["singularity_args"],
            use_conda=config["use_conda"],
            cores=config["cores"],
            # config=config,
        )

        if status:  # translate "success" into shell exit code of 0
            success(f"Run finished successfully.")
            return 0
        return 1
    else:
        error("Mode not recognized. EXIT")
        return 1


if __name__ == "__main__":
    main()
