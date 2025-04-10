import unittest
import subprocess
import re


class Test(unittest.TestCase):
    def test(self):
        result = subprocess.run(
            [
                "make",
                "-s",
                "build",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        code = result.returncode
        out = result.stdout.strip()
        err = result.stderr.strip()

        self.assertEqual(code, 0)

        self.assertIn("Hello, world!, header,3,2", out)

        expected_err_lines = [
            "bazel start //bzl:bzl",
            "Namespace\\(target='//bzl:bzl', debug=True, debug_message_limit=0, args='', shell='/bin/bash', no_build=False\\)",
            "workspace: /workspace/src/test/project/main_project",
            "command: bazel build  //bzl:bzl",
            "result: ",
            "command: bazel query 'deps\\(//bzl:bzl\\)' --output xml",
            "result: <\\?xml",
            "command: bazel cquery  --output=files //bzl:bzl",
            "result: bazel-out/k8-fastbuild/bin/bzl/libbzl.a",
            "output for cmake:",
            "/workspace/src/test/project/main_project/bzl /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/third_party/def_parser /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/tools/cpp /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/tools/cpp /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/tools/cpp /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.assert~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.assert~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.config~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.config~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container_hash~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container_hash~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.describe~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.describe~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.intrusive~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.intrusive~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.move~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.move~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.mp11~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.mp11~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.static_assert~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.static_assert~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.type_traits~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.type_traits~/include /workspace/src/test/project/main_project/bazel-out/k8-fastbuild/bin/bzl",
            "bazel end //bzl:bzl",
            "bazel start //:world",
            "Namespace\\(target='//:world', debug=True, debug_message_limit=1550, args='--config=warnings -c dbg', shell='/bin/bash', no_build=False\\)",
            "workspace: /workspace/src/test/project/bzl_world",
            "command: bazel build --config=warnings -c dbg //:world",
            "result: ",
            "command: bazel query 'deps\\(//:world\\)' --output xml",
            "result: <\\?xml",
            "command: bazel cquery --config=warnings -c dbg --output=files //:world",
            "result: bazel-out/k8-dbg/bin/libworld.a",
            "output for cmake:",
            "/workspace/src/test/project/bzl_world /workspace/src/test/project/bzl_world/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/third_party/def_parser /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/tools/cpp /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/tools/cpp /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/bazel_tools/tools/cpp /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.assert~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.assert~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.config~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.config~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container_hash~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container_hash~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.container~/include /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.describe~ /(.+)/.cache/bazel/_bazel_(.+)/(.+)/external/boost.describe~/...",
            "bazel end //:world",
        ]

        for line in expected_err_lines:
            if not re.search(line, err):
                self.fail(line)

        not_expected_err_lines = [
            "bazel start //:header",
            "bazel end //:header",
        ]

        for line in not_expected_err_lines:
            if re.search(line, err):
                self.fail(line)


if __name__ == "__main__":
    unittest.main()
