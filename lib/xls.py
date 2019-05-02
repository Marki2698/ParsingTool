import xlsxwriter
import math
import os
from decimal import Decimal
import lib.constants as constant


CUSTOM_COLUMNS = [
    'fn_uncov',
    'cd_cov_d_cov',
    'cd_uncov_d_uncov',
]


def build_xlsx_file(filename, data):
    workbook = xlsxwriter.Workbook(os.path.abspath(filename))

    overall(data, workbook)

    for raw_data_for_sheet in data:
        sheet = workbook.add_worksheet(get_sheet_name(raw_data_for_sheet))
        fill_sheet(raw_data_for_sheet, sheet)
    workbook.close()


def get_sheet_name(sheet_data):
    return sheet_data[constant.XML_FIELDS.get('FOLDER')][constant.XML_FIELDS.get('NAME')]


def fill_sheet(raw_data, sheet):
    sheet.write(0, 0, "file name")
    # sheet.write(0, 1, "function names")

    filename_column_index = 0
    filename_column = "A:A"
    function_name_column = "B:B"

    name_func_column = 1
    func_column_index = name_func_column + 1
    filename_row = 2
    func_row = filename_row + 1

    for header in constant.COLUMN_INDEXES.keys():
        sheet.write(0, constant.COLUMN_INDEXES.get(header), header)
        if header == 'cd_cov_d_cov' or header == 'cd_uncov_d_uncov':
            sheet.set_column(constant.COLUMN_INDEXES.get(header), 30)

    func_column_index = name_func_column + 1

    filename_column_width = 0
    function_name_column_width = 0

    for file in raw_data.get('files'):
        filename = file.get('info').get('name')

        if filename.endswith('.h'):
            continue

        if len(filename) > filename_column_width:
            filename_column_width = len(filename)

        sheet.write(filename_row, filename_column_index, filename)
        for func in file.get('functions'):
            function_name = func.get('name')
            if len(function_name) > function_name_column_width:
                function_name_column_width = len(function_name)

            for attrName in constant.COLUMN_INDEXES.keys():
                strategy(sheet, func_row, func, attrName)
                func_column_index += 1

            func_row += 1
            func_column_index = name_func_column + 1

        filename_row += len(file.get('functions')) + 1
        func_row = filename_row + 1

    sheet.set_column(filename_column, filename_column_width)
    sheet.set_column(function_name_column, function_name_column_width)


def overall(data, workbook):
    overall_sheet = workbook.add_worksheet('Overall')
    name_column = "A:A"

    for header in constant.COLUMN_INDEXES.keys():
        overall_sheet.write(0, constant.COLUMN_INDEXES.get(header) - 1, header)
        if header == 'cd_cov_d_cov' or header == 'cd_uncov_d_uncov':
            overall_sheet.set_column(constant.COLUMN_INDEXES.get(header) - 1, 30)

    row = 1
    filename_field_len = 0
    for folder in data:
        for file in folder.get('files'):
            file_info = file.get('info')
            filename = file_info.get('name')
            if len(filename) > filename_field_len:
                filename_field_len = len(filename)

            if filename.endswith('.h'):
                continue

            for attrName in constant.COLUMN_INDEXES.keys():
                strategy(overall_sheet, row, file_info, attrName, True)

            row += 1

    overall_sheet.set_column(name_column, filename_field_len)


def percentize(raw_result, attr):
    if attr in constant.FIELDS_TO_PERCENTIZE:
        return "{} %".format(raw_result)
    else:
        return raw_result


def calc_result(a, b):
    floated_a = float(a)
    floated_b = float(b)

    try:
        result = round(Decimal((floated_a / floated_b) * 100))
    except ZeroDivisionError:
        result = 0

    return result


def strategy(sheet, row, func_or_file_info, attr, is_file=False):

    if attr in constant.EXCLUDE_FIELDS:
        return

    if attr == 'fn_cov':
        result = covered_functions(func_or_file_info)
    elif attr == 'fn_uncov':
        result = uncovered_functions(func_or_file_info)
    elif attr == 'cd_cov_d_cov':
        result = covered_cd_and_d(func_or_file_info)
    elif attr == 'cd_uncov_d_uncov':
        result = uncovered_cd_and_d(func_or_file_info)
    else:
        result = func_or_file_info.get(attr)

    formatted_result = percentize(result, attr)
    if is_file:
        column_index = constant.COLUMN_INDEXES.get(attr) - 1
    else:
        column_index = constant.COLUMN_INDEXES.get(attr)

    sheet.write(row, column_index, formatted_result)


def covered_functions(func_or_file):
    total_functions = int(func_or_file.get(constant.XML_ATTRIBUTES.get('FUNCTIONS_TOTAL')))
    covered_funcs = int(func_or_file.get(constant.XML_ATTRIBUTES.get('FUNCTIONS_COVERED')))
    return calc_result(covered_funcs, total_functions)


def uncovered_functions(func_or_file):
    total_functions = int(func_or_file.get(constant.XML_ATTRIBUTES.get('FUNCTIONS_TOTAL')))
    covered_funcs = int(func_or_file.get(constant.XML_ATTRIBUTES.get('FUNCTIONS_COVERED')))
    return total_functions - covered_funcs


def get_sum_of_conditions_and_decisions(func_or_file):
    conditions_total = int(func_or_file.get(constant.XML_ATTRIBUTES.get('CONDITIONS_TOTAL')))
    decisions_total = int(func_or_file.get(constant.XML_ATTRIBUTES.get('DECISIONS_TOTAL')))
    return conditions_total + decisions_total


def get_sum_of_covered_conditions_and_decisions(func_or_file):
    covered_conditions = int(func_or_file.get(constant.XML_ATTRIBUTES.get('CONDITIONS_COVERED')))
    covered_decisions = int(func_or_file.get(constant.XML_ATTRIBUTES.get('DECISIONS_COVERED')))
    return covered_conditions + covered_decisions


def covered_cd_and_d(func_or_file):
    return calc_result(get_sum_of_covered_conditions_and_decisions(func_or_file),
                       get_sum_of_conditions_and_decisions(func_or_file))


def uncovered_cd_and_d(func_or_file):
    return get_sum_of_conditions_and_decisions(func_or_file) - get_sum_of_covered_conditions_and_decisions(func_or_file)
