__author__ = 'ipetrash'


from xml.dom.minidom import parseString

def pretty_xml_minidom(xml, ind=' ' * 2):
    """Функция принимает строку xml и выводит xml с отступами."""

    xml_utf8 = parseString(xml).toprettyxml(indent=ind, encoding='utf-8')
    return xml_utf8.decode('utf-8')


from lxml import etree

def pretty_xml_lxml(xml_str):
    """Функция принимает строку xml и выводит xml с отступами."""

    root = etree.fromstring(xml_str)
    return etree.tostring(root, pretty_print=True).decode('utf-8')


if __name__ == '__main__':
    xml = '<a><b/><c><z/><h/></c></a>'
    print(pretty_xml_minidom(xml))
    print(pretty_xml_lxml(xml))