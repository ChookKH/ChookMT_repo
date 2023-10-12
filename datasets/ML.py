import os, sys, io
import pandas as pd 
import numpy as np
import tensorflow as tf
import pickle
from sklearn import tree
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor, BaggingRegressor 
from sklearn.metrics import r2_score
from tensorflow.python import keras
from keras.wrappers.scikit_learn import KerasRegressor

# Check the command-line argument
if len(sys.argv) != 5:
    print('Usage: python .\ML.py <std|liaw> <NN|SK> <Trunk|Leg|Arm|Speed|Fluency|Stability> <Save|Load|Train>')
    sys.exit()

option = sys.argv[1]
mode = sys.argv[2]
target_variable = sys.argv[3]
task = sys.argv[4]

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
        [df, pd.DataFrame(data=["" for i in range(df.shape[0])], columns=["Patient ID"], index=df.index)],
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

def save_y_pred(mode, option, method, y_test, y_pred):
    '''
    Concatenate ypred value to ytrue and save as csv
    '''
    # Create a DataFrame with y_pred and appropriate column name
    y_pred_df = pd.DataFrame(
        {f'{target_variable}': y_test,
         f'pred{target_variable}': y_pred
         }, index=y_test.index
        )

    # Define the base directory for saving R2 scores
    base_dir = os.path.join('R2_scores')

    # Define file name
    file_name = f'{mode}{option.capitalize()}{method}.csv'
    file_path = os.path.join(base_dir, file_name)
    
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path, index_col=0)
    else:
        existing_df = pd.DataFrame(index=y_test.index)

    # Concatenate y_test with existing_df along columns
    updated_df = pd.concat([existing_df, y_pred_df], axis=1)
    
    # Save updated_df with y_pred as CSV
    updated_df.to_csv(file_path)

    print(f'y_test with y_pred ({method}) saved successfully at: {file_path}')

# Define weights
weights = get_weights('Datasets_SD','TrainDataset_SD.dat')
arm_weights = get_weights('Datasets_SD','ArmDataset_SD.dat')
leg_weights = get_weights('Datasets_SD','LegDataset_SD.dat')


# === === === ===
# Dataset dictionary
dataset_mapping = {
    'std': 
    {
        'folder': 'Datasets_SD',
        'test_file': 'TestDataset_SD.dat',
        'train_file': 'TrainDataset_SD.dat',
        'arm_file': 'NewArmDataset_SD.dat',
        'leg_file': 'NewLegDataset_SD.dat'
    },  
    'liaw': 
    {
        'folder': 'Datasets_Liaw',
        'test_file': 'TestDataset_Liaw.dat',
        'train_file': 'TrainDataset_Liaw.dat',
        'arm_file': 'NewArmDataset_Liaw.dat',
        'leg_file': 'NewLegDataset_Liaw.dat'        
    }
}

