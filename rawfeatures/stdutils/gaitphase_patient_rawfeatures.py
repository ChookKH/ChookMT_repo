import os, sys
import io
import csv
import shutil
import numpy as np
import pandas as pd
from scipy import integrate
from collections import defaultdict
from ckhutils.h_data import healthy_data


def check_user_phaseStartEnd(_usrarg):
    '''
    Function to check if the user entered valid values for the phase start and end
    '''
    usrargOk = False
    gaitPars = [
        "initialContact", "endOfLoadingResponse", "endOfMidstance", "endOfTerminalStance",
        "endOfPreswing", "endOfInitialSwing", "endOfMidswing", "endOfTerminalSwing"
    ]
    # Ensure that user enters a valid gait parameter
    gaitPars_err_msg = ("\n  ").join(gaitPars)
    err_msg = f"Please enter a valid gait parameter:\n  {gaitPars_err_msg}"


    if isinstance(_usrarg, str):
        if not _usrarg in gaitPars:
            raise ValueError(err_msg)
        else:
            usrargOk = True

    elif (isinstance(_usrarg, float)) or (isinstance(_usrarg, int)):
        if (_usrarg < 0) or (_usrarg > 1):
            raise ValueError("Please enter a values between 0 - 1 for _usrarg")
        else:
            usrargOk = True

    else:
        raise ValueError("Invalid argument for _usrarg")

    return usrargOk


def get_gaitphaseTime_Patient(_usrarg, _gpDict):
    '''
    Function to get the normalized time for a given gait event (patient)
    '''
    argOk = check_user_phaseStartEnd(_usrarg)

    if argOk:
        if isinstance(_usrarg, str):
            time = _gpDict[_usrarg]

        elif (isinstance(_usrarg, float)) or (isinstance(_usrarg, int)):
            time = _usrarg

    return time


def get_gaitphaseTime_RB(_usrarg, _side, _gpDF):
    '''
    Function to get the normalized time for a given gait event (reference band)
    '''
    argOk = check_user_phaseStartEnd(_usrarg)

    if argOk:
        time = _gpDF.at[_usrarg, _side]

    return time


def extract_gaitphase_rawfeatures(
        idx, _pat_rb_obj, _stridePairID,
        _phaseStart="initialContact", _phaseEnd=None
):
    '''
    Accepts a "patient_refband_grouping" object and parses the object's properties according
    to user desired input arguments and initializes the "gaitphase_patient_rawfeatures" object
    '''
    # Extracting the exact time instance for the given gait event

    # Phase start
    # -----------
    # Patient
    phaseStart_aff_patient = get_gaitphaseTime_Patient(_phaseStart, _pat_rb_obj.patGPDict_aff[idx])
    phaseStart_unaff_patient = get_gaitphaseTime_Patient(_phaseStart, _pat_rb_obj.patGPDict_unaff[idx])

    # Reference bands
    phaseStart_aff_rb = get_gaitphaseTime_RB(_phaseStart, 'AffNorm', _pat_rb_obj.rbGEvents)
    phaseStart_unaff_rb = get_gaitphaseTime_RB(_phaseStart, 'UnAffNorm', _pat_rb_obj.rbGEvents)

    # If user desires a phase
    # Phase end
    # ---------
    if not _phaseEnd is None:
        # Patient
        phaseEnd_aff_patient = get_gaitphaseTime_Patient(_phaseEnd, _pat_rb_obj.patGPDict_aff[idx])
        phaseEnd_unaff_patient  = get_gaitphaseTime_Patient(_phaseEnd, _pat_rb_obj.patGPDict_unaff[idx])

        # Reference bands
        phaseEnd_aff_rb = get_gaitphaseTime_RB(_phaseEnd, 'AffNorm', _pat_rb_obj.rbGEvents)
        phaseEnd_unaff_rb = get_gaitphaseTime_RB(_phaseEnd, 'UnAffNorm', _pat_rb_obj.rbGEvents)

        # Initializing the "gaitphase_rawfeatures" object
        gpObj = gaitphase_rawfeatures(
            _stridePairID, _pat_rb_obj.affside,
            phaseStart_aff_patient, phaseEnd_aff_patient,
            phaseStart_unaff_patient, phaseEnd_unaff_patient,
            phaseStart_aff_rb, phaseEnd_aff_rb,
            phaseStart_unaff_rb, phaseEnd_unaff_rb,
            _pat_rb_obj.affNormFeatures, _pat_rb_obj.unaffNormFeatures,
            _pat_rb_obj.rbMean_corr, _pat_rb_obj.rbLower_corr, _pat_rb_obj.rbUpper_corr,
            _pat_rb_obj.patCollection_corr[idx]
        )

    # If user only desires an event : Initial Contact
    else:
        # Initializing the "gaitevent_rawfeatures" object at only one gait event,
        # hence only extracting stats at that discrete point
        gpObj = gaitevent_rawfeatures(
            _stridePairID, _pat_rb_obj.affside,
            phaseStart_aff_patient, phaseStart_unaff_patient,
            phaseStart_aff_rb, phaseStart_unaff_rb,
            _pat_rb_obj.affNormFeatures, _pat_rb_obj.unaffNormFeatures,
            _pat_rb_obj.rbMean_corr, _pat_rb_obj.rbLower_corr, _pat_rb_obj.rbUpper_corr,
            _pat_rb_obj.patCollection_corr[idx]
        )

    return gpObj

