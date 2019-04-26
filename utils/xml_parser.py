list_of_folders_with_functions = []


def dig(xml_elem, parent_map):
    children = xml_elem.getchildren()
    sheet = {}  # TODO: rename variable
    folder = {}

    for attr in xml_elem.attrib:
        folder[attr] = xml_elem.get(attr)

    sheet['folder'] = folder

    if parent_map.get(xml_elem) is not None:
        parent_name = parent_map.get(xml_elem).get('name')
        if 'Bullseye' not in parent_name:
            sheet['folder']['name'] = parent_name + '_' + sheet['folder']['name']

    all_files_in_folder = []

    for child in children:
        if 'folder' in child.tag:
            dig(child, parent_map)
        else:
            if 'src' in child.tag:
                file = {
                    'info': parse_file_info_from_xml(child)
                }

                functions_in_file = []

                for func in child.getchildren():
                    functions_in_file.append(parse_fn_from_xml(func))

                file['functions'] = functions_in_file
                all_files_in_folder.append(file)
    sheet['files'] = all_files_in_folder

    if len(all_files_in_folder):
        list_of_folders_with_functions.append(sheet)


def parse_file_info_from_xml(file_elem):
    file_info = {}
    for attrName in file_elem.attrib:
        file_info[attrName] = file_elem.get(attrName)

    return file_info


def parse_fn_from_xml(fn_elem):
    probes = []
    func_info = {}

    for probe in fn_elem.getchildren():
        temp = {}
        for attr in probe.attrib:
            temp[attr] = probe.get(attr)
        probes.append(temp)

    for attr in fn_elem.attrib:
        func_info[attr] = fn_elem.get(attr)

    func_info['probes'] = probes

    return func_info


def count_something(arr):  # cd_total just for checking with given xml file
    count = 0
    for category in arr:
        for func in category['functions']:
            cd_total = int(func['cd_total'])
            count += cd_total

    return count


def get_stats(xml_elem, map):
    dig(xml_elem, map)

    return list_of_folders_with_functions
