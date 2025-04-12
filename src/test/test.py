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

        # Remove generated paths
        cleaned_out = re.sub(
            r'python3 /workspace/src/bazel-to-cmake-integration/bazel\.py /.+?/temp\.xml',
            'python3 /workspace/src/bazel-to-cmake-integration/bazel.py /workspace/build/temp.xml',
            out
        )
        # Remove everything between the last "END" and the executable output
        end_match = list(re.finditer(r'^-- END: .*$', cleaned_out, re.MULTILINE))
        last_end = end_match[-1].end()
        cleaned_out = cleaned_out[:last_end]

        expected = """-- START: hello -> //bzl:bzl
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

        self.maxDiff = None
        self.assertMultiLineEqual(cleaned_out.strip(), expected.strip())

        self.assertEqual(err, "")


if __name__ == "__main__":
    unittest.main()
