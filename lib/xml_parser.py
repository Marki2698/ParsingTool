import lib.constants as constant

list_of_folders_with_functions = []


def dig(xml_elem, parent_map):
    children = xml_elem.getchildren()
    sheet = {}  # TODO: rename variable
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
            dig(child, parent_map)
        else:
            if constant.XML_FIELDS.get('SRC') in child.tag:
                file = {
                    'info': parse_file_info_from_xml(child)
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


def rec(xml_elem, parent_map):
    print(xml_elem.get('info').get('name'))
    path = ''
    current_elem = xml_elem
    keep_going = True
    while keep_going:
        if current_elem is None:
            keep_going = False
        else:
            for key in parent_map.keys():
                if hasattr(key, 'name'):
                    key_name = key.get('name')
                else:
                    key_name = key.get('info').get('name')

                if hasattr(current_elem, 'name'):
                    current_name = current_elem.get('name')
                else:
                    current_name = current_elem.get('info').get('name')

                if key_name == current_name:
                    parent = parent_map.get(key)
                    if parent is None:
                        keep_going = False
                    else:

                        if hasattr(parent, 'name'):
                            parent_name = parent.get('name')
                        else:
                            parent_name = parent.get('info').get('name')

                        path += '/' + parent_name
                        current_elem = parent
    print(path)
    return path


def build_path_for_files(file, child_to_parent_map):
    file_info = file.get(constant.CUSTOM_XML_FIELDS.get('INFO'))
    filename = file_info.get(constant.XML_ATTRIBUTES.get('NAME'))
    path = rec(file, child_to_parent_map)
    return path
