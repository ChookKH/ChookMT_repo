import pandas as pd
import os
import io
import zipfile

# Get the current working directory
current_directory = os.getcwd()

# Go one level up to the parent directory
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

# Specify the path to the exportedData folder
exported_data_directory = os.path.join(parent_directory, 'ckhExportedData')

# # Specify the file name and path within the exportedData directory
# file_name = 'data.dat'
# file_path = os.path.join(exported_data_directory, file_name)

subfolder_name = 'subfolder'

# Create the subfolder within the exportedData directory
subfolder_path = os.path.join(exported_data_directory, subfolder_name)
os.makedirs(subfolder_path)

# Generate sample DataFrame
data = {'Name': ['John', 'Jane', 'Bob'],
        'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# Specify the file name and path within the subfolder
file_name = 'data.dat'
file_path = os.path.join(subfolder_path, file_name)

# Save DataFrame as .dat file
df.to_csv(file_path, sep='\t', index=False)
                        
