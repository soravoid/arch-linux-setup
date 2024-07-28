#!/usr/bin/env python3
import argparse
from pathlib import Path


def main(profile_name: str, firefox_folder: Path) -> int:
    if not firefox_folder.is_dir():
        print("provided path is not a directory.")
        return 1
    for item in firefox_folder.iterdir():
        if not item.is_dir():
            continue
        if item.name.endswith(f".{profile_name}"):
            print(str(item))
            return 0
    else:
        print(f"no profile named '{profile_name}'")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print firefox profile folder name given firefox folder."
    )
    parser.add_argument(
        "profile_name",
        type=str,
        help="Name of desired firefox profile"
    )
    parser.add_argument(
        "firefox_folder",
        type=Path,
        help="Path to the firefox config folder"
    )
    args = parser.parse_args()
    raise SystemExit(main(args.profile_name, args.firefox_folder))
