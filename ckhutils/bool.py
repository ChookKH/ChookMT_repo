import pandas as pd

def bool_output(seriesAff):
    
    h_gait = pd.read_excel('healthy_gait.xlsx')
    h_gait_series = h_gait.set_index('Gait Parameter')['Computed Mean']
    h_gait_series = h_gait_series.rename_axis(None)
    seriesAff.index = seriesAff.index.str.split('Aff').str[0]
    result = (h_gait_series >= seriesAff).astype(float)

    print(result)