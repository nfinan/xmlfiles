import os
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd

# Directory containing XML files
directory = 'c:/Users/nador/Downloads/xmlfiles/xmlfiles/materialsmine_xmls'  # REPLACE with your XML directory

def check_structure(file_path):
    """
    Checks if the XML file contains the required structure and returns the value of <xName>.
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
                        data = dynamic_property_profile.find('data')
                        if data is not None:
                            axis_label = data.find('AxisLabel')
                            if axis_label is not None:
                                x_name = axis_label.find('xName')
                                if x_name is not None:
                                    return True, x_name.text
    except ET.ParseError:
        pass
    return False, None

def find_xml_files_with_structure(directory):
    """
    Finds XML files in the specified directory that meet the check_structure criteria.
    """
    matching_files = []
    x_name_values = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            file_check, x_name = check_structure(file_path)
            if file_check:
                matching_files.append(filename)
                if x_name:  # Only append non-None x_name values
                    x_name_values.append(x_name)
    return matching_files, x_name_values

# Find matching files
matching_files, x_name_values = find_xml_files_with_structure(directory)

# Report results
print("Files with the specified structure:")
for file in matching_files:
    print(file)
print(f'Number of files with the specified structure: {len(matching_files)}')

# Count occurrences of xName values
xname_counts = Counter(x_name_values)

# Create a DataFrame from the Counter
df = pd.DataFrame.from_dict(xname_counts, orient='index', columns=['Count'])
df.index.name = 'xName'
df.reset_index(inplace=True)

# Output the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('df_out.csv', index=False)
