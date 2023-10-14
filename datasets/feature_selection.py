import os, sys, io
import pandas as pd 
import numpy as np
from sklearn.feature_selection import mutual_info_regression, f_regression

# Check the command-line argument
if len(sys.argv) != 3:
    print('Usage: python .\feature_selection.py <std|ci|liaw> <Trunk|Leg|Arm|Speed|Fluency|Stability>')
    sys.exit()

option = sys.argv[1]
target_variable = sys.argv[2]

# Define the R folder name based on the option
if option.lower() == 'std':
    folder_name = 'ReliefFexpRank_SD'
elif option.lower() == 'ci':
    folder_name = 'ReliefFexpRank_CI'
elif option.lower() == 'liaw':
    folder_name = 'ReliefFexpRank_Liaw'
else:
    print('Invalid option. Use "std" or "ci" or "liaw".')
    sys.exit()

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

# Get class weights
def get_weights(folderName, datFile):
    '''
    Calculating and assigning the sample weight of each StridePairID
    '''
    current_dir = os.getcwd()
    datasets_dir = os.path.join(
        current_dir, folderName, datFile
    )

    with open(datasets_dir, mode='r') as file:
        dataset_data = file.read()

    df = pd.read_csv(io.StringIO(dataset_data), sep=' ',index_col=0)
    df = pd.concat(
        [df, pd.DataFrame(
            data=["" for i in range(df.shape[0])],
            columns=["Patient ID"], index=df.index
        )],
        axis=1
    )

    getPatient = lambda x: x[:8] if x.startswith('RB') else x[:5]
    for idx in df.index:
        df.at[idx, "Patient ID"] = getPatient(idx)

    patientCounts = df["Patient ID"].value_counts()
    patientWeights = 1 / patientCounts

    df["Patient ID"] = df["Patient ID"].map(patientWeights).tolist()

    sampleWeights = df["Patient ID"].tolist()

    return sampleWeights

# Save top features as a txt
def save_feature_list(ensemble_name, option, target_variable, df):
    # Define the base directory for saving feature lists
    base_dir = os.path.join('feature_list', 'ensemble', ensemble_name)
    
    # Create directories if they don't exist
    os.makedirs(base_dir, exist_ok=True)
    
    # Define the file path and file name
    file_name = f'{ensemble_name}_{option}_{target_variable}.csv'
    file_path = os.path.join(base_dir, file_name)
    
    # Save the top features as a csv file
    df.to_csv(file_path)

    print(f"Feature list saved successfully at: {file_path}")

# Define weights
weights = get_weights('Datasets_SD','TrainDataset_SD.dat')
arm_weights = get_weights('Datasets_SD','NewArmDataset_SD.dat')
leg_weights = get_weights('Datasets_SD','NewLegDataset_SD.dat')


# === === === ===
# Dataset dictionary
dataset_mapping = {
    'std': 
    {
        'folder': 'Datasets_SD',
        'test_file': 'TestDataset_SD.dat',
        'train_file': 'NewTrainDataset_SD.dat',
        'arm_file': 'NewArmDataset_SD.dat',
        'leg_file': 'NewLegDataset_SD.dat'
    },  
    'ci': 
    {
        'folder': 'Datasets_CI',
        'test_file': 'TestDataset_CI.dat',
        'train_file': 'NewTrainDataset_CI.dat',
        'arm_file': 'NewArmDataset_CI.dat',
        'leg_file': 'NewLegDataset_CI.dat'
    },
    'liaw': 
    {
        'folder': 'Datasets_Liaw',
        'test_file': 'TestDataset_Liaw.dat',
        'train_file': 'NewTrainDataset_Liaw.dat',
        'arm_file': 'NewArmDataset_Liaw.dat',
        'leg_file': 'NewLegDataset_Liaw.dat'        
    }
}

