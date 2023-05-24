import time
import pickle
import shutil
import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict

from stdutils.patient import Patient, Trial
from stdutils import patient_refband_grouping
from stdutils import extract_gaitphase_rawfeatures
from stdutils import load_patients_trials as loader
from stdutils import map_patients_trials
from stdutils.gaitphase_patient_rawfeatures import gaitphase_rawfeatures
from process_gaitparameters import extract_gaitparameters

from ckhutils.h_data import healthy_data

if len(sys.argv) < 4:
    print(
        "\nPossible usage:\npython3 experiment.py " +
        "<dirOfRefBandData> <dirOfPatientTrials> <errorBandParameters>"
    )
    sys.exit(1)
else:
    rb_dir = Path(sys.argv[1]).resolve()
    metadata_dir = Path(sys.argv[2])
    errorband = sys.argv[3] # 'ci' or 'std, but just use 'ci' for this thesis


# === === === ===
# Grab the folder name of the reference band and test subject data
refBand = rb_dir.name; patientsgroup = metadata_dir.name


# === === === ===
# Initializing dictionary, mapping patients and their respective trials
# Key   : Patient ID
# Value : [<List of Valid/Clean Trial Objects>]
patients, trials = loader(metadata_dir)

print(f"Number of patients: {len(patients)}")
print(f"Number of trials  : {len(trials)}")

unsensiblePairs = []; noCommonPairs_trials = []

patient_trials_dict = map_patients_trials(patients, trials)


# === === === ===
# Extracting features
for patientID, trialObjects in patient_trials_dict.items():
    # print(f"=========================\nDealing with {patientID}\n---")

    for t in trialObjects:
        # print(f" - {t.TrialID} ... ")

        # Grouping the patient's trial data and reference band together
        patRB_group = patient_refband_grouping(
            rb_dir, t, errorband, _testSubjectsSide=None
        )

        # If only running for 1 subject (t = t)
        # patRB_group = patient_refband_grouping(
            # rb_dir, t, errorband, _testSubjectsSide=None
        # )

