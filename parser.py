import xml.etree.ElementTree as ET
import sys
from utils.xml_parser import get_stats, count_something
from utils.xls import build_xlsx_file
import xlsxwriter

# workbook = xlsxwriter.Workbook('Test.xlsx')
# worksheet = workbook.add_worksheet('test')
#
# expenses = (
#     ['Rent', 1000],
#     ['Gas', 100],
#     ['Food', 300],
#     ['Gym', 50],
# )
#
# row = 0
# col = 0
#
# for item, cost in (expenses):
#     worksheet.write(row, col, item)
#     worksheet.write(row, col+1, cost)
#     row+=1
#
# worksheet.write(row, 0, 'Total')
# worksheet.write(row, 1, '=SUM(B1:B4)')
#
# workbook.close()

xml_file = sys.argv[1]
xlsx_filename = sys.argv[2]

tree = ET.parse(xml_file)
root = tree.getroot()
child_to_parent_map = {c: p for p in root.iter() for c in p}
# print(parent_map)

# for parent, child in child_to_parent_map.items():
#     # print(parent, child)

res = get_stats(root, child_to_parent_map)
build_xlsx_file(xlsx_filename, res)
# print(count_something(res))
