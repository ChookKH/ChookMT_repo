import os, sys, io
import pandas as pd 
import numpy as np
import pickle
from sklearn import tree
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score

# Check the command-line argument
if len(sys.argv) != 3:
    print('Usage: python .\ML.py <std|ci|liaw> <Trunk|Leg|Arm|Speed|Fluency|Stability>')
    sys.exit()

option = sys.argv[1]
target = sys.argv[2]

# Get dataset
def get_dataset(folderName, datFile):
    '''
    Extract train and test datasets from designated location
    '''
    currentDir = os.getcwd()
    datasetsDir = os.path.join(
        currentDir, folderName, datFile
    ) 

    with open(datasetsDir, mode='r') as file:
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
    currentDir = os.getcwd()
    datasetsDir = os.path.join(
        currentDir, folderName, datFile
    )

    with open(datasetsDir, mode='r') as file:
        datasetData = file.read()

    df = pd.read_csv(io.StringIO(datasetData), sep=' ',index_col=0)
    df = pd.concat(
        [df, pd.DataFrame(
            data=["" for i in range(df.shape[0])], 
            columns=["Patient ID"], 
            index=df.index
            )],axis=1
    )

    getPatient = lambda x: x[:8] if x.startswith('RB') else x[:5]
    for idx in df.index:
        df.at[idx, "Patient ID"] = getPatient(idx)

    patientCounts = df["Patient ID"].value_counts()
    patientWeights = 1 / patientCounts

    df["Patient ID"] = df["Patient ID"].map(patientWeights).tolist()

    sampleWeights = df["Patient ID"].tolist()

    return sampleWeights

def save_y_pred(option, method, yTest, yPred):
    '''
    Concatenate ypred value to ytrue and save as csv
    '''
    # Create a DataFrame with y_pred and appropriate column name
    yPredDf = pd.DataFrame(
        {f'{target}': yTest,
         f'pred{target}': yPred
         }, index=yTest.index
        )

    # Define the base directory for saving R2 scores
    baseDir = os.path.join('R2_scores')

    # Define file name
    fileName = f'{option.capitalize()}{method}{Name}.csv'
    filePath = os.path.join(baseDir, fileName)
    
    if os.path.exists(filePath):
        existingDf = pd.read_csv(filePath, index_col=0)
    else:
        existingDf = pd.DataFrame(index=yTest.index)

    # Concatenate y_test with existing_df along columns
    updatedDf = pd.concat([existingDf, yPredDf], axis=1)
    
    # Save updated_df with y_pred as CSV
    updatedDf.to_csv(filePath)

    print(f'y_test with y_pred ({method}) saved successfully at: {filePath}')

# Define weights
weights = get_weights('Datasets_SD','TrainDataset_SD.dat')
armWeights = get_weights('Datasets_SD','ArmDataset_SD.dat')
legWeights = get_weights('Datasets_SD','LegDataset_SD.dat')


# === === === ===
# Dataset dictionary
dataset = {
    'std': 
    {
        'folder': 'Datasets_SD',
        'testFile': 'TestDataset_SD.dat',
        'trainFile': 'TrainDataset_SD.dat',
        'armFile': 'ArmDataset_SD.dat',
        'legFile': 'LegDataset_SD.dat'
    },  
    'ci': 
    {
        'folder': 'Datasets_CI',
        'testFile': 'TestDataset_CI.dat',
        'trainFile': 'TrainDataset_CI.dat',
        'armFile': 'ArmDataset_CI.dat',
        'legFile': 'LegDataset_CI.dat'
    }, 
    'liaw': 
    {
        'folder': 'Datasets_Liaw',
        'testFile': 'TestDataset_Liaw.dat',
        'trainFile': 'TrainDataset_Liaw.dat',
        'armFile': 'ArmDataset_Liaw.dat',
        'legFile': 'LegDataset_Liaw.dat'        
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
    'Stability']].sum(axis=1)

# Outputs options
targets = [target]


# === === === ===
# Target data
if target == 'Arm':
    targetFile = "armFile"
    sampleWeights = armWeights

elif target == 'Leg':
    targetFile = "legFile"
    sampleWeights = legWeights

else:
    targetFile = "trainFile"
    sampleWeights = weights


