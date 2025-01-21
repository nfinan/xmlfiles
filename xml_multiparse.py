test = 'L110_S12_Singha_2008.xml'
import os
import xml.etree.ElementTree as ET

# This code will report the number and names of all files in a folder
# that fit our filters.
# we are searching for xmls with data that looks like this:
'''
<DynamicPropertyProfile>
                    <data>
                        <AxisLabel>
                            <xName>Temperature</xName>
                            <xUnit>celsius</xUnit>
                            <yName>Storage Modulus</yName>
                            <yUnit>MPa</yUnit>
                        </AxisLabel>
                        <data>
                            <headers>
                                <column id="0">Temperature (C )</column>
                                <column id="1">Storage Modulus (Mpa)</column>
                            </headers>
                            <rows>
                                <row id="0">
                                    <column id="0">25.4606741573</column>
                                    <column id="1">1973.25769854</column>
                                </row>
                                <row id="1">
                                    <column id="0">39.2134831461</column>
                                    <column id="1">1920.5834684</column>
                                </row>
                                .
                                .
                                .
                                [rows beyond hidden]
                            </rows>
                        </data>
                    </data>
                </DynamicPropertyProfile>
'''

# Directory containing XML files
directory = 'c:/Users/nador/Downloads/xmlfiles/xmlfiles' # REPLACE with xml directory

def check_structure(file_path):
    # Check for various features in the xml.for example, here we are looking for xmls with
    # the nested tags: <PROPERTIES><Viscoelastic><DynamicProperties><DynamicPropertyProfile>
    # which relates to viscoelastic samples with reported tabular values.
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        properties = root.find('PROPERTIES')
        if properties is not None:
            viscoelastic = properties.find('Viscoelastic')
            if viscoelastic is not None:
                dynamic_properties = viscoelastic.find('DynamicProperties')
                if dynamic_properties is not None:
                    dynamic_property_profile = dynamic_properties.find('DynamicPropertyProfile')
                    if dynamic_property_profile is not None:
                        return True
    except ET.ParseError:
        pass
    return False

def find_xml_files_with_structure(directory):
    matching_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            if check_structure(file_path):
                matching_files.append(filename)
    return matching_files

matching_files = find_xml_files_with_structure(directory)
print("Files with the specified structure:")
for file in matching_files:
    print(file)
print(f'Number of files with tracked viscoelasticity: {len(matching_files)}')
# print(check_structure(test))