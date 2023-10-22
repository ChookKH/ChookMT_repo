from sklearn.tree import export_graphviz
import pandas as pd
import graphviz
from graphviz import Source
import pickle
import sys
from pathlib import Path

if len(sys.argv) < 4:
    print("Usage: python visualize.py <model> <dataset> <savefile>")
    sys.exit()
else:
    trainedModel = Path(sys.argv[1])
    datasetPath = Path(sys.argv[2])
    savefile = sys.argv[3]

# Loading the dataset    
dataset = pd.read_table(datasetPath, sep=' ', index_col=0)

# Loading the trained model 
with open(trainedModel, 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Export the model to a DOT file
dot_data = export_graphviz(
    loaded_model, out_file=None,
    feature_names=loaded_model.feature_names_in_,
    filled=True, rounded=True
)
graph = graphviz.Source(dot_data)
graph = Source(dot_data, filename=savefile, format="png")
graph.view()

sys.exit(0)