# Essentially ::
# The gait cycle of the patient with respect to the affected (lateral) and
# unaffected (contralateral) sides are being organized, together with the 
# reference bands. Think of it as some kind of ORGANIZER


        # === === === ===
        # Update 02.05.2023
        # -----------------
        # Create a instance of gaitphase_rawfeatures
        hData = healthy_data()
        
        if not patRB_group.noCommonPairs:
        # If there is at least one common stride pair

            for idx, pair in patRB_group.patientstridesFileMap.items():
                # 'idx' simply refers to a stride pair
                # - Pair 0
                # - Pair 1
                # - Pair 2 and so on ...
                # 'pair' is a dictionary the has the following keys:
                # - 'aff': {
                #    'kinematics':<pathOfExportedBiomechanicalAngles_affSide>,
                #    'gaitParameters':<pathOfGaitParameters_affSide>
                # }
                # - 'unaff' : {(correspondingly for unaffected side)}
                phaseFeaturesSensibility = []

                strideID_Aff   = pair['aff']['kinematics'].name
                strideID_UnAff = pair['unaff']['kinematics'].name

                ID_Aff = strideID_Aff.split('_')[-2]
                ID_UnAff = strideID_UnAff.split('_')[-2]

                stridePairID = ('_').join(strideID_Aff.split('_')[0:-2])
                stridePairID = stridePairID + f"_A{ID_Aff}_" + f"U{ID_UnAff}"
                # print(f"    > Stride pair : {stridePairID}")


                # === === === ===
                # General patient stride data
                strideGeneralData = pd.Series(
                    {
                        "StridePairID": stridePairID,
                        "Auxiliary": t.WalkTool
                    }
                ); gpSeries = pd.Series(strideGeneralData)


                # === === === ===
                # Patient stride gait parameters data
                gpSeriesAff = extract_gaitparameters(
                    patRB_group.patGPDict_aff[idx], t.AffectedSide, 
                    _side="Aff", stance_swing=False
                )
                gpSeriesUnAff = extract_gaitparameters(
                    patRB_group.patGPDict_unaff[idx], t.AffectedSide, 
                    _side="UnAff", stance_swing=False
                )

                gpSeries = pd.concat([gpSeries, gpSeriesAff])
                gpSeries = pd.concat([gpSeries, gpSeriesUnAff])

                # Remove 'Aff' for series comparison
                new_index = gpSeriesAff.index.str.replace('Aff', '')
                gpSeriesAff = pd.Series(gpSeriesAff.values, index=new_index)
                # print(gpSeriesAff)


                # Gait parameter series (within refband check, within = 0, else = 1) 
                def check_within_limits(gpSeriesAff, lowerLimits, upperLimits):

                    withinCheck = (gpSeriesAff >= lowerLimits) & (gpSeriesAff <= upperLimits)
                    withinCheck = pd.Series(np.where(withinCheck, 0, 1), index=withinCheck.index, name='Result')
                    
                    return withinCheck

                if sys.argv[3] == 'std':
                    # S.D check
                    lowerParameterSD = hData.gait_par[['Measure', 'Lower-S.D']].set_index('Measure')
                    upperParameterSD = hData.gait_par[['Measure', 'Upper-S.D']].set_index('Measure')
                    withinSDCheck = check_within_limits(gpSeriesAff, lowerParameterSD['Lower-S.D'], upperParameterSD['Upper-S.D'])
                    # print(withinSDCheck)

                if sys.argv[3] == 'ci':
                    # CI check
                    lowerParameterCI = hData.gait_par[['Measure', 'Lower-CI']].set_index('Measure')
                    upperParameterCI = hData.gait_par[['Measure', 'Upper-CI']].set_index('Measure')
                    withinCICheck = check_within_limits(gpSeriesAff, lowerParameterCI['Lower-CI'], upperParameterCI['Upper-CI'])
                    # print(withinCICheck)

                
                # Extracting the features, per pair of patient's stride data
                # === === === ===
                # Entire stride
                # print('Entire stride:')
                stride = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfTerminalSwing"
                )
                
                # Stride healthy kinematic data
                stride_h_kine = hData.intialize_hKinematics('Stride.dat')

                ### To ignore warning
                pd.options.mode.chained_assignment = None
                
                # To retain the original indexing of UnAff and Aff
                stride.UnAffDF = pd.concat(
                    [
                        stride.UnAffDF, 
                        pd.DataFrame(
                            data=list(stride.UnAffDF.index),
                            columns=["OriIndex"], index=stride.UnAffDF.index
                        )
                    ], axis=1
                )
                stride.AffDF = pd.concat(
                    [
                        stride.AffDF, 
                        pd.DataFrame(
                            data=list(stride.AffDF.index), 
                            columns=["OriIndex"], index=stride.AffDF.index
                        )
                    ], axis=1
                )

                # Check UnAff side of subject to healthy kinematic data within RefBand(within = 0, eles = 1)
                stride.UnAffDF.index = stride.UnAffDF.index.str.replace('UnAff', '')
                stride_UnAff_RB_check = stride.within_RB_check(stride.UnAffDF, stride_h_kine)
                stride_UnAff_RB_check.index = stride.UnAffDF.loc[:,'OriIndex'] 

                # Check Aff side of subject to healthy kinematic data within RefBand(within = 0, eles = 1)
                stride.AffDF.index = stride.AffDF.index.str.replace('Aff', '')
                stride_Aff_RB_check = stride.within_RB_check(stride.AffDF, stride_h_kine)
                stride_Aff_RB_check.index = stride.AffDF.loc[:,'OriIndex']

                # Upper and lower boundary of healthy metadata
                stride_upper = stride.get_hUpperMetadata("initialContact", "endOfTerminalSwing")
                stride_lower = stride.get_hLowerMetadata("initialContact", "endOfTerminalSwing")
                p_stride = stride.Metadata

                stride_is_in = ((p_stride >= stride_lower) & (p_stride <= stride_upper))
                stride_is_in = (~stride_is_in).astype(int)

                # Unravel into one column
                stride_Aff_RB_check = hData.unravel(stride_Aff_RB_check)
                stride_UnAff_RB_check = hData.unravel(stride_UnAff_RB_check)

                # Merge df  
                strideMerged = pd.concat([stride_is_in, stride_Aff_RB_check, stride_UnAff_RB_check], axis=0)
                strideMerged.columns = ['Series', 'Status']
                strideMerged = strideMerged.stack().reset_index(level=1, drop=True)
                # print(strideMerged)

                hData.export_data(stridePairID, 'Stride.dat', strideMerged)

                # sys.exit()
                # Stance phase
                # print('Stance phase:')
                stance = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfPreswing"
                )

                # Stance healthy kinematic data
                stance_h_kine = hData.intialize_hKinematics('Stance.dat')

                # To retain the original indexing of UnAff and Aff
                stance.UnAffDF['OriIndex'] = stance.UnAffDF.index
                stance.AffDF['OriIndex'] = stance.AffDF.index                

                # Check UnAff side of subject to healthy kinematic data within RefBand(within = 0, eles = 1)
                stance.UnAffDF.index = stance.UnAffDF.index.str.replace('UnAff', '')
                stance_UnAff_RB_check = stance.within_RB_check(stance.UnAffDF, stance_h_kine)
                stance_UnAff_RB_check.index = stance.UnAffDF['OriIndex']

                # Check Aff side of subject to healthy kinematic data within RefBand(within = 0, eles = 1)
                stance.AffDF.index = stance.AffDF.index.str.replace('Aff', '')
                stance_Aff_RB_check = stance.within_RB_check(stance.AffDF, stance_h_kine)
                stance_Aff_RB_check.index = stance.AffDF['OriIndex']
                
                # Upper and lower boundary of healthy metadata
                stance_upper = stance.get_hUpperMetadata("initialContact", "endOfPreswing")
                stance_lower = stance.get_hLowerMetadata("initialContact", "endOfPreswing")
                p_stance = stance.Metadata
                
                stance_is_in = ((p_stance >= stance_lower) & (p_stance <= stance_upper))
                stance_is_in = (~stance_is_in).astype(int)

                # Unravel into one column
                stance_Aff_RB_check = hData.unravel(stance_Aff_RB_check)
                stance_UnAff_RB_check = hData.unravel(stance_UnAff_RB_check)                
                
                # Merge df  
                stanceMerged = pd.concat([stance_is_in, stance_Aff_RB_check, stance_UnAff_RB_check], axis=0)
                stanceMerged.columns = ['Series', 'Status']
                stanceMerged = stanceMerged.stack().reset_index(level=1, drop=True)
                # print(stanceMerged)

                hData.export_data(stridePairID, 'Stance.dat', stanceMerged)

                # sys.exit()                
                # Swing phase
                # print('Swing phase:')
                swing = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfTerminalSwing"
                )

                # Swing healthy kinematic data
                swing_h_kine = hData.intialize_hKinematics('Swing.dat')

                # To retain the original indexing of UnAff and Aff
                swing.UnAffDF['OriIndex'] = swing.UnAffDF.index
                swing.AffDF['OriIndex'] = swing.AffDF.index

                # Check UnAff side of subject to healthy kinematic data within RefBand(within = 0, eles = 1)
                swing.UnAffDF.index = swing.UnAffDF.index.str.replace('UnAff', '')
                swing_UnAff_RB_check = swing.within_RB_check(swing.UnAffDF, swing_h_kine)
                swing_UnAff_RB_check.index = swing.UnAffDF['OriIndex']

                # Check Aff side of subject to healthy kinematic data within RefBand(within = 0, eles = 1)
                swing.AffDF.index = swing.AffDF.index.str.replace('Aff', '')
                swing_Aff_RB_check = swing.within_RB_check(swing.AffDF, swing_h_kine)
                swing_Aff_RB_check.index = swing.AffDF['OriIndex']
                
                swing_upper = swing.get_hUpperMetadata("endOfPreswing", "endOfTerminalSwing")
                swing_lower = swing.get_hLowerMetadata("endOfPreswing", "endOfTerminalSwing")
                p_swing = swing.Metadata
                
                swing_is_in = ((p_swing >= swing_lower) & (p_swing <= swing_upper))
                swing_is_in = (~swing_is_in).astype(int)

                # Unravel into one column
                swing_Aff_RB_check = hData.unravel(swing_Aff_RB_check)
                swing_UnAff_RB_check = hData.unravel(swing_UnAff_RB_check)

                # Merge df  
                swingMerged = pd.concat([swing_is_in, swing_Aff_RB_check, swing_UnAff_RB_check], axis=0)
                swingMerged.columns = ['Series', 'Status']
                swingMerged = swingMerged.stack().reset_index(level=1, drop=True)
                # print(swingMerged)
                
                hData.export_data(stridePairID, 'Swing.dat', swingMerged)
                # sys.exit()
                               

# If the trial has no common pair at all due to all data being faulty
else:
    print("Warning: This trial data has no valid stride pairs")

sys.exit(0)  