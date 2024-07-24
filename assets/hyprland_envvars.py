#!/usr/bin/python

"""
Move all environment variables from /etc/environment to hyprland.conf

.. codeauthor: Jaden <git@jaden.rs>
"""
import argparse
from pathlib import Path


def main(home_dir: Path, check_mode: bool) -> int:
    non_envvars: list[str] = []
    envvars: list[tuple[str, str]] = []
    hyprland_conf = home_dir / ".config" / "hypr" / "hyprland.conf"
    etc_env = Path("/etc/environment")
    if not etc_env.exists():
        print("The file /etc/environment does not exist.")
        return 1
    if not hyprland_conf.exists():
        print("The Hyprland conf file does not exist.")
        return 1
    with etc_env.open("r") as f:
        data = f.readlines()
    for line in data:
        if line[0] == "#":
            non_envvars.append(line)
        else:
            envvar_name, envvar_val = line.split("=")
            if not isinstance(envvar_val, str):
                envvar_val = "=".join(envvar_val)
            envvars.append((envvar_name, envvar_val))
    if check_mode:
        print("Found the following envionment variables:")
        for name, value in envvars:
            print(f"\t{name}={value.strip()}")
        return 0

    with etc_env.open("w") as f:
        f.writelines(non_envvars)

    with hyprland_conf.open("a") as f:
        f.writelines(f"env = {name},{value}" for name, value in envvars)
        
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move contents of /etc/environment to hyperland.conf"
    )
    parser.add_argument(
        "homedir", type=Path, help="Home directory of the user"
    )
    parser.add_argument(
        "--check", action="store_true", help="Do not change any files"
    )
    args = parser.parse_args()
    raise SystemExit(main(args.homedir, args.check))
