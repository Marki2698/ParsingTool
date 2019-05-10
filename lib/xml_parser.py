import lib.constants as constant

list_of_folders_with_functions = []


def dig(xml_elem, parent_map, file_path=''):
    children = xml_elem.getchildren()
    sheet = {}
    folder = {}

    for attr in xml_elem.attrib:
        folder[attr] = xml_elem.get(attr)

    sheet[constant.XML_FIELDS.get('FOLDER')] = folder

    if parent_map.get(xml_elem) is not None:
        parent_name = parent_map.get(xml_elem).get(constant.XML_ATTRIBUTES.get('NAME'))
        if 'Bullseye' not in parent_name:
            current_folder_name = sheet[constant.XML_FIELDS.get('FOLDER')][constant.XML_FIELDS.get('NAME')]
            folder = sheet[constant.XML_FIELDS.get('FOLDER')]
            folder[constant.XML_FIELDS.get('NAME')] = set_folder_name(parent_name, current_folder_name)

    all_files_in_folder = []

    for child in children:
        if constant.XML_FIELDS.get('FOLDER') in child.tag:
            path = file_path + '/' + child.get(constant.XML_ATTRIBUTES.get('NAME'))
            dig(child, parent_map, path)
        else:
            if constant.XML_FIELDS.get('SRC') in child.tag:
                file = {
                    'info': parse_file_info_from_xml(child),
                    'path': file_path
                }

                functions_in_file = []

                for func in child.getchildren():
                    functions_in_file.append(parse_fn_from_xml(func))

                file[constant.CUSTOM_XML_FIELDS.get('FUNCTIONS')] = functions_in_file
                all_files_in_folder.append(file)
    sheet[constant.CUSTOM_XML_FIELDS.get('FILES')] = all_files_in_folder

    if len(all_files_in_folder):
        list_of_folders_with_functions.append(sheet)


def set_folder_name(parent_name, current_name):
    return "{}_{}".format(parent_name, current_name)


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

    func_info[constant.CUSTOM_XML_FIELDS.get('PROBES')] = probes

    return func_info


def get_stats(xml_elem, child_to_parent_map):
    dig(xml_elem, child_to_parent_map)

    return list_of_folders_with_functions
