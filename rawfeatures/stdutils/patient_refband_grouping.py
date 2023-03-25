import os, sys
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
from stdutils.select_doubleStridePairs import select_commonPairs, initialize_gaitParametersIdxFileMap

class patient_refband_grouping:
    '''
    Class that contains the dataframes related to the reference band constructed from the collection of
    test subjects and the selected patient.

    Contains information on the mean, lower and upper confidence intervals of the reference band pertaining
    to each of the kinematical parameter.

    Each biomechanical angle of the patient's kinematic data is normalized according to the following scheme:
    1. Biomechanical angles on the lateral side are normalized with respect to the stride on the lateral side
    2. Biomechanical angles on the contralateral side are normalized with respect to the stride on the
       contralateral side
    3. Biomechanical angles in the middle (thorax, head) are normalized with respect to the stride on the
       lateral and contralateral side

    Parameters:
    -----------
    _rb_dir : pathlib.Path
    Path to the reference bands directory

    _trial : stdutils.patient.Trial
    Patient's trial object

    CI : str
    The type of confidence interval, either 'std' (standard deviation) or 'ci' (confidence interval)

    _testSubjectsSide : str or None
    Implemented on 25.02.2022 to accomodate for test subjects which will be included
    for feature selection. Available options: None, 'r', 'l'
    '''
    def __init__(self, _rb_dir, _trial, CI, _testSubjectsSide=None):
        self.rb_dir = _rb_dir; self.CI = CI
        self.affside = self.get_affectedside(_trial, testSubjectsSide=_testSubjectsSide)

        # === === === ===
        # Reading and setting the dataframes to the appropriate class properties
        # Reference bands
        self.get_rb_mean_data()
        # >> self.rbMean_aff | self.rbMean_unaff
        self.get_rb_errorinterval_data()
        # >> self.rbUpper_aff | self.rbLower_aff | self.rbUpper_unaff | self.rbLower_unaff
        self.get_rb_gEvents_data()
        # >> self.rbGEvents


        # === === === ===
        # Initializing dictionaries of features pertaining to the affected and unaffected side
        self.affNormFeatures, self.unaffNormFeatures = self.generate_featuresList(
            self.rbMean_aff
        )
        # >> self.affNormFeatures
        # dict{<oldName>: <newName>}


        # === === === ===
        # Patient
        self.patientstridesFileMap, self.noCommonPairs = self.get_patientDataFilePaths(_trial)
        # >> patientstridesFileMap
        # dict{idx:
        #     dict{'aff': {'kinematics': Path, 'gaitParameters': Path}}
        #     dict{'unaff': {'kinematics': Path, 'gaitParameters': Path}}
        # }
        # The values of this dictionary correspond to matching right and left normalized strides


        # Note: Each idx, correspond to a unique matching pair of affected and unaffected patient
        # stride body kinematics, which was matched earlier in the patientstridesFileMap dictionary
        self.patGPDict_aff = self.read_gaitparameters(self.patientstridesFileMap, "aff")
        self.patGPDict_unaff = self.read_gaitparameters(self.patientstridesFileMap, "unaff")
        # >> self.patGPDict_aff | self.patGPDict_unaff
        # dict{idx: dict{<patientGaitParameters>}


        # === === === ===
        # Main task: Renaming the feature labels accordingly
        self.rbMean_corr  = self.process_featureLabels(self.rbMean_aff, self.rbMean_unaff)
        self.rbLower_corr = self.process_featureLabels(self.rbLower_aff, self.rbLower_unaff)
        self.rbUpper_corr = self.process_featureLabels(self.rbUpper_aff, self.rbUpper_unaff)

        self.patCollection_corr = self.process_featureLabels_patientDoubleStrides(
            self.patientstridesFileMap
        )
        # >> self.patCollection_corr
        # dict{idx: pd.DataFrame()}


    def get_affectedside(self, _trial, testSubjectsSide=None):
        '''
        Get affected side of the patient based on the name of the saved .dat files
        '''
        # Simply take the first path in either the list self.trial.KinematicsR and
        # self.trial.KinematicsL
        # Example : ES010HR1937a-S-3Gang02_01_affRight.dat

        rData_name = (Path(_trial.KinematicsR[0]).name).split("_")[-1]
        lData_name = (Path(_trial.KinematicsL[0]).name).split("_")[-1]

        if testSubjectsSide == None:
            if (rData_name == "affRight.dat") and (lData_name == "unaffLeft.dat"):
                affside = "r"
            elif (rData_name == "unaffRight.dat") and (lData_name == "affLeft.dat"):
                affside = "l"
            else:
                raise ValueError(
                    "Unexpected error, could not determine affected side. Contact administrator"
                )
        else:
            if testSubjectsSide == 'r':
                affside = "r"
            elif testSubjectsSide == 'l':
                affside = "l"
            else:
                raise ValueError(
                    "Invalid input argument for designated \'affected side\' for test subject (r, l)"
                )

        return affside


    def get_rb_mean_data(self):
        '''
        Gets the appropriate aggregated test subject data in forming the reference bands
        '''
        # Select the appropriate test subject aggregated data according to the desired
        # normalized side
        if self.affside == "r":
            self.rbMean_aff = pd.read_table(
                self.rb_dir.joinpath("rMean.dat"),
                sep=' ',
                low_memory=False
            )
            self.rbMean_unaff = pd.read_table(
                self.rb_dir.joinpath("lMean.dat"),
                sep=' ',
                low_memory=False
            )
        elif self.affside == "l":
            self.rbMean_aff = pd.read_table(
                self.rb_dir.joinpath("lMean.dat"),
                sep=' ',
                low_memory=False
            )
            self.rbMean_unaff = pd.read_table(
                self.rb_dir.joinpath("rMean.dat"),
                sep=' ',
                low_memory=False
            )
        else:
            raise ValueError(
                "Unexpected error, could not determine affected side. Contact administrator"
            )


    def get_rb_errorinterval_data(self):
        '''
        Importing the dataframes for the upper and lower boundaries of the confidence interval
        '''
        if self.affside == "r":
            if self.CI == "std":
                rbUpper_aff_path = self.rb_dir.joinpath("rUpperStd.dat")
                rbLower_aff_path = self.rb_dir.joinpath("rLowerStd.dat")

                rbUpper_unaff_path = self.rb_dir.joinpath("lUpperStd.dat")
                rbLower_unaff_path = self.rb_dir.joinpath("lLowerStd.dat")

            elif self.CI == "ci":
                rbUpper_aff_path = self.rb_dir.joinpath("rUpperCis.dat")
                rbLower_aff_path = self.rb_dir.joinpath("rLowerCis.dat")

                rbUpper_unaff_path = self.rb_dir.joinpath("lUpperCis.dat")
                rbLower_unaff_path = self.rb_dir.joinpath("lLowerCis.dat")

            else:
                raise ValueError("Error band must either be of type \"ci\" or \"std\"")

        elif self.affside == "l":
            if self.CI == "std":
                rbUpper_aff_path = self.rb_dir.joinpath("lUpperStd.dat")
                rbLower_aff_path = self.rb_dir.joinpath("lLowerStd.dat")

                rbUpper_unaff_path = self.rb_dir.joinpath("rUpperStd.dat")
                rbLower_unaff_path = self.rb_dir.joinpath("rLowerStd.dat")

            elif self.CI == "ci":
                rbUpper_aff_path = self.rb_dir.joinpath("lUpperCis.dat")
                rbLower_aff_path = self.rb_dir.joinpath("lLowerCis.dat")

                rbUpper_unaff_path = self.rb_dir.joinpath("rUpperCis.dat")
                rbLower_unaff_path = self.rb_dir.joinpath("rLowerCis.dat")

            else:
                raise ValueError("Error band must either be of type \"ci\" or \"std\"")

        # Affected side (left), confidence interval
        self.rbUpper_aff = pd.read_table(rbUpper_aff_path, sep=' ')
        self.rbLower_aff = pd.read_table(rbLower_aff_path, sep=' ')

        # Unaffected side (right), confidence interval
        self.rbUpper_unaff = pd.read_table(rbUpper_unaff_path, sep=' ')
        self.rbLower_unaff = pd.read_table(rbLower_unaff_path, sep=' ')


    def get_rb_gEvents_data(self):
        '''
        Importing the dataframe containing the central tendencies (median) of the eight gait events of all
        the test subjects as a collective, for both the affected and unaffected stride normalized gait data.

        This method will also rename left and right to either affected or unaffected according to the
        patient's affected side
        '''
        self.rbGEvents = pd.read_table(self.rb_dir.joinpath("gEventsMedian.dat"), sep=' ', index_col=0)

        # Renaming accordingly
        if self.affside == 'l':
            self.rbGEvents = self.rbGEvents.rename(
                columns={'LeftNorm': 'AffNorm', 'RightNorm': 'UnAffNorm'}
            )
        elif self.affside == 'r':
            self.rbGEvents = self.rbGEvents.rename(
                columns={'LeftNorm': 'UnAffNorm', 'RightNorm': 'AffNorm'}
            )


    def get_patientDataFilePaths(self, _trial):
        '''
        Gets the patient's body kinematical data and setting them to the appropriate class field
        '''
        commonPairs, idxFileMapR, idxFileMapL = select_commonPairs(_trial)
        # Reminder, each value in the dictionary commonPairs is a list : [<leftNorm>, <rightNorm>]

        # Trial object has a list of right and left normalized gait parameters file paths, where
        # faulty data has been ignored
        gaitParIdxFileMapR, gaitParIdxFileMapL = initialize_gaitParametersIdxFileMap(_trial)

        # === === === ===
        '''
        Initializing a dictionary with the following structure
        {idx: {
            "aff": {
                "kinematics": <affKinematics_idx>,
                "gaitParameters": <affGaitParameters_idx>
            }
            "unaff": {
                "kinematics": <unaffKinematics_idx>,
                "gaitParameters": <unaffGaitParameters_idx>
            }
        }
        '''
        patientstrides = defaultdict()

        noCommonPairs = False

        if not len(commonPairs) == 0:
            for k in commonPairs.keys():
                l = commonPairs[k][0]; r = commonPairs[k][1]

                if ((l in idxFileMapL.keys() and l in gaitParIdxFileMapL.keys())
                    and (r in idxFileMapR.keys() and r in gaitParIdxFileMapR.keys())
                    ):

                    if self.affside == "r":
                        aff = {
                            "kinematics": idxFileMapR[r], "gaitParameters": gaitParIdxFileMapR[r]
                        }
                        unaff = {
                            "kinematics": idxFileMapL[l], "gaitParameters": gaitParIdxFileMapL[l]
                        }

                    elif self.affside == "l":
                        aff = {
                            "kinematics": idxFileMapL[l], "gaitParameters": gaitParIdxFileMapL[l]
                        }
                        unaff = {
                            "kinematics": idxFileMapR[r], "gaitParameters": gaitParIdxFileMapR[r]
                        }

                    else:
                        raise ValueError(
                            "Unexpected error, could not determine affected side. " +
                            "Contact administrator"
                        )

                    pair = {"aff": aff, "unaff": unaff}; patientstrides[k] = pair

                else:
                    self.print_missingData(l, idxFileMapL, "left", "kinematics")
                    self.print_missingData(r, idxFileMapR, "right", "kinematics")
                    self.print_missingData(l, gaitParIdxFileMapL, "left", "parameters")
                    self.print_missingData(r, gaitParIdxFileMapR, "right", "parameters")

        else:
            print(f"No common pairs could be found for the trial {_trial.TrialID} ... ")
            noCommonPairs = True


        return patientstrides, noCommonPairs


    def print_missingData(self, _i, _dict, _norm, _type):
        '''Sub-routine for the method get_patientDataFilePaths'''
        if _type == "kinematics":
            if not _i in _dict.keys():
                print(
                    f"The gait kinematics corresponding to stride ID, {_i} | {_norm} normalized was not " +
                    "considered due to faults found."
                )
        elif _type == "parameters":
            if not _i in _dict.keys():
                print(
                    f"The gait parameters corresponding to stride ID, {_i} | {_norm} normalized  was not " +
                    "considered due to faults found."
                )


    def read_gaitparameters(self, _patientStridesFileMap,  _side):
        '''
        Receives a dictionary mapping information pertaining to a patient's stride information to
        its corresponding data files (kinematics, gait parameters) and returns a dictionary
        mapping the patient's stride index to the corresponding gait parameters dictionary
        '''
        # Dictionary mapping patient's stride index to corresponding gait parameters
        patIdx_GP = defaultdict(dict)

        # The idx refers to the pair of affected and unaffected stride normalized biomechanical
        # angles
        for idx in _patientStridesFileMap.keys():
            gaitParPath = Path(_patientStridesFileMap[idx][_side]['gaitParameters'])

            patGPDict = defaultdict(float)

            f = open(gaitParPath, mode='r')
            lines = [line.replace("\n", "") for line in f if not "%" in line]

            # Initializing the patEventsDict dictionary
            for line in lines:
                linesplits = line.split("  ")
                patGPDict[linesplits[0]] = float(linesplits[1])

            patIdx_GP[idx] = patGPDict

        return patIdx_GP


    def generate_featuresList(self, _bioMechDF):
        '''
        Returns two dictionaries, one dictionary mapping features pertaining to the affected side
        to its 'new name' of the patient and the other, features pertaining to the unaffected side

        Update 07.04.2022 -- Features in the middle (e.g. throrax, pelvis) will be considered twice,
        according to the left and right side
        '''
        affFeatures = defaultdict(str); unaffFeatures = defaultdict(str)

        for col in _bioMechDF.columns:
            if "Right" in col:
                if self.affside == "r":
                    newCol = col.replace("Right", "Aff")
                    affFeatures[col] = newCol
                else:
                    newCol = col.replace("Right", "UnAff")
                    unaffFeatures[col] = newCol

            elif "Left" in col:
                if self.affside == "r":
                    newCol = col.replace("Left", "UnAff")
                    unaffFeatures[col] = newCol
                else:
                    newCol = col.replace("Left", "Aff")
                    affFeatures[col] = newCol

            # Update 13.04.2022 -- All features in the middle will now be considered but parsed
            # in terms of "affected" and "unaffected"
            else:
                if '_' in col:
                    aff_newCol = f"{col.split('_')[0]}Aff_{col.split('_')[1]}"
                    affFeatures[col] = aff_newCol

                    unaff_newCol = f"{col.split('_')[0]}UnAff_{col.split('_')[1]}"
                    unaffFeatures[col] = unaff_newCol

                elif 'upperBodyTilt' in col:
                    aff_newCol = f"{col.split('.')[0]}Aff.{col.split('.')[1]}"
                    affFeatures[col] = aff_newCol

                    unaff_newCol = f"{col.split('.')[0]}UnAff.{col.split('.')[1]}"
                    unaffFeatures[col] = unaff_newCol

        # Update 13.04.2022 -- Add %time into affFeatures
        affFeatures['%time'] = '%time'

        return affFeatures, unaffFeatures


    def process_featureLabels(self, _dfAff, _dfUnAff):
        '''
        The main task of this method is to rename the feature labels according to the patient's
        affected side
        '''
        processed_df = pd.DataFrame()

        # Update 05.04.2022 -- Dealing with patients extracted data that might not contain
        # angles contained in the reference bands

        excludedAff_Features = []; excludedUnAff_Features = []
        for k, v in self.affNormFeatures.items():
            if k in _dfAff.columns:
                processed_df[v] = _dfAff[k]
            else:
                print(f"{k} was excluded from patient's kinematic data")
                excludedAff_Features.append(k)

        for k, v in self.unaffNormFeatures.items():
            if k in _dfUnAff.columns:
                processed_df[v] = _dfUnAff[k]
            else:
                print(f"{k} was excluded from patient's kinematic data")
                excludedUnAff_Features.append(k)

        # Update dictionaries
        if len(excludedAff_Features) > 0:
            for featToPop in excludedAff_Features:
                self.affNormFeatures.pop(featToPop)

        if len(excludedUnAff_Features) > 0:
            for featToPop in excludedUnAff_Features:
                self.unaffNormFeatures.pop(featToPop)

        return processed_df


    def process_featureLabels_patientDoubleStrides(self, _map):
        '''
        This is a wrapper method to loop through the given patientstridesFileMap dictionary and
        process the feature labels, namely renaming them accordingly
        '''
        # Initializing dictionary to hold the processed kinematical biomechanical angles
        processedBioMechCollection = defaultdict()

        for idx, patient in _map.items():
            dfAff   = pd.read_table(patient["aff"]["kinematics"], sep=' ')
            dfUnAff = pd.read_table(patient["unaff"]["kinematics"], sep=' ')

            newdf = self.process_featureLabels(dfAff, dfUnAff)

            processedBioMechCollection[idx] = newdf

        return processedBioMechCollection