# Initializing data targets
yTrainCollection = pd.read_csv('ytrain.csv',index_col=0)
yTestCollection = pd.read_csv('ytest.csv',index_col=0)
yTestCollection['Sum'] = yTestCollection[['Trunk', 'Leg', 'Arm', 'Speed', 'Fluency', 'Stability']].sum(axis=1)

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
# FOR neural network
if mode == 'NN':
    if option in dataset_mapping:
        dataset_info = dataset_mapping[option]

        # Set random seed for reproducibility
        np.random.seed(0)
        tf.random.set_seed(0)


        # === === === ===
        # Initializing train data
        XtrainDF = get_dataset(dataset_info['folder'], dataset_info[targetFile])
        Xtrain = np.array(XtrainDF, np.float32)
        yTrainDF = yTrainCollection[target_variable]
        yTrain = np.array(yTrainDF, np.float32)


        # === === === ===
        # Initializing test data
        XtestDF = get_dataset(dataset_info['folder'], dataset_info['test_file'])

        print("Target Variable:", target_variable)

        # Special for Arm and Leg Dataset, trim Xtest to only contain relevant
        # features
        if (target_variable == "Leg") or (target_variable == "Arm"):
            XtestDF = XtestDF[XtrainDF.columns]

        Xtest = np.array(XtestDF, np.float32)
        yTest = np.array(yTestCollection[target_variable], np.float32)


        # === === === ===
        # Grid search for the best number of layers and nodes
        def create_model(layers, nodes):
            model = keras.Sequential()
            model.add(
                keras.layers.Dense(
                nodes, activation="relu", input_shape=(Xtrain.shape[1],)
                )
            )
        
            for i in range(1, layers):
                model.add(keras.layers.Dense(nodes, activation='relu'))

            model.add(keras.layers.Dense(1))
            model.compile(loss="mse", optimizer="adam")

            return model

        layers_range = [1, 2, 3]  # Range of number of layers to test
        nodes_range = [32, 64, 128, 256, 512]  # Range of number of nodes to test
        
        param_grid = {'layers': layers_range, 'nodes': nodes_range}
        model = KerasRegressor(
            build_fn=create_model, 
            verbose=0
        )
        cross = KFold(n_splits=10, shuffle=False)
        grid_search = GridSearchCV(
            estimator=model, 
            param_grid=param_grid, 
            cv=cross, 
            scoring='r2'
        )
        grid_result = grid_search.fit(Xtrain, yTrain)

        
        # === === === ===
        # For feature selection
        # Construct the base folder path for feature_list
        feature_list_base_path = os.path.join(os.getcwd(), 'feature_list')

        # Construct the folder path based on the input arguments
        folder_path = os.path.join(feature_list_base_path, option, target_variable)

        # Construct the file names based on the task
        file_names = [
            'mean.txt', 
            'random1.txt', 
            'random2.txt', 
            'stacking1.txt', 
            'stacking2.txt', 
            'voting.txt'
        ]
        
        # Load the content of the selected feature file
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            
            # Check if the file exists
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    selected_features = file.read().splitlines()
                    
                num_features_to_keep = int(0.1 * len(yTrainCollection[target_variable]))
                XtrainDF_selected = XtrainDF[selected_features[:num_features_to_keep]]
                XtestDF_selected = XtestDF[selected_features[:num_features_to_keep]]


        # === === === ===
        # Save NN models
        if task == 'Save':
            # Folder to store all models
            nn_models_folder = os.path.join(os.getcwd(), 'NN_models')
            if not os.path.exists(nn_models_folder):
                os.makedirs(nn_models_folder)
    
            #  Create subfolders
            dataset_folder = dataset_info['folder']
            nn_dataset_folder = os.path.join(nn_models_folder, f'NN{option}')
            if not os.path.exists(nn_dataset_folder):
                os.makedirs(nn_dataset_folder)

            # Save the trained model using TensorFlow's model saving mechanism
            model_filename = os.path.join(nn_dataset_folder, f'best_model_{target_variable}')
            if not os.path.exists(nn_dataset_folder):
                os.makedirs(nn_dataset_folder)
            grid_result.best_estimator_.model.save(model_filename)

            print(f"Trained model saved as {model_filename}")

        # === === === ===
        # Load NN models
        elif task == 'Load':
            dataset_info = dataset_mapping[option]
            nn_models_folder = os.path.join(os.getcwd(), 'NN_models')
            nn_dataset_folder = os.path.join(nn_models_folder, f'NN{option}')
            model_filename = os.path.join(nn_dataset_folder, f'best_model_{target_variable}')

            if os.path.exists(model_filename):
                # Load the saved model
                loaded_model = keras.models.load_model(model_filename)


        # === === === ===
        # Train NN models
        elif task == 'Train':
            # Xtrain 
            Xtrain_selected = np.array(XtrainDF_selected, np.float32)

            # Xtest
            Xtest_selected = np.array(XtestDF_selected, np.float32)
            
            # Train model with selected features
            grid_search.fit(Xtrain_selected, yTrain)
            
            # Predict using the trained model
            y_pred = grid_search.predict(Xtest_selected)

            best_layers = grid_result.best_params_['layers']
            best_nodes = grid_result.best_params_['nodes']

            print("Best number of layers:", best_layers)
            print("Best number of nodes:", best_nodes)

            # Flatten y_pred
            y_pred = y_pred.flatten()
        
            # R2 score
            r2 = r2_score(yTest, y_pred)
            print(f"R2 score: {r2}")
        
        else:
            print("Invalid option. Use 'Save' or 'Load' or 'Train'.")
    else:
        print("Invalid option. Use 'std' or 'liaw'.")


