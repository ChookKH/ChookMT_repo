import pickle
import shap
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import os

if len(sys.argv) < 6:
    print(
        "Usage: python shapSVM.py <model> <dataset> <labels> " + 
        "<bordaFeatureList> <target> <subscore>"
        )
    sys.exit()
else:
    ### Can tidy up by creating methods in a class
    trainedModel = Path(sys.argv[1])
    datasetPath = Path(sys.argv[2])
    labelsPath = Path(sys.argv[3])
    bordaFeatureList = Path(sys.argv[4])
    target = sys.argv[5]
    subscore = int(sys.argv[6])

# Loading the dataset    
Xtrain = pd.read_table(datasetPath, sep=' ', index_col=0)

# Trimming the dataset according to the Borda ranked feature ensemble method
selectedFeaturesDf = pd.read_csv(bordaFeatureList, index_col=0)
sortedFeatures = selectedFeaturesDf['x'].sort_values(ascending=False)
topFeatures = sortedFeatures.index[:int(0.1*Xtrain.shape[0])]  
XtrainReduced = Xtrain[topFeatures]

# Loading the labels
ytrain = pd.read_table(labelsPath, sep=',', index_col=0)[target]

# Loading the trained model 
with open(trainedModel, 'rb') as modelFile:
    loadedModel = pickle.load(modelFile)

# Create a SHAP explainer for model 
explainer = shap.Explainer(
    loadedModel.predict, masker=XtrainReduced.values,
    featureNames=list(XtrainReduced.columns), seed=0
)

# To be done:
# 1. Group samples according to subscore
scoreGroups = {}

for score, group in ytrain.groupby(ytrain):
    scoreGroups[score] = group

ids = scoreGroups[subscore].index.tolist()
groupScore = scoreGroups[subscore].values

# 2. Rank features according to sum of absolute SHAP values per subscore group
# Filter the XtrainReduced dataframe for the current group
XGroup = XtrainReduced.loc[ids]
shapArray = np.zeros(XGroup.shape[1])
shapDF = pd.DataFrame(columns=XGroup.columns)

for idx, row in XGroup.iterrows():
    # Compute SHAP values for the current group
    shapRow = explainer(row.values.reshape(1, -1)).values[0]
    shapArray += np.abs(shapRow)

sumRow = pd.Series(shapArray, index=XGroup.columns, name=target)
shapDF = shapDF.append(sumRow)
shapDF = shapDF.sort_values(by=shapDF.index[0], axis=1, ascending=False)

# Normalize the values by the number of stride pairs and abs subscore diff
numIds = len(ids)
baseValue = explainer(XtrainReduced.loc[ids[0]].values.reshape(1, -1)).base_values[0]
absDiff  = np.abs(baseValue - subscore)
shapDF = shapDF / (numIds * absDiff)

# 3. Naming folders
test = sys.argv[1].split("_")[-4].split(".")[0] 
datasetType = os.path.basename(sys.argv[1]).split("_")[0]
outputFileName = f"{subscore}_{test}_{datasetType}_{target}.csv"
shapDF.to_csv(outputFileName, index=True)

# Deriving explanation for a given prediction
# shapValues_test = explainer(
#     XtrainReduced.values[0,:].reshape(1, XtrainReduced.shape[1])
#     )
# shapAbsValues_test = abs(shapValues_test.values)
# print(shapValues_test)

# # Visualize
# shap.plots.waterfall(shapValues_test[0])