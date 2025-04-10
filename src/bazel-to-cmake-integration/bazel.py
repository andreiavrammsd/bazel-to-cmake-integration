import os
import subprocess
import pathlib
import sys
import argparse
import xml.etree.ElementTree as ET


class Bazel:
    debug_is_on: bool
    debug_message_limit: int
    workspace: pathlib.Path
    shell: str

    def __init__(
        self, debug_is_on: bool, debug_message_limit: int, workspace: str, shell: str
    ):
        self.debug_is_on = debug_is_on
        self.debug_message_limit = debug_message_limit
        self.workspace = pathlib.Path(workspace)
        self.shell = shell

    def debug(self, message):
        if self.debug_is_on:
            message = str(message)

            if self.debug_message_limit > 0 and len(message) > self.debug_message_limit:
                message = f"{message[0:self.debug_message_limit]}...\n"

            print(message, file=sys.stderr)

    def build(self, target: str, args: str):
        cmd = f"bazel build {args} {target}"
        self.__run(cmd)

    def get_include_directories(self, target: str, args: str):
        cmd = f"bazel query 'deps({target})' --output xml"
        deps = self.__run(cmd)

        root = ET.fromstring(deps)
        directories = []

        for node in root.iter("rule"):
            if node.get("class") == "cc_library":
                location = node.get("location")
                includes = [include.get('value') for include in node.findall(".//list[@name='includes']/string")]

                root = pathlib.Path(location).parent
                directories.append(root.as_posix())

                for dep_include in includes:
                    directories.append((root / pathlib.Path(dep_include)).as_posix())

        return directories
   
    def get_link_directories(self, target: str, args: str):
        cmd = f"bazel cquery {args} --output=files {target}"
        files = self.__run(cmd).split()

        directories = {}
        for file in files:
            directory = self.workspace / pathlib.Path(file).parent
            directories[directory.as_posix()] = True

        return list(directories.keys())

    def __run(self, cmd: str):
        self.debug(f"command: {cmd}")

        out = subprocess.run(
            cmd,
            check=True,
            shell=True,
            executable=self.shell,
            capture_output=True,
            text=True,
            cwd=self.workspace,
        ).stdout.strip()

        self.debug(f"result: {out}\n")

        return out


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        type=str,
        help="Bazel target to use",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information",
        default=False,
    )
    parser.add_argument(
        "--debug-message-limit",
        type=int,
        help="Print debug information",
        default=200,
    )
    parser.add_argument(
        "--args",
        type=str,
        help="Arguments as string for bazel build",
        default="",
    )
    parser.add_argument(
        "--shell",
        type=str,
        help="Shell executable",
        default="/bin/bash",
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Whether to build the target",
        default=False,
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    workspace = os.getcwd()
    bazel = Bazel(args.debug, args.debug_message_limit, workspace, args.shell)

    bazel.debug(f"bazel start {args.target}\n")
    bazel.debug(args)
    bazel.debug(f"workspace: {workspace}")

    if args.no_build is False:
        bazel.build(args.target, args.args)

    include_directories = bazel.get_include_directories(args.target, args.args)
    link_directories = bazel.get_link_directories(args.target, args.args)
    directories = " ".join(include_directories + link_directories)
    bazel.debug(f"\noutput for cmake:\n{directories}\n")

    print(directories)

    bazel.debug(f"bazel end {args.target}\n")


if __name__ == "__main__":
    main()
