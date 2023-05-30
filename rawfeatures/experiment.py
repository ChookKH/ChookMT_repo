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


                # Gait parameter series (within refband check, within = 0, else = 1)
                def check_within_limits(gpSeriesAff, lowerLimits, upperLimits):
                    '''
                    Compare Aff subject gait parameter series with healthy subjects
                    '''
                    withinCheck = pd.Series(
                        np.where(
                            (gpSeriesAff >= lowerLimits) & (gpSeriesAff <= upperLimits), 
                            0, 1
                        ),index=gpSeriesAff.index, name='Result'
                    )
                    
                    return withinCheck

                if sys.argv[3] == 'std':
                    # S.D check
                    parameterSD = hData.gait_par.set_index('Measure')
                    withinSDCheck = check_within_limits(
                        gpSeriesAff, parameterSD['Lower-S.D'], parameterSD['Upper-S.D']
                        )

                if sys.argv[3] == 'ci':
                    # CI check
                    parameterCI = hData.gait_par.set_index('Measure')
                    withinCICheck = check_within_limits(
                        gpSeriesAff, parameterCI['Lower-CI'], parameterCI['Upper-CI']
                        )


                def process_phase(phaseStart, phaseEnd, filename):
                    '''
                    Process the phases to print out 1 or 0 and export .dat file 
                    '''
                    phase_data = extract_gaitphase_rawfeatures(
                        idx, patRB_group, stridePairID, 
                        _phaseStart=phaseStart, _phaseEnd=phaseEnd
                    )

                    # Initialize the kinematic data for healthy subject
                    phase_h_kine = hData.intialize_hKinematics(filename)

                    # Create a column OriIndex to retain original index
                    phase_data.UnAffDF = pd.concat(
                        [
                            phase_data.UnAffDF, 
                                pd.DataFrame(
                                    data=list(phase_data.UnAffDF.index), 
                                    columns=['OriIndex'], 
                                    index=phase_data.UnAffDF.index
                                )
                        ], axis=1
                    )

                    phase_data.AffDF = pd.concat(
                        [
                            phase_data.AffDF, 
                            pd.DataFrame(
                                data=list(phase_data.AffDF.index), 
                                columns=['OriIndex'], 
                                index=phase_data.AffDF.index
                            )
                        ], axis=1
                    )

                    # Unaffected side of subject do within refband check (within=0, else=1) 
                    phase_data.UnAffDF.index = phase_data.UnAffDF.index.str.replace('UnAff', '')
                    phase_UnAff_RB_check = phase_data.within_RB_check(
                        phase_data.UnAffDF, phase_h_kine
                    )
                    phase_UnAff_RB_check.index = phase_data.UnAffDF.loc[:, 'OriIndex']

                    # Affected side of subject do within refband check (within=0, else=1)
                    phase_data.AffDF.index = phase_data.AffDF.index.str.replace('Aff', '')
                    phase_Aff_RB_check = phase_data.within_RB_check(
                        phase_data.AffDF, phase_h_kine
                    )
                    phase_Aff_RB_check.index = phase_data.AffDF.loc[:, 'OriIndex']

                    # Get healthy subject upper and lower boundary metadata
                    phase_upper = phase_data.get_hUpperMetadata(phaseStart, phaseEnd)
                    phase_lower = phase_data.get_hLowerMetadata(phaseStart, phaseEnd)
                    pat_phase = phase_data.Metadata

                    # Patient metadat of subject do is_in refband check (within=0, else=1)
                    phase_is_in = ((pat_phase >= phase_lower) & (pat_phase <= phase_upper))
                    phase_is_in = (~phase_is_in).astype(int)

                    # Unravel m x 3 data into m x 1 dataframe
                    phase_Aff_RB_check = hData.unravel(phase_Aff_RB_check)
                    phase_UnAff_RB_check = hData.unravel(phase_UnAff_RB_check)

                    phase_merged = pd.concat(
                        [
                            phase_is_in, 
                            phase_Aff_RB_check, 
                            phase_UnAff_RB_check
                        ], axis=0
                    ).stack().reset_index(level=1, drop=True)

                    hData.export_data(stridePairID, filename, phase_merged)

                # Extracting the features, per pair of patient's stride data
                # === === === ===
                # Entire stride
                stride_phase = process_phase("initialContact", "endOfTerminalSwing", "Stride.dat")

                # Stance phase
                stance_phase = process_phase("initialContact", "endOfPreswing", "Stance.dat")

                # Swing phase
                swing_phase = process_phase("endOfPreswing", "endOfTerminalSwing", "Swing.dat")
                               

# If the trial has no common pair at all due to all data being faulty
else:
    print("Warning: This trial data has no valid stride pairs")

sys.exit(0)  