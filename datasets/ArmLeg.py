import pandas as pd
import os, io

# Get dataset
def get_dataset(folderName, datFile):
    '''
    Extract train and test datasets from designated location
    '''
    current_dir = os.getcwd()
    datasets_dir = os.path.join(
        current_dir, folderName, datFile
    ) 

    with open(datasets_dir, mode='r') as file:
        dataset_data = file.read()

    df = pd.read_csv(io.StringIO(dataset_data), sep=' ',index_col=0)
    
    # Convert dataframe to float type
    df = df.astype(float)
    df = df.applymap('{:.1f}'.format)

    return df

# Export .dat file
def export(folderName, dataframe, name):
    '''
    Export .dat file into designated folder
    '''
    current_dir = os.getcwd()
    folder_dir = os.path.join(
        current_dir, folderName
    ) 

    file_path = os.path.join(folder_dir, name)

    if os.path.exists(file_path):
        os.remove(file_path)

    dataframe.to_csv(file_path, sep=' ', index=True)

# Get ci dataset
train = get_dataset('Datasets_CI', 'TrainDataset_CI.dat')
test = get_dataset('Datasets_CI', 'TestDataset_CI.dat')

# Get reference data
armRef = get_dataset('Datasets_SD', 'ArmDataset_SD.dat')
legRef = get_dataset('Datasets_SD', 'LegDataset_SD.dat')

# Trim dataset
legCI = train[legRef.columns]
armCI = train[armRef.columns]

# Export file
export('Datasets_CI', legCI, 'NewLegDataset_CI.dat')
export('Datasets_CI', armCI, 'NewArmDataset_CI.dat')