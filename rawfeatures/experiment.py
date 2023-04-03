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

from ckhutils.bool import bool_output
from ckhutils.bool import h_subject_gait
from ckhutils.bool import series_compare

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
    print(f"=========================\nDealing with {patientID}\n---")

    for t in trialObjects:
        print(f" - {t.TrialID} ... ")

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
                print(f"    > Stride pair : {stridePairID}")


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

                print(gpSeriesAff)

                bool_output(gpSeriesAff)
                
                # gpSeriesAff.index = gpSeriesAff.index.str.split('Aff').str[0]
                # print(gpSeriesAff.index)

                # Extracting the features, per pair of patient's stride data
                # === === === ===
                # Entire stride
                print('Entire stride:')
                stride = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfTerminalSwing"
                )
                h_stride = h_subject_gait("initialContact", "endOfTerminalSwing")
                print(type(stride))
                print(type(h_stride))
                series_compare(h_stride, stride)
                time.sleep(1)

                # Stance phase
                print('Stance phase:')
                stance = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfPreswing"
                )
                h_stance = h_subject_gait("initialContact", "endOfPreSwing")

                # Swing phase
                print('Swing phase:')
                swing = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfTerminalSwing"
                )
                h_swing = h_subject_gait("endOfPreSwing", "endOfTerminalSwing")

                # === === === ===
                # Perry phases
                # Initial contact
                print('Initial contact:')
                InCnt = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd=None
                )

                # Load response
                print('Load response:')
                LdRsp = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfLoadingResponse"
                )
                h_LdRsp = h_subject_gait("initialContact", "endOfLoadingResponse")

                # Mid stance
                print('Mid stance:')
                MdStn = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfLoadingResponse", _phaseEnd="endOfMidstance"
                )
                h_MdStn = h_subject_gait("endOfLoadingResponse", "endOfMidStance")

                # Terminal stance
                print('Terminal stance:')
                TrStn = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfMidstance", _phaseEnd="endOfTerminalStance"
                )
                h_TrStn = h_subject_gait("endOfMidstance", "endOfTerminalStance")

                # Pre swing
                print('Pre swing:')
                PrSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfTerminalStance", _phaseEnd="endOfPreswing"
                )
                h_PrSwg = h_subject_gait("endOfTerminalStance", "endOfPreSwing")

                # Initial Swing
                print('Initial swing:')
                InSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfInitialSwing"
                )
                h_InSwg = h_subject_gait("endOfPreswing", "endOfInitialSwing")

                # Mid swing
                print('Mid swing:')
                MdSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfInitialSwing", _phaseEnd="endOfMidswing"
                )
                h_MdSwg = h_subject_gait("endOfInitialSwing", "endOfMidSwing")

                # Terminal swing
                print('Terminal swing:')
                TrSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfMidswing", _phaseEnd="endOfTerminalSwing"
                )
                h_TrSwg = h_subject_gait("endOfMidSwing", "endOfTerminalSwing")
                
                time.sleep(5)

# If the trial has no common pair at all due to all data being faulty
else:
    print("Warning: This trial data has no valid stride pairs")

sys.exit(0)  