import os
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd

# Directory containing XML files
directory = 'c:/Users/nador/Downloads/xmlfiles/xmlfiles/materialsmine_xmls'  # REPLACE with your XML directory

def check_structure(file_path):
    """
    Checks if the XML file contains the required structure and if
    <DynamicPropertyProfile><data><AxisLabel><xName> is 'Temperature'.
    """
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
                        # Check for "Temperature" in the required nested tags
                        data = dynamic_property_profile.find('data')
                        if data is not None:
                            axis_label = data.find('AxisLabel')
                            if axis_label is not None:
                                x_name = axis_label.find('xName')
                                # if x_name is not None and x_name.text == 'Frequency':
                                if x_name is not None:
                                    # print(x_name.text)
                                    return True, x_name.text
    except ET.ParseError:
        pass
    return False, None

def find_xml_files_with_structure(directory):
    """
    Finds XML files in the specified directory that meet the check_structure criteria.
    """
    matching_files = []
    XCols = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            file_check, XCol = check_structure(file_path)
            if file_check:
                matching_files.append(filename)
                XCols.append(XCol)

    return matching_files, XCols

# Find matching files
matching_files, XCols = find_xml_files_with_structure(directory)

# Report results
print("Files with the specified structure and containing 'Temperature':")
for file in matching_files:
    print(file)
print(f'Number of files with the specified structure and "Temperature": {len(matching_files)}')
# print(XCols)

xaxis_type = Counter(XCols).keys()
xaxis_count = Counter(XCols).values()
df = pd.DataFrame([xaxis_type, xaxis_count], columns=["Type", "Count"])
print(df)
df.to_csv('df_out.csv')