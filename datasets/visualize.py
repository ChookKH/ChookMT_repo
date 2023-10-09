from sklearn.tree import export_graphviz
from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
import graphviz
from graphviz import Source
import pickle
import sys
import os
import io

# if len(sys.argv) != 2:
#     print("Usage: python .\visualize.py option")
#     sys.exit()

# option = sys.argv[1]

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

# if option == 'vis':    
dataset = get_dataset('Datasets_Liaw', 'NewArmDataset_Liaw.dat')
feature_list = dataset.columns.tolist()

# Specify the pickle path
pickle_dir = 'D:\ChookMT_repo\datasets\SK_models\SK_Datasets_Liaw_TR'
pickle_folder = 'TR_Arm_model.pickle'
pickle_path = os.path.join(pickle_dir,pickle_folder)
with open(pickle_path, 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Export the model to a DOT file
dot_file = 'model.dot'
export_graphviz(
    loaded_model,
    out_file=dot_file,
    feature_names=feature_list,
    filled=True,
    rounded=True

)
# Render the DOT file as a PNG image
output_image = 'model_tree.png'
src = Source.from_file(dot_file, format='png')
src.render(output_image, view=True)
print(f"Model tree visualization saved as {output_image}")