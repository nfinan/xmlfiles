import os
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd

# Directory containing XML files
directory = 'c:/Users/nador/Downloads/xmlfiles/xmlfiles/materialsmine_xmls'  # REPLACE with your XML directory

def check_structure(file_path):
    """
    Checks if the XML file contains the required structure and extracts the value of <column id="0">.
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
                            nested_data = data.find('data')
                            if nested_data is not None:
                                headers = nested_data.find('headers')
                                if headers is not None:
                                    column_0 = headers.find('column[@id="0"]')  # Find <column id="0">
                                    if column_0 is not None:
                                        return True, column_0.text  # Return the text value of <column id="0">
    except ET.ParseError:
        pass
    return False, None

def find_xml_files_with_structure(directory):
    """
    Finds XML files in the specified directory that meet the check_structure criteria.
    """
    matching_files = []
    column_values = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            file_check, column_value = check_structure(file_path)
            if file_check:
                matching_files.append(filename)
                if column_value:  # Only append non-None column values
                    column_values.append(column_value)
    return matching_files, column_values

# Find matching files
matching_files, column_values = find_xml_files_with_structure(directory)

# Report results
print("Files with the specified structure:")
for file in matching_files:
    print(file)
print(f'Number of files with the specified structure: {len(matching_files)}')

# Count occurrences of <column id="0"> values
column_counts = Counter(column_values)

# Create a DataFrame from the Counter
df = pd.DataFrame.from_dict(column_counts, orient='index', columns=['Count'])
df.index.name = 'Column ID 0 Value'
df.reset_index(inplace=True)

# Output the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('df_out_2.csv', index=False)
