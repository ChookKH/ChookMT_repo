import pandas as pd
import os
import io
import zipfile

zip_path = os.path.join(os.pardir, 'testSubjectsCollective.zip')

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for filename in zip_ref.namelist():
        if filename.endswith('.dat'):
            with zip_ref.open(filename) as file:
                for line in file:
                    df = pd.read_csv(file, sep=' ', index_col=0, header=None)
                    df.index.name = 'Stats'
                    if filename == 'InCnt.dat':
                        df.columns = ['Measurement']
                        
                    # new_df = df.agg(['Min', 'Median', 'Max'])
                    else:    
                        df.columns = ['Min', 'Median', 'Max']
                    print(df)
                        
