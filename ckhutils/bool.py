import os, io
import pandas as pd

def bool_output(seriesAff):
    '''
    Function to compare a healthy gait parameters with the gait parameters from subject
    '''
    h_gait = pd.read_excel(
        'healthy_gait.xlsx', engine="openpyxl",
        usecols="A:B", nrows=12
    )

    h_gait_series = h_gait.set_index('Gait Parameter')['Computed Mean']
    h_gait_series = h_gait_series.rename_axis(None)
    seriesAff.index = seriesAff.index.str.split('Aff').str[0]
    result = (h_gait_series >= seriesAff).astype(float)

    print(h_gait_series)
    print(result)


def series_compare(seriesPatient, seriesHealthy):
    '''
    Function to compare subject and healthy subject, converting into bool
    '''
    series_bool = (seriesPatient <= seriesHealthy).astype(float)
    print(series_bool)
