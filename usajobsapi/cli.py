"""
Command line interface for the python-usajobsapi package.

This module builds the argument parser that powers the `usajobsapi`
executable, handling global configuration common to every subcommand.
"""

from __future__ import annotations

import argparse
import sys

from usajobsapi._version import __title__ as pkg_title
from usajobsapi._version import __version__ as pkg_version
from usajobsapi.client import USAJobsClient


def build_parser() -> argparse.ArgumentParser:
    """Create the top-level argument parser for the CLI."""
    client_defaults = USAJobsClient()
    parser = argparse.ArgumentParser(
        prog=pkg_title,
        description="USAJOBS REST API Command Line Interface.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {pkg_version}",
        help="Display the package version.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=client_defaults.timeout,
        metavar="SECONDS",
        help="Request timeout in seconds. Defaults to the client default.",
    )
    parser.add_argument(
        "-A",
        "--user-agent",
        dest="auth_user",
        default=client_defaults.headers["User-Agent"],
        metavar="EMAIL",
        help="Email address associated with the API key (User-Agent header).",
    )
    parser.add_argument(
        "--auth-key",
        dest="auth_key",
        default=client_defaults.headers["Authorization-Key"],
        metavar="KEY",
        help="API key used for authenticated requests.",
    )
    parser.add_argument(
        "--no-ssl-verify",
        dest="ssl_verify",
        action="store_false",
        default=client_defaults.ssl_verify,
        help="Disable TLS certificate verification.",
    )
    return parser


def main() -> None:
    if "--version" in sys.argv:
        print(pkg_version)
        sys.exit(0)

    parser = build_parser()
    parser.parse_args(sys.argv)
