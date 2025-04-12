import unittest
import subprocess


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

        expected_debug_out = """-- START: hello -> //bzl:bzl
-- WORKSPACE: /workspace/src/test/project/main_project
-- BAZEL ARGUMENTS: 
-- BAZEL BUILD TARGET: ON
-- bazel build  //bzl:bzl
-- bazel query deps(//bzl:bzl) --output xml
-- python3 /workspace/src/bazel-to-cmake-integration/bazel.py /workspace/build/temp.xml
-- bazel cquery  --output=files //bzl:bzl
-- END: hello -> //bzl:bzl

-- START: hello -> //:world
-- WORKSPACE: /workspace/src/test/project/bzl_world
-- BAZEL ARGUMENTS: --config=warnings -c dbg
-- BAZEL BUILD TARGET: ON
-- bazel build --config=warnings -c dbg //:world
-- bazel query deps(//:world) --output xml
-- python3 /workspace/src/bazel-to-cmake-integration/bazel.py /workspace/build/temp.xml
-- bazel cquery --config=warnings -c dbg --output=files //:world
-- END: hello -> //:world"""
        self.assertIn(expected_debug_out, out)

        not_expected_debug_out = """-- START: hello -> //:header
-- WORKSPACE: /workspace/src/test/project/bzl_header_only
-- BAZEL ARGUMENTS: -c opt
-- BAZEL BUILD TARGET: OFF
-- bazel query deps(//:header) --output xml
-- python3 /workspace/src/bazel-to-cmake-integration/bazel.py /workspace/build/temp.xml
-- bazel cquery -c opt --output=files //:header
-- END: hello -> //:header"""
        self.assertNotIn(not_expected_debug_out, out)

        expected_executable_out = "Hello, world!, header,3,2"
        self.assertIn(expected_executable_out, out)

        self.assertEqual(err, "")


if __name__ == "__main__":
    unittest.main()
