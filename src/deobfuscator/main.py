# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from cli import App


def main():
    parser = argparse.ArgumentParser(
        description="88 Deobfuscator – remove various Python obfuscation layers."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Path to the obfuscated Python file (or .zip for ChristianObf). "
             "Required unless --list is used."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file for the deobfuscated code. "
             "Default: decoded_<input_filename>.py"
    )
    parser.add_argument(
        "-m", "--method",
        help="Force a specific deobfuscation method (use --list to see all). "
             "Default: auto (automatic detection)."
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all supported obfuscation methods and exit."
    )

    args = parser.parse_args()

    if not args.input_file and not args.list:
        parser.error("input_file is required unless --list is used")

    try:
        app = App()
        app.run(args)
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
