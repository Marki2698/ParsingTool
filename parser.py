import xml.etree.ElementTree as ET
import sys
import os
from lib.xml_parser import get_stats
from lib.xls import build_xlsx_file

xml_path = sys.argv[1]
xlsx_path = sys.argv[2]

if not os.path.exists(xml_path):
    print('path does not exist, please check your path and try again.')
    exit(0)

tree = ET.parse(xml_path)
root = tree.getroot()
child_to_parent_map = {child: parent for parent in root.iter() for child in parent}
stats = get_stats(root, child_to_parent_map)
build_xlsx_file(xlsx_path, stats, child_to_parent_map)