# Initialize for healthy kinematics data
healthyData = healthy_data()

# === === === ===
# Raw features extracted from a gait phase
class gaitphase_rawfeatures:
    '''
    Class that contains dataframe pertaining to the gait phase, bounded between the temporal
    event input
    '''
    def __init__(
            self, _stridePairID, _affSide,
            _tGaitLowerAff_Patient, _tGaitUpperAff_Patient,
            _tGaitLowerUnAff_Patient, _tGaitUpperUnAff_Patient,
            _tGaitLowerAff_RB, _tGaitUpperAff_RB,
            _tGaitLowerUnAff_RB, _tGaitUpperUnAff_RB,
            _affNormFeaturesDict, _unaffNormFeaturesDict,
            _RB_MeanDF, _RB_LowerDF, _RB_UpperDF, _patDS
    ):
        # Basic patient trial's ID
        self.StridePairID = _stridePairID

        # Short preprocessing step to set '%time' as the dataframes' index
        _RB_MeanDF  = self.set_timeindex(_RB_MeanDF)
        _RB_LowerDF = self.set_timeindex(_RB_LowerDF)
        _RB_UpperDF = self.set_timeindex(_RB_UpperDF)
        _patDS      = self.set_timeindex(_patDS)

        # First casting all the time (%) into float
        _tGaitLowerAff_Patient = float(_tGaitLowerAff_Patient)
        _tGaitUpperAff_Patient = float(_tGaitUpperAff_Patient)
        _tGaitLowerUnAff_Patient = float(_tGaitLowerUnAff_Patient)
        _tGaitUpperUnAff_Patient = float(_tGaitUpperUnAff_Patient)

        _tGaitLowerAff_RB = float(_tGaitLowerAff_RB)
        _tGaitUpperAff_RB = float(_tGaitUpperAff_RB)
        _tGaitLowerUnAff_RB = float(_tGaitLowerUnAff_RB)
        _tGaitUpperUnAff_RB = float(_tGaitUpperUnAff_RB)

        # First remove '%time' in _affNormFeaturesDict
        if '%time' in _affNormFeaturesDict:
            _affNormFeaturesDict.pop('%time')


        # # === === === ===
        # # Partitioning the reference bands and patient's curves accordingly
        # phaseRBMean_Aff, phaseRBMean_UnAff = self.extract_phaseDF(
        #     _RB_MeanDF,
        #     _tGaitLowerAff_RB, _tGaitLowerUnAff_RB,
        #     _tGaitUpperAff_RB, _tGaitUpperUnAff_RB,
        #     _affNormFeaturesDict, _unaffNormFeaturesDict
        # )
        # phaseRBUpper_Aff, phaseRBUpper_UnAff = self.extract_phaseDF(
        #     _RB_UpperDF,
        #     _tGaitLowerAff_RB, _tGaitLowerUnAff_RB,
        #     _tGaitUpperAff_RB, _tGaitUpperUnAff_RB,
        #     _affNormFeaturesDict, _unaffNormFeaturesDict
        # )
        # phaseRBLower_Aff, phaseRBLower_UnAff = self.extract_phaseDF(
        #     _RB_LowerDF,
        #     _tGaitLowerAff_RB, _tGaitLowerUnAff_RB,
        #     _tGaitUpperAff_RB, _tGaitUpperUnAff_RB,
        #     _affNormFeaturesDict, _unaffNormFeaturesDict
        # )
        phasePatDS_Aff, phasePatDS_UnAff = self.extract_phaseDF(
            _patDS,
            _tGaitLowerAff_Patient, _tGaitLowerUnAff_Patient,
            _tGaitUpperAff_Patient, _tGaitUpperUnAff_Patient,
            _affNormFeaturesDict, _unaffNormFeaturesDict
        )


        # === === === ===
        # Update 01.12.2021
        # -----------------
        # 1. The gait phases for both the reference bands and the patient will be normalized [0 - 100] %
        # 2. Stats of patient curve and of the stats difference between patient and RB in the phase
        #    will be considered (fundamentally different from what was done during Liaw's master thesis)
        # 3. Deviation areas and integrals will not be considered anymore (shown to be weak features from
        #    Liaw's master thesis)

        # Patient stats
        # -------------
        self.StatsDF = self.extract_patient_stats(phasePatDS_Aff, phasePatDS_UnAff)
        self.StatsDF = self.StatsDF.drop(labels=['kneeJointUnAff_varus/adduction.q', 
                                         'kneeJointAff_varus/adduction.q', 
                                         'kneeJointUnAff_varus/adduction.qd', 
                                         'kneeJointAff_varus/adduction.qd'])
        self.StatsDF = self.StatsDF.rename_axis('Stats')

        # Seperate the UnAff side
        self.UnAffDF = self.StatsDF[self.StatsDF.index.str.contains('UnAff')]
        
        # Seperate the Aff side
        StatsDFLength = len(self.StatsDF) // 2
        self.AffDF = self.StatsDF[:StatsDFLength]
        
        # Patient and reference bands deviation stats
        # -------------------------------------------
        # The stats of the reference bands are defined as the following:
        # Min : Minimum of the lower confidence interval boundary
        # Median : Median of mean line in the confidence interval
        # Max : Maximum of the upper confidence interval boundary
        # self.RBStatsDF = self.extract_rb_stats(
        #     phaseRBLower_Aff, phaseRBMean_Aff, phaseRBUpper_Aff,
        #     phaseRBLower_UnAff, phaseRBMean_UnAff, phaseRBUpper_UnAff
        # )
        
        # print(self.RBStatsDF)

        # === === === ===
        # Update 18.03.2023 (Chook)
        # -----------------
        # Added a boolean conversion for dataframe comparison between StatsDF and RBStatsDF
        # self.BoolStatsDF = self.StatsDF.le(self.RBStatsDF).astype(float)
        # print(self.BoolStatsDF)
        

        # === === === ===
        # Patient gait phase metadata
        self.Metadata = self.initialize_gaitphaseMetadata(
            _tGaitLowerAff_Patient, _tGaitUpperAff_Patient,
            _tGaitLowerUnAff_Patient, _tGaitUpperUnAff_Patient,
            _tGaitLowerAff_RB, _tGaitUpperAff_RB,
            _tGaitLowerUnAff_RB, _tGaitUpperUnAff_RB
        )


        # === === === ===
        # Update 05.04.2023 (Chook)
        # -----------------
        # Obtaining averaged gait phase metadata of healthy test-subjects
        self.LowerSD, self.UpperSD, self.LowerCI, self.UpperCI = self.initialize_hMetadata()


    # === === === ===
    # Update 27.04.2023 (Chook)
    # -----------------
    # Changed comparison from less than to within refband (within=0, else 1)
    def within_RB_check(self, pat_df, rb_df):
        '''
        Method to check whether the patient stats lie within refband stats
        '''
        output_df = pd.DataFrame()

        output_df['Min'] = ((pat_df['Min'] >= rb_df['Min']) &
                            (pat_df['Min'] <= rb_df['Max']))
        output_df['Median'] = ((pat_df['Median'] >= rb_df['Min']) & 
                            (pat_df['Median'] <= rb_df['Max']))
        output_df['Max'] = ((pat_df['Max'] >= rb_df['Min']) &
                            (pat_df['Max'] <= rb_df['Max']))
        
        output_df = ~output_df
        output_df = output_df.astype(int)

        # min_comparison = pat_df['Min'] > rb_df['Min']
        # median_comparison = (pat_df['Median'] >= rb_df['Min']) & (pat_df['Median'] <= rb_df['Max'])
        # max_comparison = pat_df['Max'] < rb_df['Max']

        # output_df = pd.DataFrame({'Min': min_comparison.astype(int),
        #                'Median': median_comparison.astype(int),
        #                'Max': max_comparison.astype(int)},
        #               index=rb_df.index)

        return output_df 


    def initialize_hMetadata(self):
        '''
        (Implemented by Chook)
        Extract healthy gait stats
        '''
        
        lowerEventsSD = healthyData.gait_eve[['Measure', 'Lower-S.D']].set_index('Measure')
        upperEventsSD = healthyData.gait_eve[['Measure', 'Upper-S.D']].set_index('Measure')
        lowerEventsCI = healthyData.gait_eve[['Measure', 'Lower-CI']].set_index('Measure')
        upperEventsCI = healthyData.gait_eve[['Measure', 'Upper-CI']].set_index('Measure')

        lowerPhaseSD = healthyData.gait_pha[['Measure', 'Lower-S.D']].set_index('Measure')
        upperPhaseSD = healthyData.gait_pha[['Measure', 'Upper-S.D']].set_index('Measure')
        lowerPhaseCI = healthyData.gait_pha[['Measure', 'Lower-CI']].set_index('Measure')
        upperPhaseCI = healthyData.gait_pha[['Measure', 'Upper-CI']].set_index('Measure')

        mergedLowerSD = pd.concat([lowerEventsSD, lowerPhaseSD], axis=0)/100
        mergedUpperSD = pd.concat([upperEventsSD, upperPhaseSD], axis=0)/100
        mergedLowerCI = pd.concat([lowerEventsCI, lowerPhaseCI], axis=0)/100
        mergedUpperCI = pd.concat([upperEventsCI, upperPhaseCI], axis=0)/100

        mergedLowerSD.loc['initialContact'] = 0
        mergedUpperSD.loc['initialContact'] = 0
        mergedLowerCI.loc['initialContact'] = 0
        mergedUpperCI.loc['initialContact'] = 0
        
        mergedLowerSD.loc['SwingWidth'] = 1 - mergedUpperSD.at['endOfPreswing', 'Upper-S.D']
        mergedUpperSD.loc['SwingWidth'] = 1 - mergedLowerSD.at['endOfPreswing', 'Lower-S.D']
        mergedLowerCI.loc['SwingWidth'] = 1 - mergedUpperCI.at['endOfPreswing', 'Upper-CI']
        mergedUpperCI.loc['SwingWidth'] = 1 - mergedLowerCI.at['endOfPreswing', 'Lower-CI']

        mergedLowerSD = mergedLowerSD.rename(columns={'Lower-S.D': ''})
        mergedUpperSD = mergedUpperSD.rename(columns={'Upper-S.D': ''})
        mergedLowerCI = mergedLowerSD.rename(columns={'Lower-CI': ''})
        mergedUpperCI = mergedUpperSD.rename(columns={'Upper-CI': ''})
       
        return mergedLowerSD, mergedUpperSD, mergedLowerCI, mergedUpperCI


    def get_hUpperMetadata(self, _phaseStart, _phaseEnd):
        '''
        Function to classify healthy subject gait width and gait start percentage
        '''
        h_metadata = pd.Series({}, dtype=float)

        if sys.argv[3] == 'std':
            # Entire stride
            if _phaseStart == "initialContact" and _phaseEnd == "endOfTerminalSwing":
                gw="StrideWidth"

            # Stance phase
            if _phaseStart == 'initialContact' and _phaseEnd == 'endOfPreswing':
                gw="endOfPreswing"

            # Swing phase
            if _phaseStart == 'endOfPreswing' and _phaseEnd == 'endOfTerminalSwing':
                gw="SwingWidth"

                h_upper_metadata = pd.Series(
                    {
                        "GaitWidth_Aff": self.UpperSD.loc[gw].values[0],
                        "GaitStart_Aff": self.UpperSD.loc[_phaseStart].values[0],
                        "GaitWidth_UnAff": self.UpperSD.loc[gw].values[0],
                        "GaitStart_UnAff": self.UpperSD.loc[_phaseStart].values[0]
                    }
                )
    
        if sys.argv[3] == 'ci':
            # Entire stride
            if _phaseStart == "initialContact" and _phaseEnd == "endOfTerminalSwing":
                gw="StrideWidth"

            # Stance phase
            if _phaseStart == 'initialContact' and _phaseEnd == 'endOfPreswing':
                gw="endOfPreswing"

            # Swing phase
            if _phaseStart == 'endOfPreswing' and _phaseEnd == 'endOfTerminalSwing':
                gw="SwingWidth"

            h_upper_metadata = pd.Series(
                {
                    "GaitWidth_Aff": self.UpperCI.loc[gw].values[0],
                    "GaitStart_Aff": self.UpperCI.loc[_phaseStart].values[0],
                    "GaitWidth_UnAff": self.UpperCI.loc[gw].values[0],
                    "GaitStart_UnAff": self.UpperCI.loc[_phaseStart].values[0]
                }
            )

        return h_upper_metadata


    def get_hLowerMetadata(self, _phaseStart, _phaseEnd):
        '''
        Function to classify healthy subject gait width and gait start percentage
        '''
        h_metadata = pd.Series({}, dtype=float)

        if sys.argv[3] == 'std':
            # Entire stride
            if _phaseStart == "initialContact" and _phaseEnd == "endOfTerminalSwing":
                gw="StrideWidth"

            # Stance phase
            if _phaseStart == 'initialContact' and _phaseEnd == 'endOfPreswing':
                gw="endOfPreswing"

            # Swing phase
            if _phaseStart == 'endOfPreswing' and _phaseEnd == 'endOfTerminalSwing':
                gw="SwingWidth"

            h_lower_metadata = pd.Series(
                {
                    "GaitWidth_Aff": self.LowerSD.loc[gw].values[0],
                    "GaitStart_Aff": self.LowerSD.loc[_phaseStart].values[0],
                    "GaitWidth_UnAff": self.LowerSD.loc[gw].values[0],
                    "GaitStart_UnAff": self.LowerSD.loc[_phaseStart].values[0]
                }
            )
    
        if sys.argv[3] == 'ci':
            # Entire stride
            if _phaseStart == "initialContact" and _phaseEnd == "endOfTerminalSwing":
                gw="StrideWidth"

            # Stance phase
            if _phaseStart == 'initialContact' and _phaseEnd == 'endOfPreswing':
                gw="endOfPreswing"

            # Swing phase
            if _phaseStart == 'endOfPreswing' and _phaseEnd == 'endOfTerminalSwing':
                gw="SwingWidth"

            h_lower_metadata = pd.Series(
                {
                    "GaitWidth_Aff": self.LowerCI.loc[gw].values[0],
                    "GaitStart_Aff": self.LowerCI.loc[_phaseStart].values[0],
                    "GaitWidth_UnAff": self.LowerCI.loc[gw].values[0],
                    "GaitStart_UnAff": self.LowerCI.loc[_phaseStart].values[0]
                }
            )

        return h_lower_metadata
    

    def extract_patient_stats(self, _phasePatientAff, _phasePatientUnAff):
        '''
        Extracts the stats of the patient's values within the gait phase (min, median, max)
        '''
        _phasePatient_Min    = pd.concat([_phasePatientAff.min(), _phasePatientUnAff.min()])
        _phasePatient_Median = pd.concat([_phasePatientAff.median(), _phasePatientUnAff.median()])
        _phasePatient_Max    = pd.concat([_phasePatientAff.max(), _phasePatientUnAff.max()])

        statsDF = pd.DataFrame([_phasePatient_Min, _phasePatient_Median, _phasePatient_Max]).T
        statsDF = statsDF.rename(columns={0: 'Min', 1: 'Median', 2: 'Max'})

        return statsDF


    def extract_rb_stats(
            self, _phaseRBLower_Aff, _phaseRBMean_Aff, _phaseRBUpper_Aff,
            _phaseRBLower_UnAff, _phaseRBMean_UnAff, _phaseRBUpper_UnAff
    ):
        '''
        Extracts the stats of the reference bands within the gait phase (min, median, max)
        '''
        _phaseRB_Min    = pd.concat([_phaseRBLower_Aff.min(), _phaseRBLower_UnAff.min()])
        _phaseRB_Median = pd.concat([_phaseRBMean_Aff.median(), _phaseRBMean_UnAff.median()])
        _phaseRB_Max    = pd.concat([_phaseRBUpper_Aff.max(), _phaseRBUpper_UnAff.max()])

        statsDF = pd.DataFrame([_phaseRB_Min, _phaseRB_Median, _phaseRB_Max]).T
        statsDF = statsDF.rename(columns={0: 'Min', 1: 'Median', 2: 'Max'})

        return statsDF


    def set_timeindex(self, _df):
        '''
        Set '%time' as the dataframe's index
        '''
        # First modifying _df such that '%time' is the index
        _df = _df.set_index('%time')

        return _df


    def calculate_boundary(self, _tGait, _df, _features, _boundary):
        '''
        Given a particular time, interpolate and return the corresponding value if needed

        Return: i (_tGait-1 or _tGait), j (_tGait+1), (row at _tGait)
        '''
        tArray = _df.index

        # First extract the features according to the list given
        if isinstance(_features, dict):
            dfMod = _df[_features.values()].copy()
        if isinstance(_features, list):
            dfMod = _df[_features].copy()

        # First check if _tGait is already available in _df
        if _tGait in tArray:
            if _boundary == "lower":

                # Update
                # ------
                # We could be dealing with cases where the lower boundary of the gait
                # phase is also at 100 %

                # If that is the case, the values will simply be returned

                if (tArray.get_loc(_tGait)) < len(tArray) - 1:
                    i = _tGait
                    j = tArray[tArray.get_loc(_tGait) + 1]
                    val = dfMod.loc[_tGait]
                else:
                    i = _tGait; j = _tGait; val = dfMod.loc[_tGait]
            elif _boundary == "upper":
                i = tArray[tArray.get_loc(_tGait) - 1]
                j = _tGait
                val = dfMod.loc[_tGait]
            else:
                raise ValueError("Invalid argument value for _boundary")
        else:
            p1 = 0
            p2 = len(_df) - 1

            for i in range(int(len(_df)/2) + 1):
                m = int((p1+p2) / 2)
                if tArray[m] < _tGait:
                    p1 = m + 1
                elif tArray[m] > _tGait:
                    p2 = m - 1

                if p1 > p2:
                    break

            if _boundary == "lower":
                i = _tGait
                j = tArray[p1]
                h = tArray[p2]
                val = self.interpolate(i, h, j, dfMod.loc[h], dfMod.loc[j])

            elif _boundary == "upper":
                j = _tGait
                i = tArray[p2]
                k = tArray[p1]
                val = self.interpolate(j, i, k, dfMod.loc[i], dfMod.loc[k])
            else:
                raise ValueError("Invalid argument value for _boundary")

        return i, j, val


    def interpolate(self, x, x1, x2, y1, y2):
        '''
        Sub-method to interpolte
        '''
        dy = y2 - y1
        dx = x2 - x1
        y  = dy / dx * (x - x1) + y1

        return y


    def check_phaseDFSensibility(self, _tgL, _tgU):
        '''
        Check if phase to be extracted is sensible

        Deprecated on 16.09.2021
        '''
        tgL = _tgL / 100; tgU = _tgU / 100

        dataSensible = True
        if (tgL > 1) or (tgU > 1):
            dataSensible = False

        return dataSensible


    def extract_phaseDF(
            self, _df, _tgLAff, _tgLUnAff, _tgUAff, _tgUUnAff, _affFDict, _unaffFDict
    ):
        '''
        Extracts the dataframe of the biomechanical values of a phase, as defined by the input
        normalized time boundaries.

        Remember to consider for the affected and unaffected sides
        '''
        df_aff    = self.partitionDF(_df, _tgLAff, _tgUAff, _affFDict)
        df_unaff  = self.partitionDF(_df, _tgLUnAff, _tgUUnAff, _unaffFDict)

        return df_aff, df_unaff


    def partitionDF(self, _df, _tGaitLower, _tGaitUpper, _features):
        '''
        Partitions the dataframe according to the given lower and upper normalized time
        instance boundaries.

        Remember to consider the affected and unaffected normalized strides separately.
        '''
        # Normalized time instances for gait parameters are given in %
        _tLower = _tGaitLower / 100; _tUpper = _tGaitUpper / 100

        # Dealing with the phase's lower time boundary
        l1, l2, row1 = self.calculate_boundary(_tLower, _df, _features, "lower")

        # Dealing with the phase's upper time boundary
        u1, u2, row2 = self.calculate_boundary(_tUpper, _df, _features, "upper")

        if isinstance(_features, dict):
            phaseSubDF = _df[_features.values()].copy()
        elif isinstance(_features, list):
            phaseSubDF = _df[_features].copy()

        phaseSubDF = phaseSubDF.loc[l2:u1]

        phaseDF = (row1.to_frame()).transpose()
        phaseDF = phaseDF.set_index([pd.Index([l1])])
        phaseDF = pd.concat([phaseDF, phaseSubDF])

        row2 = (row2.to_frame().transpose()).set_index([pd.Index([u2])])
        phaseDF = pd.concat([phaseDF, row2])

        return phaseDF


    def initialize_gaitphaseMetadata(
            self, _tgLAffPat, _tgUAffPat, _tgLUnAffPat, _tgUUnAffPat,
            _tgLAffRB, _tgUAffRB, _tgLUnAffRB, _tgUUnAffRB

    ):
        '''
        Initializing series of patient's metadata
        '''
        metadata = pd.Series(
            {
                "GaitWidth_Aff": (_tgUAffPat - _tgLAffPat) / 100,
                "GaitStart_Aff": _tgLAffPat / 100,
                "GaitWidth_UnAff": (_tgUUnAffPat - _tgLUnAffPat) / 100,
                "GaitStart_UnAff": _tgLUnAffPat / 100,
                # "GaitWidthDiff_Aff": ((_tgUAffPat - _tgLAffPat) - (_tgUAffRB - _tgLAffRB)) / 100,
                # "GaitWidthDiff_UnAff": ((_tgUUnAffPat - _tgLUnAffPat) - (_tgUUnAffRB - _tgLUnAffRB)) / 100
            }
        )

        return metadata


    def pairIdx_toStr(self, n):
        '''Function to convert pair index. Sub-function used when automatizing file names'''
        if n < 10:
            nStr = f"0{n}"
        elif (n >= 10) and (n < 100):
            nStr = f"{n}"

        return nStr


