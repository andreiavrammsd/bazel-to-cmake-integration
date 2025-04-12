import pathlib
import xml.etree.ElementTree as ET
import sys


if len(sys.argv) == 1:
    print("Path to xml file is missing")
    exit(1)

with open(sys.argv[1]) as file:
    root = ET.fromstring(file.read())

    for node in root.iter("rule"):
        if node.get("class") == "cc_library":
            location = node.get("location")
            includes = [
                include.get("value")
                for include in node.findall(".//list[@name='includes']/string")
            ]

            root = pathlib.Path(location).parent
            print(root.as_posix())

            for dep_include in includes:
                print((root / pathlib.Path(dep_include)).as_posix())
