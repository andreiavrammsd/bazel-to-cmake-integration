import unittest
import subprocess
import re
import os


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

        self.assertEqual(code, 0, err)
        self.assertIn("Hello, world!, header,3,2", out)
        self.assertEqual(err, "")

        # Extract debug entries
        pattern = re.compile(r"-- START:.*?-- END:.*?(?=\n|$)", re.DOTALL)
        debug_entries = pattern.findall(out)
        actual_cleaned = "\n\n".join(debug_entries)

        expected_bazel_exec = f"bazel-{os.environ["BAZEL_VERSION"]}" if os.environ["BAZEL_VERSION"] else "bazel"
        expected = f"""-- START: hello -> //bzl:bzl
-- WORKSPACE: /workspace/src/test/project/main_project
-- BAZEL ARGUMENTS: 
-- BAZEL BUILD TARGET: ON
-- {expected_bazel_exec} build  //bzl:bzl
-- {expected_bazel_exec} query deps(//bzl:bzl) --output xml
-- python3 -c "
import sys
import pathlib
import xml.etree.ElementTree as ET

root = ET.fromstring(sys.stdin.read())

for node in root.iter('rule'):
    if node.get('class') == 'cc_library':
        base = pathlib.Path(node.get('location')).parent
        print(base.as_posix())
        for i in node.findall('.//list[@name="includes"]/string'):
            print((base / pathlib.Path(i.get('value'))).as_posix())
"
-- {expected_bazel_exec} cquery  --output=files //bzl:bzl
-- END: hello -> //bzl:bzl

-- START: hello -> //:world
-- WORKSPACE: /workspace/src/test/project/bzl_world
-- BAZEL ARGUMENTS: --config=warnings -c dbg
-- BAZEL BUILD TARGET: ON
-- {expected_bazel_exec} build --config=warnings -c dbg //:world
-- {expected_bazel_exec} query deps(//:world) --output xml
-- python3 -c "
import sys
import pathlib
import xml.etree.ElementTree as ET

root = ET.fromstring(sys.stdin.read())

for node in root.iter('rule'):
    if node.get('class') == 'cc_library':
        base = pathlib.Path(node.get('location')).parent
        print(base.as_posix())
        for i in node.findall('.//list[@name="includes"]/string'):
            print((base / pathlib.Path(i.get('value'))).as_posix())
"
-- {expected_bazel_exec} cquery --config=warnings -c dbg --output=files //:world
-- END: hello -> //:world"""

        self.maxDiff = None
        self.assertEqual(actual_cleaned.strip(), expected.strip())


if __name__ == "__main__":
    unittest.main()