# === === === ===
# FOR sklearn tree based regressors
# Parameter library for HPT
elif mode == 'SK':
    model_params = {
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

        # 'RFR':{
        #     'model': RandomForestRegressor(),
        #     'params': {
        #         'n_estimators': [50, 100, 500, 1000],
        #         'random_state':[0]
        #     }
        # },

        # 'ABR':{
        #     'model': AdaBoostRegressor(),
        #     'params': {
        #         'n_estimators': [50, 100, 500, 1000],
        #         'random_state':[0]
        #     }
        # },

        # 'BR':{
        #     'model': BaggingRegressor(),
        #     'params': {
        #         'n_estimators': [50, 100, 500, 1000],
        #         'random_state':[0]
        #     }
        # },

        # 'GBR':{
        #     'model': GradientBoostingRegressor(),
        #     'params': {
        #         'n_estimators': [50, 100, 500, 1000],
        #         'random_state':[0]
        #     }
        # }
    }
    
    
    # === === === ===
    # Initialize train and test data
    if option in dataset_mapping:
        dataset_info = dataset_mapping[option]

        # Train data
        XtrainDF = get_dataset(dataset_info['folder'], dataset_info[targetFile])
        yTrain = yTrainCollection[target_variable]

        # Test data
        XtestDF = get_dataset(dataset_info['folder'], dataset_info['test_file'])
        yTest = yTestCollection[target_variable]

        # === === === ===
        # For hyperparameter tuning
        for classifier_name, classifier_params in model_params.items():
            classifier = classifier_params['model']
            param_grid = classifier_params['params']

            # To loop through each 
            for target_variable in target_variables: 
                cross = KFold(n_splits=10, shuffle=False)
                grid_search = GridSearchCV(
                    classifier, 
                    param_grid, 
                    scoring='r2', 
                    cv=cross
                )
                grid_search.fit(
                    XtrainDF, 
                    yTrain, 
                    sample_weight=weights
                )

                # Special for Arm and Leg Dataset, trim Xtest to only contain relevant
                # features
                if (target_variable == "Leg") or (target_variable == "Arm"):
                    XtestDF = XtestDF[XtrainDF.columns]


                # === === === ===
                # Load SK models
                if task == 'Save':
                    # Folder to store all models
                    sk_models_folder = os.path.join(os.getcwd(), 'SK_models')
                    if not os.path.exists(sk_models_folder):
                        os.makedirs(sk_models_folder)
        
                    # Create folder for each dataset and classifier
                    folderName = os.path.join(sk_models_folder, f'SK_{dataset_info["folder"]}_{classifier_name}')
                    if not os.path.exists(folderName):
                        os.makedirs(folderName)
        
                    # Save the trained model using pickle
                    model_filename = f'{folderName}/{classifier_name}_{target_variable}_model.pickle'
                    with open(model_filename, 'wb') as model_file:
                        pickle.dump(grid_search.best_estimator_, model_file)
        
                    print(f"Trained {classifier_name} model for {target_variable} saved as {model_filename}")

                # === === === ===
                # Load SK models
                elif task == 'Load':
                    if option in dataset_mapping:
                        dataset_info = dataset_mapping[option]
                        sk_models_folder = os.path.join(os.getcwd(), 'SK_models')
            
                        # Iterate over the classifiers and target variables
                        for classifier_name, classifier_params in model_params.items():
                            for target_variable in target_variables:
                                folderName = os.path.join(sk_models_folder, f'SK_{dataset_info["folder"]}_{classifier_name}')
                                model_filename = f'{folderName}/{classifier_name}_{target_variable}_model.pickle'
            
                                if os.path.exists(model_filename):
                                    # Load the saved model using pickle
                                    with open(model_filename, 'rb') as model_file:
                                        loaded_model = pickle.load(model_file) 
                                        print(loaded_model)

                elif task == 'Train':
                    # Construct the base folder path for feature_list
                    feature_list_base_path = os.path.join(os.getcwd(), 'feature_list', 'ensemble')

                    # Define the folder names for the three methods
                    method_folders = ['borda']

                    # Load and train model for each method
                    file_name = f'borda_{option}_{target_variable}.csv'
                    file_path = os.path.join(feature_list_base_path, 'borda', file_name)

                    # Check if the file exists
                    if os.path.exists(file_path):
                        # Load the feature list from the CSV file
                        selected_features_df = pd.read_csv(file_path, index_col=0)

                        # Sort features based on scores in descending order and select top 100 features
                        num_features_to_keep = int(0.1 * len(yTrainCollection[target_variable]))
                        sorted_features = selected_features_df['x'].sort_values(ascending=False)
                        top_features = sorted_features.index[:num_features_to_keep]
                        XtrainDF_selected = XtrainDF[top_features]
                        XtestDF_selected = XtestDF[top_features]

                        # Train model with selected features
                        grid_search.fit(XtrainDF_selected, yTrain, sample_weight=weights)

                        # Predict using the trained model
                        y_pred = grid_search.predict(XtestDF_selected)

                        # Call the function to save y_test with appended y_pred column
                        save_y_pred(mode, option, 'borda', yTest, y_pred)
                        
                        # R2 score
                        # balance_score = r2_score(yTest, y_pred)
                        # print(f'{classifier_name}({option}) - {target_variable} score(borda) = {balance_score}')
                        # print("Best parameters:", grid_search.best_params_) 

                        # === === === ===
                        # Folder to store all models
                        # sk_models_folder = os.path.join(os.getcwd(), 'SK_models')
                        # if not os.path.exists(sk_models_folder):
                        #     os.makedirs(sk_models_folder)
            
                        # # Create folder for each dataset and classifier
                        # folderName = os.path.join(sk_models_folder, f'SK_{dataset_info["folder"]}_{classifier_name}')
                        # if not os.path.exists(folderName):
                        #     os.makedirs(folderName)
            
                        # # Save the trained model using pickle
                        # model_filename = f'{folderName}/{classifier_name}_{target_variable}_{method_folder}.pickle'
                        # with open(model_filename, 'wb') as model_file:
                        #     pickle.dump(grid_search.best_estimator_, model_file)
            
                        # print(f"Trained {classifier_name} model for {target_variable} saved as {model_filename}")
    
                    else:
                        print(f"File not found for method: {method_folders}")
                else:
                    print("Invalid option. Use 'Save' or 'Load' or 'Train'.")
    else:
        print("Invalid option. Use 'std' or 'liaw'.")
else:
    print("Invalid execution mode. Use 'NN' or 'SK'.")