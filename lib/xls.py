import xlsxwriter
import os
from decimal import Decimal
import lib.constants as constant
from .xml_parser import build_path_for_files


def build_xlsx_file(filename, data, child_to_parent_map):
    workbook = xlsxwriter.Workbook(os.path.abspath(filename))

    overall(data, workbook, child_to_parent_map)

    for raw_data_for_sheet in data:
        sheet = workbook.add_worksheet(get_sheet_name(raw_data_for_sheet))
        fill_sheet(raw_data_for_sheet, sheet)
    workbook.close()


def get_sheet_name(sheet_data):
    return sheet_data[constant.XML_FIELDS.get('FOLDER')][constant.XML_FIELDS.get('NAME')]


def fill_sheet(raw_data, sheet):
    sheet.write(constant.FILENAME_HEADER_CELL, "file name")

    filename_column_index = 0

    name_func_column = 1
    filename_row = 2
    func_row = filename_row + 1

    for header in constant.COLUMN_INDEXES.keys():
        sheet.write(0, constant.COLUMN_INDEXES.get(header), header)
        if header == 'cd_cov_d_cov' or header == 'cd_uncov_d_uncov':
            column_index = constant.COLUMN_INDEXES.get(header)
            sheet.set_column(column_index, column_index, 15)

    func_column_index = name_func_column + 1

    filename_column_width = 0
    function_name_column_width = 0

    for file in raw_data.get(constant.CUSTOM_XML_FIELDS.get('FILES')):
        filename = file.get(constant.CUSTOM_XML_FIELDS.get('INFO')).get(constant.XML_ATTRIBUTES.get('NAME'))

        if filename.endswith(constant.HEADER_EXTENTION):
            continue

        filename_column_width = set_name_field_length(filename, filename_column_width)

        sheet.write(filename_row, filename_column_index, filename)
        for func in file.get(constant.CUSTOM_XML_FIELDS.get('FUNCTIONS')):
            function_name = func.get(constant.XML_ATTRIBUTES.get('NAME'))
            function_name_column_width = set_name_field_length(function_name, function_name_column_width)

            for attrName in constant.COLUMN_INDEXES.keys():
                strategy(sheet, func_row, func, attrName)
                func_column_index += 1

            func_row += 1
            func_column_index = name_func_column + 1

        filename_row += len(file.get(constant.CUSTOM_XML_FIELDS.get('FUNCTIONS'))) + 1
        func_row = filename_row + 1

    sheet.set_column(constant.NAME_COLUMN, filename_column_width)
    sheet.set_column(constant.FUNCTION_NAME_COLUMN, function_name_column_width)


def overall(folders, workbook, child_to_parent_map):
    overall_sheet = workbook.add_worksheet('Overall')

    for header in constant.COLUMN_INDEXES.keys():
        overall_sheet.write(0, constant.COLUMN_INDEXES.get(header) - 1, header)
        if header == 'cd_cov_d_cov' or header == 'cd_uncov_d_uncov':
            column_index = constant.COLUMN_INDEXES.get(header) - 1
            overall_sheet.set_column(column_index, column_index, 15)

    row = 1
    filename_field_len = 0
    for folder in folders:

        for file in folder.get(constant.CUSTOM_XML_FIELDS.get('FILES')):
            # path = build_path_for_files(file, child_to_parent_map)
            file_info = file.get(constant.CUSTOM_XML_FIELDS.get('INFO'))
            filename = file_info.get(constant.XML_ATTRIBUTES.get('NAME'))
            filename_field_len = set_name_field_length(filename, filename_field_len)

            if filename.endswith(constant.HEADER_EXTENTION):
                continue

            for attrName in constant.COLUMN_INDEXES.keys():
                strategy(overall_sheet, row, file_info, attrName, True)

            row += 1

    overall_sheet.set_column(constant.NAME_COLUMN, filename_field_len)


def set_name_field_length(name, prev_length):
    if len(name) > prev_length:
        return len(name)
    else:
        return prev_length


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
