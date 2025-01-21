import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('c:/Users/nador/Downloads/xmlfiles/xmlfiles/L101_S1_Dang_2007.xml')
# tree = ET.parse('L101_S1_Dang_2007.xml')
root = tree.getroot()

# Extract and print the relevant information
def parse_xml_element(element, indent=""):
    for child in element:
        if list(child):
            print(f"{indent}{child.tag}:")
            parse_xml_element(child, indent + "    ")
        else:
            print(f"{indent}{child.tag}: {child.text}")

parse_xml_element(root)