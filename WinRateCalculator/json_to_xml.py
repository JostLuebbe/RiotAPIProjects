import xml.etree.ElementTree as ET


def indent(elem, level=0):
    i = "\n" + level * "  "
    j = "\n" + (level - 1) * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


def convert_json_to_xml(json_file):
    def converter(input, root, name):
        if type(input) is list:
            for i, item in enumerate(input):
                sub_tier = ET.SubElement(root, name + str(i))
                converter(item, sub_tier, name)
        elif type(input) is dict:
            for key, value in input.items():
                if key[0].isdigit():
                    continue
                if type(value) in [list, dict]:
                    mother = ET.SubElement(root, key)
                    converter(value, mother, str(key))
                elif (type(key) is str) and (type(value) in [str, int, bool]):
                    ET.SubElement(root, key).text = str(value)
                else:
                    print('Key Type: ' + str(type(key)))
                    print('Value Type: ' + str(type(value)))

    xml_root = ET.Element('root')
    converter(json_file, xml_root, 'default')
    indent(xml_root)

    return xml_root
