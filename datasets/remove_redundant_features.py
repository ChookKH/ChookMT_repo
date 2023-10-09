import pandas as pd
import sys, os, io

# Check the command-line argument
if len(sys.argv) != 3:
    print('Usage: python .\remove_redundant_features.py SD|Liaw Arm|Leg|Train')
    sys.exit()

# SD or Liaw dataset
dataset_type = sys.argv[1]
if dataset_type not in ['SD', 'Liaw']:
    print("Invalid dataset type. Choose from 'Arm', 'Leg', 'Train'." )
    sys.exit()

# Different datasets call
dataset_name = sys.argv[2]
if dataset_name not in ['Arm', 'Leg', 'Train']:
    print("Invalid dataset name. Choose from 'Arm', 'Leg', 'Train'." )
    sys.exit()

filename = f'{dataset_name}Dataset_{dataset_type}'

# Get and read datasets directory
current_dir = os.getcwd()
dataset_dir = os.path.join(current_dir, 'Datasets_' + dataset_type, filename + '.dat')

with open(dataset_dir, mode='r') as file:
    dataset_data = file.read()

# IMPORTANT: Only carry this out on the training dataset!
df = pd.read_csv(io.StringIO(dataset_data), sep= ' ', index_col=0)

featuresToRemove = []
for col in df.columns:
    featureSD = df[col].std()
    
    if featureSD == 0.0:
        featuresToRemove.append(col)

# Run a reduced dataset for the std == 0.0 with reduced features
new_df = df.drop(columns=featuresToRemove)
new_filename = f'New{dataset_name}Dataset_{dataset_type}.dat'
new_dataset_dir = os.path.join(current_dir, 'Datasets_' + dataset_type, new_filename)
new_df.to_csv(new_dataset_dir, sep=' ')

print(f"New dataset saved as: {new_dataset_dir}")