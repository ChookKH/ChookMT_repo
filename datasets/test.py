import pandas as pd

yTrainCollection = pd.read_csv('ytest.csv',index_col=0)
num_features_to_keep = int(0.1 * len(yTrainCollection))
print(num_features_to_keep)