# === === === ===
# Raw features extracted from a single gait event
class gaitevent_rawfeatures:
    def __init__(
            self, _stridePairID, _affSide,
            _tGaitAff_Patient, _tGaitUnAff_Patient,
            _tGaitAff_RB, _tGaitUnAff_RB,
            _affNormFeaturesDict, _unaffNormFeaturesDict,
            _RB_MeanDF, _RB_LowerDF, _RB_UpperDF, _patDS
    ):
        # Basic patient trial's ID
        self.StridePairID = _stridePairID

        # Short preprocessing step to set '%time' as the dataframes' index
        _RB_MeanDF  = self.set_timeindex(_RB_MeanDF)
        _RB_LowerDF = self.set_timeindex(_RB_LowerDF)
        _RB_UpperDF = self.set_timeindex(_RB_UpperDF)
        _patDS      = self.set_timeindex(_patDS)

        # First casting all the time (%) into float
        _tGaitAff_Patient   = float(_tGaitAff_Patient)
        _tGaitUnAff_Patient = float(_tGaitUnAff_Patient)
        _tGaitAff_RB        = float(_tGaitAff_RB)
        _tGaitUnAff_RB      = float(_tGaitUnAff_RB)

        # First remove '%time' from _affNormFeaturesDict
        if '%time' in _affNormFeaturesDict:
            _affNormFeaturesDict.pop('%time')


        # The DataFrames of the kinematical joints according to the different gait phases are
        # different for both data normalized on the affected and unaffected side due to the
        # different gait events
        # === === === ===
        # Selecting the corresponding temporal kinematical values normalized to the affected side
        # at the selected gait event, time (%)
        eventRBUpper = self.extract_series(
            _RB_UpperDF, _tGaitAff_RB, _tGaitUnAff_RB, _affNormFeaturesDict, _unaffNormFeaturesDict
        )
        eventRBMean = self.extract_series(
            _RB_MeanDF, _tGaitAff_RB, _tGaitUnAff_RB, _affNormFeaturesDict, _unaffNormFeaturesDict
        )
        eventRBLower = self.extract_series(
            _RB_LowerDF, _tGaitAff_RB, _tGaitUnAff_RB, _affNormFeaturesDict, _unaffNormFeaturesDict
        )

        # Extracting patient values for each biomechanical angle for the given time instance
        self.Values = self.extract_series(
            _patDS, _tGaitAff_Patient, _tGaitUnAff_Patient, _affNormFeaturesDict, _unaffNormFeaturesDict
        )


        # === === === ===
        # Computing the difference between patient values and reference band for each
        # biomechanical angle
        self.DeviationValues = self.compute_patient_deviations(
            self.Values, eventRBUpper, eventRBLower
        )


        # === === === ===
        # Patient gait event metadata
        self.Metadata = self.initialize_gaiteventMetadata(_tGaitAff_Patient, _tGaitUnAff_Patient)


    def extract_series(self, df, _tgAff, _tgUnAff, _affFDict, _unaffFDict):
        '''
        Extracts a series of biomechanical values at the given gait event or time (%)

        Allows for combining features from two different normalized strides.
        '''
        series_aff    = self.select_discEventSeries(df, _tgAff, _affFDict)
        series_unaff  = self.select_discEventSeries(df, _tgUnAff, _unaffFDict)

        combined_series = pd.concat([series_aff, series_unaff])

        return combined_series


    def select_discEventSeries(self, _df, _tGait, _features):
        '''
        Returns the row of body kinematical values at the given gait time. If not present, values
        will be intrapolated
        '''
        if isinstance(_features, dict):
            _df_featuresList = _df[_features.values()].copy()
        elif isinstance(_features, list):
            _df_featuresList = _df[_features].copy()

        if _tGait in _df_featuresList.index:
            rowVal = _df_featuresList.loc[_tGait]
        else:
            rowVal = self.interpolateGaitPhase(_tGait, _df_featuresList)

        return rowVal


    def compute_patient_deviations(self, _patVals, _RBUpper, _RBLower):
        '''
        Calculates the discrete differences between the patient and reference band (only at one
        single discrete gait event).

        Values that lie within the reference band will be considered to have a difference of zero.

        Values that lie above the reference band will have a positive difference.

        Values that lie below the reference band will have a negative difference.
        '''
        # Calculating the discrete differences between the patient and reference bands, also
        # categorizing them according to a positive or negative deviation
        # === === === ===
        diff_series = pd.Series(index=_patVals.index, dtype=float)

        for angle in _patVals.index:
            pat = _patVals[angle]; upper = _RBUpper[angle]; lower = _RBLower[angle]

            if pat > upper:
                diff_series[angle] = pat - upper
            elif pat < lower:
                diff_series[angle] = pat - lower
            elif (pat >= lower) and (pat <= upper):
                diff_series[angle] = 0

        return diff_series


    def set_timeindex(self, _df):
        '''
        Set '%time' as the dataframe's index
        '''
        # First modifying _df such that '%time' is the index
        _df = _df.set_index('%time')

        return _df


    def interpolateGaitPhase(self, _tGait, _df):
        '''
        Given a particular time, interpolate and return the corresponding value
        '''
        tArray = _df.index

        p1 = 0
        p2 = len(_df) - 1

        for i in range(int(len(_df)/2) + 1):
            m = int((p1+p2) / 2)
            if tArray[m] < _tGait:
                p1 = m + 1
            elif tArray[m] > _tGait:
                p2 = m - 1

            if p1 > p2:
                break

        # Interpolate and return the upper and lower time index boundary and interpolated values
        dy = _df.loc[tArray[p1]] - _df.loc[tArray[p2]]
        dx = tArray[p1] - tArray[p2]
        val = dy/dx * (_tGait - tArray[p2]) + _df.loc[tArray[p2]]

        return val


    def initialize_gaiteventMetadata(self, _tgAff, _tgUnAff):
        '''
        Initializing series of patient's metadata
        '''
        metadata = pd.Series(
            {
                "GaitStart_Aff": _tgAff / 100,
                "GaitStart_UnAff": _tgUnAff / 100
            }
        )

        return metadata


    def pairIdx_toStr(self, n):
        '''Function to convert pair index. Sub-function used when automatizing file names'''
        if n < 10:
            nStr = f"0{n}"
        elif (n >= 10) and (n < 100):
            nStr = f"{n}"

        return nStr
