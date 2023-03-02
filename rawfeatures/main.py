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
from process_gaitparameters import extract_gaitparameters

if len(sys.argv) < 4:
    print(
        "\nPossible usage:\npython3 main.py " +
        "<dirOfRefBandData> <dirOfPatientTrials> <errorBandParameters>"
    )
    sys.exit(1)
else:
    rb_dir = Path(sys.argv[1]).resolve()
    patientsinfo_dir = Path(sys.argv[2])
    errorband = sys.argv[3]


# === === === ===
# Grab the folder name of the reference band and test subject data
refBand = rb_dir.name; patientsgroup = patientsinfo_dir.name


# === === === ===
# Initializing dictionary, mapping patients and their respective trials
# Key   : Patient ID
# Value : [<Patient Object>, <List of Valid/Clean Trial Objects>]
subjects, trials = loader(patientsinfo_dir)

unsensiblePairs = []; noCommonPairs_trials = []

patient_trials_dict = map_patients_trials(subjects[0:3], trials)


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

        # === === === ===
        # If the group has at least one common pair
        # ---
        # Note: Checks have been implemented to ensure that every valid patient stride meets the following
        # condition
        # 1. Appropriate left and right stride pairs
        # 1.1 Left and right stride pairs with the same index
        # 1.2 Left and right stride pairs with different indices, but sequential (1-2, 4-5, etc..)
        # 2. For each left and right stride, there should be a corresponding valid gait parameters file
        # 2.1 In each trial object, any faulty or problematic file is simply ignored
        # 2.2 That is handled by the script process_rawdata/filer_data.py
        if not patRB_group.noCommonPairs:
            for idx, pair in patRB_group.patientstridesFileMap.items():
                phaseFeaturesSensibility = []

                strideID_Aff   = pair['aff']['kinematics'].name
                strideID_UnAff = pair['unaff']['kinematics'].name
                ID_Aff = strideID_Aff.split('_')[-2]; ID_UnAff = strideID_UnAff.split('_')[-2]

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
                    patRB_group.patGPDict_aff[idx], t.AffectedSide, _side="Aff",
                    stance_swing=False
                )
                gpSeriesUnAff = extract_gaitparameters(
                    patRB_group.patGPDict_unaff[idx], t.AffectedSide, _side="UnAff",
                    stance_swing=False
                )

                gpSeries = pd.concat([gpSeries, gpSeriesAff])
                gpSeries = pd.concat([gpSeries, gpSeriesUnAff])

                # Extracting the features, per pair of patient's stride data
                # === === === ===
                # Entire stride
                pat_Stride = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfTerminalSwing"
                )
                # Stance phase
                pat_stancePhase = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfPreswing"
                )
                # Swing phase
                pat_swingPhase = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfTerminalSwing"
                )

                # === === === ===
                # Perry phases
                # Initial contact
                pat_InCnt = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd=None
                )

                # Load response
                pat_LdRsp = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfLoadingResponse"
                )

                # Mid stance
                pat_MdStn = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfLoadingResponse", _phaseEnd="endOfMidstance"
                )

                # Terminal stance
                pat_TrStn = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfMidstance", _phaseEnd="endOfTerminalStance"
                )

                # Pre swing
                pat_PrSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfTerminalStance", _phaseEnd="endOfPreswing"
                )

                # Initial Swing
                pat_InSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfInitialSwing"
                )

                # Mid swing
                pat_MdSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfInitialSwing", _phaseEnd="endOfMidswing"
                )

                # Terminal swing
                pat_TrSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfMidswing", _phaseEnd="endOfTerminalSwing"
                )

        # If the trial has no common pair at all due to all data being faulty
        else:
            noCommonPairs_trials.append(t.TrialID)


# === === === ===
# Saving txt file with list of trials that have no valid pair of strides (if necessary)
if len(noCommonPairs_trials) > 0:
    f = open(
        (patients_RB_subfolder.parent).joinpath("Trials_NoValidStridePairs.txt"), 'w'
    )
    for t in noCommonPairs_trials:
        f.write(f"{t}\n")
    f.close()
else:
    print("Every trial has at least one valid pair of stride data ... ")

sys.exit(0)
