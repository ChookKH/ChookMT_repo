import pandas as pd

files = [
    'Arm_epochs1000_alphaHPTuning_sd_ckh.csv',
    'Fluency_epochs1000_alphaHPTuning_sd_ckh.csv',
    'Leg_epochs1000_alphaHPTuning_sd_ckh.csv',
    'Speed_epochs1000_alphaHPTuning_sd_ckh.csv',
    'Stability_epochs1000_alphaHPTuning_sd_ckh.csv',
    'Trunk_epochs1000_alphaHPTuning_sd_ckh.csv'
]

result = pd.DataFrame()
SMSnames = []

for file in files:
    # Read df
    df = pd.read_table(file, delimiter=',', index_col=0)
    df = df.reset_index(drop=True)
    bestIndex = df['avrR2'].idxmax()
    bestRow = df.loc[bestIndex]

    # Compile best params
    indexName = file.split('_')[0]
    SMSnames.append(indexName)
    result = result.append(bestRow)
    result = result.reset_index(drop=True)

result.index = SMSnames
result.index.name = None
result.to_csv('best_params.csv', index=True)