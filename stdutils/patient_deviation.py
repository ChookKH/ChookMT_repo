import os, sys
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict

class patient_refband_grouping:
    '''
    Class that contains the dataframes related to the test subjects aggregate/norm and selected patient.

    Contains information on the mean, lower and upper confidence interval of each of the
    kinematical parameter.

    In this version the patient's kinematic data will be more comprehensive in the sense that
    the selected features are normalized according to that joint side

    Example:
        - The affected ankle joint angles will be normalized with respect to the affected side
            whereas the unaffected side with respect to the unaffected side
    '''
    def __init__(self, _aggnorm_dir, _patient, _trial, CI):
        self.aggnorm_dir = _aggnorm_dir
        self.patient = _patient
        self.trial = _trial
        self.CI = CI

        self.affside = self.get_affectedside()

        # Reading and setting the dataframes to the appropriate class properties
        self.get_aggnorm_mean_data()
        # >> self.aggMean_aff | self.aggMean_unaff
        self.get_aggnorm_errorinterval_data()
        # >> self.aggUpper_aff | self.aggLower_aff | self.aggUpper_unaff | self.aggLower_unaff
        self.get_patient_data()
        # >> self.pat_aff | self.pat_unaff | self.patEvents_aff | self.patEvents_unaff

        self.patEventsDict_aff = self.read_gaitparameters(self.patEvents_aff)
        self.patEventsDict_unaff = self.read_gaitparameters(self.patEvents_unaff)

        # Main task: Renaming the feature labels accordingly
        self.process_feature_labels()
        # >> self.aggMean_corr | self.aggLower_corr | self.aggUpper_corr | self.pat_corr
        # >> self.affNormFeatures | self.unaffNormFeatures


    def get_affectedside(self):
        '''
        Get affected side of the patient based on the name of the saved .dat files
        '''
        rData_name = (self.trial.RightNormalizedData.name).split("_")[-1]
        lData_name = (self.trial.LeftNormalizedData.name).split("_")[-1]

        if (rData_name == "affRight.dat") and (lData_name == "unaffLeft.dat"):
            affside = "r"
        elif (rData_name == "unaffRight.dat") and (lData_name == "affLeft.dat"):
            affside = "l"
        else:
            raise ValueError("Unexpected error, could not determine affected side. Contact administrator")

        return affside


    def get_aggnorm_mean_data(self):
        '''
        Gets the appropriate aggregated test subject data in forming the reference bands
        '''
        # Select the appropriate test subject aggregated data according to the desired normalized side
        if self.affside == "r":
            self.aggMean_aff = pd.read_table(
                self.aggnorm_dir.joinpath("rMean.dat"),
                sep=' ',
                low_memory=False
            )
            self.aggMean_unaff = pd.read_table(
                self.aggnorm_dir.joinpath("lMean.dat"),
                sep=' ',
                low_memory=False
            )
        elif self.affside == "l":
            self.aggMean_aff = pd.read_table(
                self.aggnorm_dir.joinpath("lMean.dat"),
                sep=' ',
                low_memory=False
            )
            self.aggMean_unaff = pd.read_table(
                self.aggnorm_dir.joinpath("rMean.dat"),
                sep=' ',
                low_memory=False
            )
        else:
            raise ValueError("Unexpected error, could not determine affected side. Contact administrator")


    def get_aggnorm_errorinterval_data(self):
        '''
        Importing the dataframes for the upper and lower boundaries of the confidence interval
        '''
        if self.affside == "r":
            if self.CI == "std":
                # Affected side (right), standard deviation
                self.aggUpper_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("rUpperStd.dat"),
                    sep=' '
                )
                self.aggLower_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("rLowerStd.dat"),
                    sep=' '
                )

                # Unaffected side (left), standard deviation
                self.aggUpper_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("lUpperStd.dat"),
                    sep=' '
                )
                self.aggLower_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("lLowerStd.dat"),
                    sep=' '
                )
            elif self.CI == "ci":
                # Affected side (right), confidence interval
                self.aggUpper_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("rUpperCis.dat"),
                    sep=' '
                )
                self.aggLower_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("rLowerCis.dat"),
                    sep=' '
                )

                # Unaffected side (right), confidence interval
                self.aggUpper_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("lUpperCis.dat"),
                    sep=' '
                )
                self.aggLower_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("lLowerCis.dat"),
                    sep=' '
                )
            else:
                raise ValueError("Error band must either be of type \"ci\" or \"std\"")

        elif self.affside == "l":
            if self.CI == "std":
                # Affected side (left), standard deviation
                self.aggUpper_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("lUpperStd.dat"),
                    sep=' '
                )
                self.aggLower_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("lLowerStd.dat"),
                    sep=' '
                )

                # Unaffected side (right), standard deviation
                self.aggUpper_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("rUpperStd.dat"),
                    sep=' '
                )
                self.aggLower_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("rLowerStd.dat"),
                    sep=' '
                )
            elif self.CI == "ci":
                # Affected side (left), confidence interval
                self.aggUpper_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("lUpperCis.dat"),
                    sep=' '
                )
                self.aggLower_aff = pd.read_table(
                    self.aggnorm_dir.joinpath("lLowerCis.dat"),
                    sep=' '
                )

                # Unaffected side (right), confidence interval
                self.aggUpper_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("rUpperCis.dat"),
                    sep=' '
                )
                self.aggLower_unaff = pd.read_table(
                    self.aggnorm_dir.joinpath("rLowerCis.dat"),
                    sep=' '
                )
            else:
                raise ValueError("Error band must either be of type \"ci\" or \"std\"")


    def get_patient_data(self):
        '''
        Gets the patient's body kinematical data and setting them to the appropriate class field
        '''
        # Reading the dataframes
        self.trial.getData()

        # Affected side data
        if self.affside == "r":
            # Body kinematical data
            self.pat_aff   = self.trial.RightNormDF
            self.pat_unaff = self.trial.LeftNormDF

            # Gait parameters
            self.patEvents_aff   = Path(self.trial.FolderPath).joinpath(f"{self.trial.TrialID}_eventsRightNorm.dat")
            self.patEvents_unaff = Path(self.trial.FolderPath).joinpath(f"{self.trial.TrialID}_eventsLeftNorm.dat")

        elif self.affside == "l":
            # Body kinematical data
            self.pat_aff   = self.trial.LeftNormDF
            self.pat_unaff = self.trial.RightNormDF

            # Gait parameters
            self.patEvents_aff   = Path(self.trial.FolderPath).joinpath(f"{self.trial.TrialID}_eventsLeftNorm.dat")
            self.patEvents_unaff = Path(self.trial.FolderPath).joinpath(f"{self.trial.TrialID}_eventsRightNorm.dat")
        else:
            raise ValueError("Unexpected error, could not determine affected side. Contact administrator")


    def read_gaitparameters(self, _patEvents):
        '''
        Read the gait parameters file and assigning them to the corresponding class property based on the
        patient's affected side
        '''
        # Gait parameters for the affected side of the patient
        patEventsDict = defaultdict(str)
        f = open(_patEvents, mode='r')
        lines = [line.replace("\n", "") for line in f if not (("Events:" in line) or ("Gait parameters" in line))]
        f.close()

        # Initializing the patEventsDict dictionary
        for line in lines:
            linesplits = line.split("  ")

            if len(linesplits) == 4:
                self.rename_footstrikes_gaitevents(
                    linesplits[2],
                    linesplits[1],
                    linesplits[3],
                    patEventsDict
                )
            elif len(linesplits) == 3:
                patEventsDict[linesplits[2]] = linesplits[1]
            else:
                raise ValueError("Unexpected eror encountered while reading gait paramters file. Please contact administrator")

        return patEventsDict


    def rename_footstrikes_gaitevents(self, _side, _value, _event, _patEventsDict):
        '''
        Private method to deal with the foot strike gait events, since they repeat. First strike
        is renamed with an "initial" suffix and the other "end"
        '''
        # Patient affected on the right side
        if self.affside == "r":
            # Affected side
            if (_side == "RIGHT") and (_value == "0"):
                _patEventsDict[f"AFF INI. {_event}"] = _value
            elif (_side == "RIGHT") and (_value == "1"):
                _patEventsDict[f"AFF END {_event}"] = _value
            elif _side == "RIGHT":
                _patEventsDict[f"AFF {_event}"] = _value

            # Unaffected side
            elif (_side == "LEFT") and (_value == "0"):
                _patEventsDict[f"UNAFF INI. {_event}"] = _value
            elif (_side == "LEFT") and (_value == "1"):
                _patEventsDict[f"UNAFF END {_event}"] = _value
            elif _side == "LEFT":
                _patEventsDict[f"UNAFF {_event}"] = _value

        # Patient affected on the left side
        elif self.affside == "l":
            if (_side == "LEFT") and (_value == "0"):
                _patEventsDict[f"AFF INI. {_event}"] = _value
            elif (_side == "LEFT") and (_value == "1"):
                _patEventsDict[f"AFF END {_event}"] = _value
            elif _side == "LEFT":
                _patEventsDict[f"AFF {_event}"] = _value

            # Unaffected side
            elif (_side == "RIGHT") and (_value == "0"):
                _patEventsDict[f"UNAFF INI. {_event}"] = _value
            elif (_side == "RIGHT") and (_value == "1"):
                _patEventsDict[f"UNAFF END {_event}"] = _value
            elif _side == "RIGHT":
                _patEventsDict[f"UNAFF {_event}"] = _value


    def process_feature_labels(self):
        '''
        The main task of this method is to rename the feature labels according to the patient's affected side
        '''
        self.aggMean_corr  = pd.DataFrame()
        self.aggLower_corr = pd.DataFrame()
        self.aggUpper_corr = pd.DataFrame()
        self.pat_corr      = pd.DataFrame()

        # Generating a list containing features normalized to the affected and
        # unaffected side
        self.affNormFeatures   = []
        self.unaffNormFeatures = []

        # Looping through the aggregated test subjects mean kinematical values columns names
        # Doesn't matter which dataframe is actually use, they all have the same column names
        columnList = self.aggMean_aff.columns
        for i in range(len(columnList)):
            col = columnList[i]
            if "Right" in col:
                if self.affside == "r":
                    newCol = col.replace("Right", "Aff")
                    self.aggMean_corr[newCol]  = self.aggMean_aff[col]
                    self.aggLower_corr[newCol] = self.aggLower_aff[col]
                    self.aggUpper_corr[newCol] = self.aggUpper_aff[col]
                    self.pat_corr[newCol]      = self.pat_aff[col]
                    self.affNormFeatures.append(newCol)
                else:
                    newCol = col.replace("Right", "UnAff")
                    self.aggMean_corr[newCol]  = self.aggMean_unaff[col]
                    self.aggLower_corr[newCol] = self.aggLower_unaff[col]
                    self.aggUpper_corr[newCol] = self.aggUpper_unaff[col]
                    self.pat_corr[newCol]      = self.pat_unaff[col]
                    self.unaffNormFeatures.append(newCol)

            elif "Left" in col:
                if self.affside == "r":
                    newCol = col.replace("Left", "UnAff")
                    self.aggMean_corr[newCol]  = self.aggMean_unaff[col]
                    self.aggLower_corr[newCol] = self.aggLower_unaff[col]
                    self.aggUpper_corr[newCol] = self.aggUpper_unaff[col]
                    self.pat_corr[newCol]      = self.pat_unaff[col]
                    self.unaffNormFeatures.append(newCol)
                else:
                    newCol = col.replace("Left", "Aff")
                    self.aggMean_corr[newCol]  = self.aggMean_aff[col]
                    self.aggLower_corr[newCol] = self.aggLower_aff[col]
                    self.aggUpper_corr[newCol] = self.aggUpper_aff[col]
                    self.pat_corr[newCol]      = self.pat_aff[col]
                    self.affNormFeatures.append(newCol)
            else:
                self.aggMean_corr[col]  = self.aggMean_aff[col]
                self.aggLower_corr[col] = self.aggLower_aff[col]
                self.aggUpper_corr[col] = self.aggUpper_aff[col]
                self.pat_corr[col]      = self.pat_aff[col]
                self.affNormFeatures.append(col)
