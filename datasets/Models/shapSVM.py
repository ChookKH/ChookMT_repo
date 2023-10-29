import pickle
import shap
import sys
from pathlib import Path
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
    feature_names=list(XtrainReduced.columns), seed=0,
)

# To be done:
# 1. Group samples according to subscore
# 2. Rank features according to sum of absolute SHAP values per subscore group

# Deriving explanation for a given prediction
shapValues_test = explainer(
    XtrainReduced.values[0,:].reshape(1, XtrainReduced.shape[1])
    )
shapAbsValues_test = abs(shapValues_test.values)
print(shapAbsValues_test)

# Visualize
shap.plots.waterfall(shapValues_test[0])