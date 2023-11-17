import pandas as pd
import numpy as np
import os, io, zipfile, sys, shutil

class healthy_data:

    def __init__(self, _refbandDir):

        # Obtaining healthy gait event durations, parameters and phases
        self.gaitEvents, self.gaitParameters, self.gaitPhases = self.initialize_hData(_refbandDir)

    def initialize_hData(self, _refbandDir):
        '''
        Extract healthy gait event durations, parameter and phases
        '''
        # Read .dat file
        with open(_refbandDir.joinpath("RefBand_GaitPE_repTrials_n1.dat"), mode='r') as file:
            h_data = file.read()

        # Classify into phase duration, parameters and phases
        h_df = pd.read_csv(io.StringIO(h_data), sep=' ')
        h_df = h_df.rename(columns={'Unnamed: 0': 'Measure'})

        gait_events = h_df.iloc[:6, :]
        gait_parameters = h_df.iloc[6:18, :]
        gait_phases = h_df.iloc[18:, :]

        return gait_events, gait_parameters, gait_phases

    def unravel(self, dataFrame):
        '''
        Unravel the 3 min, median and max columns into 1 column
        '''
        return (
            dataFrame

            # Reset the index, adding a new column 'index'
            .reset_index()

            # - Lambda function to split column names into a list (check if column name has __)
            # - No seperator (__) then return original name
            .rename(columns=lambda x: x.split('__') if '__' in x else x)

            # - Reshape the dataframe from columns to rows
            # - 'OriIndex' column kept as identifier
            # - Remaining columns (min, median, max) considered as value variables
            # - New 'variable' column = min, median, max
            # - New 'value' column = numbers
            .melt(id_vars='OriIndex', value_vars=dataFrame.columns)

            # Remove any rows that are missing values
            .dropna()

            # - Create new column 'OriIndex' by concatenating 'OriIndex' column
            #   with 'variable' column, seperated by '__'
            .assign(OriIndex=lambda df: df['OriIndex'] + '__' + df['variable'])

            # Rename 'value' column to 'Status'
            .rename(columns={'value': 'Status'})

            # Set 'OriIndex' as new index
            .set_index('OriIndex')

            # Display only the 'Status' column from the dataframe, making it only 1 column
            [['Status']]
        )

    # Gait parameter series (within refband check, within = 0, else = 1)
    def check_within_limits(self, gpSeries, lowerLimits, upperLimits):
        '''
        Compare Aff subject gait parameter series with healthy subjects
        '''
        withinCheck = pd.Series(
            np.where(
                (gpSeries >= lowerLimits) & (gpSeries <= upperLimits),
                0, 1
            ),index=gpSeries.index, name='Result'
        )

        return withinCheck
