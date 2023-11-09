import pickle
import shap
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import os

if len(sys.argv) < 5:
    print(
        "Usage: python shapSVM.py <model> <dataset> <labels> " + 
        "<bordaFeatureList> <target>"
        )
    sys.exit()
else:
    trainedModel = Path(sys.argv[1])
    datasetPath = Path(sys.argv[2])
    labelsPath = Path(sys.argv[3])
    bordaFeatureList = Path(sys.argv[4])
    target = sys.argv[5]

# Loading the dataset    
Xtrain = pd.read_table(datasetPath, sep=' ', index_col=0)

# Trimming the dataset according to the Borda ranked feature ensemble method
selectedFeaturesDf = pd.read_csv(bordaFeatureList, index_col=0)
sortedFeatures = selectedFeaturesDf['x'].sort_values(ascending=False)
topFeatures = sortedFeatures.index[:int(0.1*Xtrain.shape[0])]   # 0.1 * Xtrain.shape[0]
XtrainReduced = Xtrain[topFeatures]

# Loading the labels
ytrain = pd.read_table(labelsPath, sep=',', index_col=0)[target]

# Loading the trained model 
with open(trainedModel, 'rb') as modelFile:
    loadedModel = pickle.load(modelFile)

# Create a SHAP explainer for model 
explainer = shap.Explainer(
    loadedModel.predict, masker=XtrainReduced.values,
    feature_names=list(XtrainReduced.columns), seed=0,
    max_evals=2 * XtrainReduced.shape[1] + 1
)

# To be done:
# 1. Group samples according to subscore
scoreGroups = {}

for score, group in ytrain.groupby(ytrain):
    scoreGroups[score] = group

# 2. Rank features according to sum of absolute SHAP values per subscore group
for score, group in scoreGroups.items():
    # Extract IDs and scores for the current group
    ids = group.index.tolist()
    group_scores = group.values

    # Filter the XtrainReduced dataframe for the current group
    X_group = XtrainReduced.loc[ids]
    shap_values_sum = np.zeros(X_group.shape[1])
    sum_shap_values_df = pd.DataFrame(columns=X_group.columns)
    # shap_values_df = pd.DataFrame(index=X_group.index, columns=X_group.columns)
    
    for idx, row in X_group.iterrows():
        # Compute SHAP values for the current group
        shap_values_row = explainer(row.values.reshape(1, -1)).values[0]
        # shap_values_df.loc[idx] = np.abs(shap_values_row.values[0])
        shap_values_sum += np.abs(shap_values_row)
    
    sum_shap_values_row = pd.Series(shap_values_sum, index=X_group.columns, name=target)
    sum_shap_values_df = sum_shap_values_df.append(sum_shap_values_row)
    sum_shap_values_df = sum_shap_values_df.sort_values(by=sum_shap_values_df.index[0], axis=1, ascending=False)

    # 3. Naming folders
    test = dataset_type = sys.argv[1].split("_")[-1].split(".")[0]  # split("_")[-4] for SVM
    dataset_type = os.path.basename(sys.argv[1]).split("_")[0]
    output_file_name = f"{score}_{test}_{dataset_type}_{target}.csv"
    sum_shap_values_df.to_csv(output_file_name, index=True)

# Deriving explanation for a given prediction
# shapValues_test = explainer(
#     XtrainReduced.values[0,:].reshape(1, XtrainReduced.shape[1])
#     )
# shapAbsValues_test = abs(shapValues_test.values)
# print(XtrainReduced.values[0,:])

# # Visualize
# shap.plots.waterfall(shapValues_test[0])