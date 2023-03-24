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

# :: would print unknowns
# print(patients)

# :: check for data type
# print(type(patients))

# :: ERR print list
# for patient in patients:
#     print(patient[0])

# for trials in trials:
#     print(trials)

# :: print only first patient trials
# for i in range(len(patients)):
#     if i == 0:
#         print(patients[i])

# print(f"Number of patients: {len(patients)}") # 100 patients
# print(f"Number of trials  : {len(trials)}")   # 546 trials

# # unsensiblePairs = []; noCommonPairs_trials = []

patient_trials_dict = map_patients_trials(patients, trials)
# print(patient_trials_dict)
# print(type(patient_trials_dict))

# :: ERR too many values to unpack
# for key, value in patient_trials_dict:
#     print(key, value)

# for key, value in patient_trials_dict.items():
#     print(key, value)

# print(patient_trials_dict.keys())

# :: ERR stdutils.patients.Trial object at ....
# print(patient_trials_dict.values())

# # Taking the patient ES011 for example
ES011 = patient_trials_dict["ES011"]

# print("\n\nLooping through elements in patient_trials_dict[ES011]")


# # === === === ===
# # Extracting features
# for trial in ES011:
#     print(f" - {trial.TrialID} ... ")

# # Taking the first trial, for learning purposes
ES011_T1 = ES011[0]
# print(ES011_T1)

# print("\n\nTaking a look at one trial")
# # Grouping the patient's trial data and reference band together
# # - Specifically::
patRB_group = patient_refband_grouping(
    rb_dir, ES011_T1, errorband, _testSubjectsSide=None
)
# # Essentially ::
# # The gait cycle of the patient with respect to the affected (lateral) and
# # unaffected (contralateral) sides are being organized, together with the
# # reference bands. Think of it as some kind of ORGANIZER


if not patRB_group.noCommonPairs: # :: ERR why .noCommonPairs is bool in patient_refband_grouping?
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

        # print(strideID_Aff)
        # print(strideID_UnAff)

        ID_Aff = strideID_Aff.split('_')[-2]        # ['ES011-B-3Gang02', '01', 'affRight.dat']
        ID_UnAff = strideID_UnAff.split('_')[-2]

        # print(ID_Aff)                               # 01
        # print(ID_UnAff)

        stridePairID = ('_').join(strideID_Aff.split('_')[0:-2])
        stridePairID = stridePairID + f"_A{ID_Aff}_" + f"U{ID_UnAff}"
        print(f"    > Stride pair : {stridePairID}")


        # === === === ===
        # General patient stride data
        strideGeneralData = pd.Series(
            {
                "StridePairID": stridePairID,
                "Auxiliary": ES011_T1.WalkTool
            }
        ); gpSeries = pd.Series(strideGeneralData)

        # print(strideGeneralData)
        # print(gpSeries)

        # === === === ===
        # Patient stride gait parameters data
        gpSeriesAff = extract_gaitparameters(
            patRB_group.patGPDict_aff[idx], ES011_T1.AffectedSide,
            _side="Aff", stance_swing=False
        )
        gpSeriesUnAff = extract_gaitparameters(
            patRB_group.patGPDict_unaff[idx], ES011_T1.AffectedSide,
            _side="UnAff", stance_swing=False
        )

        gpSeries = pd.concat([gpSeries, gpSeriesAff])
        gpSeries = pd.concat([gpSeries, gpSeriesUnAff])

        print(gpSeriesAff)
        #print(gpSeries[::-1])

        # Extracting the features, per pair of patient's stride data
        # === === === ===
        # Entire stride
        # stride = extract_gaitphase_rawfeatures(
        #     idx, patRB_group, stridePairID,
        #     _phaseStart="initialContact", _phaseEnd="endOfTerminalSwing"
        # )
        # Stance phase
        stance = extract_gaitphase_rawfeatures(
            idx, patRB_group, stridePairID,
            _phaseStart="initialContact", _phaseEnd="endOfPreswing"
        )

# If the trial has no common pair at all due to all data being faulty
else:
    print("Warning: This trial data has no valid stride pairs")

sys.exit(0)






# -----------TO BE CONTINUED-----------#
        # # Swing phase
        # pat_swingPhase = extract_gaitphase_rawfeatures(
        #     idx, patRB_group, stridePairID,
        #     _phaseStart="endOfPreswing", _phaseEnd="endOfTerminalSwing"
        # )

        # === === === ===
        # Perry phases
        # Initial contact
        # pat_InCnt = extract_gaitphase_rawfeatures(
        #     idx, patRB_group, stridePairID,
        #     _phaseStart="initialContact", _phaseEnd=None
        # )

        #         # Load response
        #         pat_LdRsp = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="initialContact", _phaseEnd="endOfLoadingResponse"
        #         )

        #         # Mid stance
        #         pat_MdStn = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="endOfLoadingResponse", _phaseEnd="endOfMidstance"
        #         )

        #         # Terminal stance
        #         pat_TrStn = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="endOfMidstance", _phaseEnd="endOfTerminalStance"
        #         )

        #         # Pre swing
        #         pat_PrSwg = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="endOfTerminalStance", _phaseEnd="endOfPreswing"
        #         )

        #         # Initial Swing
        #         pat_InSwg = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="endOfPreswing", _phaseEnd="endOfInitialSwing"
        #         )

        #         # Mid swing
        #         pat_MdSwg = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="endOfInitialSwing", _phaseEnd="endOfMidswing"
        #         )

        #         # Terminal swing
        #         pat_TrSwg = extract_gaitphase_rawfeatures(
        #             idx, patRB_group, stridePairID,
        #             _phaseStart="endOfMidswing", _phaseEnd="endOfTerminalSwing"
        #         )