# === === === ===
# FOR sklearn tree based regressors
# Parameter library for HPT
modelParams = {
    'SVM': {
        'model': SVR(),
        'params': {
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'C': [0.1, 1, 10],
            'epsilon': [0.1, 0.2, 0.5],
            'degree': [2, 3, 4]
        }
    },

    'TR':{
        'model': tree.DecisionTreeRegressor(),
        'params': {
            'max_features': [None, 'sqrt', 'log2'],
            'splitter': ['best', 'random'],
            'min_weight_fraction_leaf': [0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
            'max_depth': [3, 4, 5, 6, 7],
            'random_state':[0]
        }
    },

    'RFR':{
        'model': RandomForestRegressor(),
        'params': {
            'n_estimators': [50, 100, 500, 1000],
            'random_state':[0]
        }
    },

    'ABR':{
        'model': AdaBoostRegressor(),
        'params': {
            'n_estimators': [50, 100, 500, 1000],
            'random_state':[0]
        }
    }
}


# === === === ===
# Initialize train and test data
if option in dataset:
    datasetInfo = dataset[option]

    # Train data
    XtrainDF = get_dataset(datasetInfo['folder'], datasetInfo[targetFile])
    yTrain = yTrainCollection[target]
    
    # Test data
    XtestDF = get_dataset(datasetInfo['folder'], datasetInfo['testFile'])
    yTest = yTestCollection[target]
    

    # === === === ===
    # For hyperparameter tuning
    for Name, Params in modelParams.items():
        classifier = Params['model']
        paramGrid = Params['params']

        # To loop through each target
        for target in targets: 
            cross = KFold(n_splits=10, shuffle=False)
            gridSearch = GridSearchCV(
                classifier, 
                paramGrid, 
                scoring='r2', 
                cv=cross
            )

            # Special for Arm and Leg Dataset, trim Xtest to only contain relevant
            # features
            if (target == "Leg") or (target == "Arm"):
                XtestDF = XtestDF[XtrainDF.columns]
            else:
                pass

            # Construct the base folder path for feature_list
            featurePath = os.path.join(
                os.getcwd(), 'feature_list'
            )

            # Load and train model for each method
            fileName = f'borda_{option}_{target}.csv'
            filePath = os.path.join(featurePath, fileName)

            # Check if the file exists
            if os.path.exists(filePath):
                # Load the feature list from the CSV file
                selectedFeaturesDf = pd.read_csv(filePath, index_col=0)

                # Sort features in descending order
                sortedFeatures = selectedFeaturesDf['x'].sort_values(ascending=False)

                # Number of features that would be taken (10% of sample size)
                numFeaturesToKeep = int(0.1 * len(yTrainCollection[target]))
                topFeatures = sortedFeatures.index[:numFeaturesToKeep]

                # New Xtrain and Xtest
                XtrainDFSelected = XtrainDF[topFeatures]
                XtestDFSelected = XtestDF[topFeatures]
                
                # Train model with selected features
                gridSearch.fit(XtrainDFSelected, yTrain, sample_weight=weights)

                # Predict using the trained model
                yPred = gridSearch.predict(XtestDFSelected)

                # Capping the SMS-subscores at 0 and 3
                capUpperValues = np.vectorize(lambda x: 3.0 if x > 3.0 else x)
                capLowerValues = np.vectorize(lambda x: 0.0 if x < 0.0 else x)
                yPred = capUpperValues(yPred)
                yPred = capLowerValues(yPred)
                
                # Call the function to save y_test with appended yPred column
                save_y_pred(option, 'borda', yTest, yPred)
                
                # R2 score
                balanceScore = r2_score(yTest, yPred)
                # print(f'{Name}({option}) - {target} score(borda) = {balanceScore}')
                # print("Best parameters:", gridSearch.best_params_) 

                # === === === ===
                # Folder to store all models
                modelsFolder = os.path.join(
                    os.getcwd(), 'Models'
                    )
                if not os.path.exists(modelsFolder):
                    os.makedirs(modelsFolder)
    
                # Create folder for each dataset and classifier
                folderName = os.path.join(
                    modelsFolder, f'{datasetInfo["folder"]}_{Name}'
                    )
                if not os.path.exists(folderName):
                    os.makedirs(folderName)
     
                # Save the trained model using pickle
                modelFilename = f'{folderName}/{Name}_{target}_borda.pickle'
                with open(modelFilename, 'wb') as modelFile:
                    pickle.dump(gridSearch.best_estimator_, modelFile)
    
                print(f"Trained {Name} model for {target} saved as {modelFilename}")

            else:
                print(f"File not found for method: {fileName}")
else:
    print("Invalid option. Use 'std' or 'ci' or 'liaw'.")