# Initializing data targets
yTrainCollection = pd.read_csv('ytrain.csv',index_col=0)
yTestCollection = pd.read_csv('ytest.csv',index_col=0)
yTestCollection['Sum'] = yTestCollection[[
    'Trunk', 
    'Leg', 
    'Arm', 
    'Speed', 
    'Fluency', 
    'Stability'
]].sum(axis=1)

# Outputs options
target_variables = [target_variable]


# === === === ===
# Target data
if target_variable == 'Arm':
    targetFile = "arm_file"
    sample_weights = arm_weights

elif target_variable == 'Leg':
    targetFile = "leg_file"
    sample_weights = leg_weights

else:
    targetFile = "train_file"
    sample_weights = weights


# === === === ===
# Feature selection section
if option in dataset_mapping:
    dataset_info = dataset_mapping[option]
    np.random.seed(0)


    # === === === ===
    # Initializing train data
    XtrainDF = get_dataset(dataset_info['folder'], dataset_info[targetFile])
    Xtrain = np.array(XtrainDF, np.float32)
    yTrainDF = yTrainCollection[target_variable]
    yTrain = np.array(yTrainDF, np.float32)


    # === === === ===
    # Feature importance using Mutual Information Regression
    mi_scores = mutual_info_regression(Xtrain, yTrain)

    # Create df with feature name and corresponding score
    mi_df = pd.DataFrame({
        'x': mi_scores
    }, index=XtrainDF.columns)

    mi_file_name = f'mi_{option}_{target_variable}.csv'


    # === === === ===
    # Feature selection using f-regression
    f_scores = f_regression(Xtrain, yTrain)

    # Create df with feature name and corresponding score
    f_df = pd.DataFrame({
        'x': f_scores[0]
    }, index=XtrainDF.columns)

    f_file_name = f'f_{option}_{target_variable}.csv'

  
    # === === === ===
    # Call R csv files
    file_name = f'{folder_name}_{target_variable}.csv'
    file_path = os.path.join('..', 'R', file_name)
    r_df = pd.read_csv(file_path)
    r_df.set_index(r_df.columns[0], inplace=True)
    r_df.index.name = ''

    
    # === === === === 
    # Ensemble methods
    # Mean
    mean_scores = (mi_df['x'] + f_df['x'] + r_df['x']) / 3

    # Create a DataFrame for mean scores
    mean_df = pd.DataFrame({
        'x': mean_scores
    }, index=mi_df.index)
    
    save_feature_list('mean', option, target_variable, mean_df)
    
    # === === === ===
    # Ensemble Reciprocal Ranking
    # Rank features using the three methods
    mi_df['Rank_MI'] = mi_df['x'].rank()
    f_df['Rank_F'] = f_df['x'].rank()
    r_df['Rank_R'] = r_df['x'].rank()
    
    # Calculate reciprocal ranks
    mi_df['Reciprocal_Rank_MI'] = 1 / mi_df['Rank_MI']
    f_df['Reciprocal_Rank_F'] = 1 / f_df['Rank_F']
    r_df['Reciprocal_Rank_R'] = 1 / r_df['Rank_R']
    
    # Calculate total reciprocal rank for each feature
    total_reciprocal_rank = 1 / (mi_df['Reciprocal_Rank_MI'] +
                            f_df['Reciprocal_Rank_F'] +
                            r_df['Reciprocal_Rank_R'])
    
    # Create a DataFrame for reciprocal ranks
    reciprocal_df = pd.DataFrame({
        'x': total_reciprocal_rank
    }, index=mi_df.index)

    save_feature_list('reciprocal', option, target_variable, reciprocal_df)


    # === === === ===
    # Ensemble Borda Count
    borda_scores = mi_df['Rank_MI'] + f_df['Rank_F'] + r_df['Rank_R']

    borda_df = pd.DataFrame({
        'x': borda_scores
    }, index=mi_df.index)

    save_feature_list('borda', option, target_variable, borda_df)

else:
    print("Invalid option. Use 'std' or 'ci' or 'liaw'.")

