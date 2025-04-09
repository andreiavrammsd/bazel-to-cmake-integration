import os
import subprocess
import pathlib
import sys
import argparse


class Bazel:
    debug_is_on: bool
    debug_message_limit: int
    workspace: str
    shell: str

    def __init__(
        self, debug_is_on: bool, debug_message_limit: int, workspace: str, shell: str
    ):
        self.debug_is_on = debug_is_on
        self.debug_message_limit = debug_message_limit
        self.workspace = workspace
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

    def get_includes(self, target: str, args: str):
        cmd = f"bazel info {args} output_base"
        output_base = self.__run(cmd)

        cmd = f"bazel query 'deps({target})'"  # --output package
        deps = self.__run(cmd).split()

        includes = {}

        for dep in deps:
            if dep.startswith("@@") and "//:" in dep:
                start = 2
                end = dep.find("//:", start)
                path = os.path.join(output_base, "external", dep[start:end], "include")
                includes[path] = True
            elif dep.startswith("@") and "//:" in dep:
                path = os.path.join(
                    output_base, "external", dep.split("//:")[1] + "~", "include"
                )
                if pathlib.Path(path).is_dir():
                    includes[path] = True
            elif dep.startswith("//"):  # //:
                path = pathlib.Path(dep.strip("//:"))
                include = os.path.join(
                    self.workspace, path.parts[0] if len(path.parts) > 1 else ""
                )
                includes[include] = True

                start = dep.find("//") + 2
                end = dep.find(":", start)
                root = os.path.join(self.workspace, dep[start:end])
                includes[root] = True

        return list(includes.keys())

    def get_link_directories(self, target: str, args: str):
        cmd = f"bazel cquery {args} --output=files {target} 2>/dev/null"  # 2>/dev/null?
        libraries = self.__run(cmd).split()

        # workspace = self.__run(f"bazel info {args} workspace")
        # if workspace != self.workspace:
        #     self.debug("buba")
        #     self.debug(self.workspace)
        #     self.debug(workspace)

        directories = {}
        for library in libraries:
            directory = os.path.join(
                self.workspace, pathlib.Path(library).parent.as_posix()
            )
            directories[directory] = True

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

    include_directories = bazel.get_includes(args.target, args.args)
    link_directories = bazel.get_link_directories(args.target, args.args)
    directories = " ".join(include_directories + link_directories)
    bazel.debug(f"\noutput for cmake:\n{directories}\n")

    print(directories)

    bazel.debug(f"bazel end {args.target}\n")


if __name__ == "__main__":
    main()
