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
        self.assertEqual(err, "")

        # Normalize dynamic paths
        normalized = re.sub(
            r'python3 /workspace/src/bazel-to-cmake-integration/bazel\.py /.+?/temp\.xml',
            'python3 /workspace/src/bazel-to-cmake-integration/bazel.py /workspace/build/temp.xml',
            out
        )

        # Extract debug entries
        pattern = re.compile(r"-- START:.*?-- END:.*?(?=\n|$)", re.DOTALL)
        debug_entries = pattern.findall(normalized)
        actual_cleaned = "\n\n".join(debug_entries)

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
        self.assertEqual(actual_cleaned.strip(), expected.strip())


if __name__ == "__main__":
    unittest.main()
