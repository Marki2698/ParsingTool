import xlsxwriter


def build_xlsx_file(filename, data):
    workbook = xlsxwriter.Workbook(filename)

    overall(data, workbook)

    for raw_data_for_sheet in data:
        sheet = workbook.add_worksheet(raw_data_for_sheet['folder']['name'])
        fill_sheet(raw_data_for_sheet, sheet)
    workbook.close()


def fill_sheet(raw_data, sheet):
    sheet.write(0, 0, "file name")
    sheet.write(0, 1, "function names")

    filename_column_index = 0
    filename_column = "A:A"
    function_name_column = "B:B"

    name_func_column = 1
    func_column_index = name_func_column + 1
    filename_row = 2
    func_row = filename_row + 1

    example_func_for_stats = raw_data.get('files')[0].get('functions')[0]
    for stat in example_func_for_stats.keys():
        if stat in 'probes' or stat in 'name':
            continue
        else:
            sheet.write(0, func_column_index, stat)
            func_column_index += 1

    func_column_index = name_func_column + 1

    filename_column_width = 0
    function_name_column_width = 0

    for file in raw_data.get('files'):
        filename = file.get('info').get('name')

        if len(filename) > filename_column_width:
            filename_column_width = len(filename)

        sheet.write(filename_row, filename_column_index, filename)
        for func in file.get('functions'):
            function_name = func.get('name')
            if len(function_name) > function_name_column_width:
                function_name_column_width = len(function_name)

            for attrName in func.keys():
                if attrName in 'probes':
                    continue

                if attrName in 'name':
                    sheet.write(func_row, name_func_column, func.get(attrName))
                else:
                    sheet.write(func_row, func_column_index, func.get(attrName))
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
    name_column_index = 0
    example_file_for_stats = data[0].get('files')[0].get('info')
    header_file_column = 0
    for stat_key in example_file_for_stats.keys():
        if stat_key in 'mtime':
            continue
        else:
            if stat_key in 'name':
                overall_sheet.write(0, name_column_index, stat_key)

            else:
                overall_sheet.write(0, header_file_column, stat_key)
                header_file_column += 1

    row = 1
    col = 0
    filename_field_len = 0
    for folder in data:
        for file in folder.get('files'):
            file_info = file.get('info')
            filename = file.get('info').get('name')
            if len(filename) > filename_field_len:
                filename_field_len = len(filename)

            for attrName in file_info.keys():

                if attrName in 'mtime':
                    continue
                else:
                    if attrName in 'name':
                        overall_sheet.write(row, name_column_index, file_info.get(attrName))
                    else:
                        overall_sheet.write(row, col, file_info.get(attrName))
                        col += 1
            row += 1
            col = 0

    print(filename_field_len)
    overall_sheet.set_column(name_column, filename_field_len)
