import pickle
import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict

from stdutils.patient import Patient, Trial
from stdutils import patient_refband_grouping
from stdutils import load_patients_trials as loader
from stdutils import map_patients_trials
from stdutils.gaitphase_patient_rawfeatures import gaitphase_rawfeatures
from processes import extract_gaitparameters, check_gpWithinNorm, process_phaseData

from ckhutils import healthy_data

# === === === ===
# Main
if len(sys.argv) < 4:
    print(
        "Possible usage:python3 main.py <dirOfRefBandData> <dirOfPatientTrials> <saveFolder_exportedData>"
    )
    sys.exit(1)
else:
    rb_dir = Path(sys.argv[1]).resolve()
    metadata_dir = Path(sys.argv[2])
    saveFolder_exportedData = Path(sys.argv[3])


# === === === ===
# Grab the folder name of the reference band and test subject data
refBand = rb_dir.name; patientsgroup = metadata_dir.name

# Importing class of healthy data
hData = healthy_data(rb_dir)


# === === === ===
# Initializing dictionary, mapping patients and their respective trials
# Key   : Patient ID
# Value : [<List of Valid/Clean Trial Objects>]
patients, trials = loader(metadata_dir)

# print(f"Number of patients: {len(patients)}")
# print(f"Number of trials  : {len(trials)}")

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
            rb_dir, t, "std", _testSubjectsSide=None
        )

        # === === === ===
        # Update 02.05.2023
        # -----------------
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

                gpSeries = pd.concat([gpSeries, gpSeriesAff, gpSeriesUnAff])

                # ckh:: Inspecting if patient's gait parameters lie within the norm
                gpSeries = check_gpWithinNorm(gpSeries, gpSeriesAff, gpSeriesUnAff, hData)

                # Export series
                stridePairID_subfolder = saveFolder_exportedData.joinpath(stridePairID)
                os.makedirs(stridePairID_subfolder)
                gpSeries.to_csv(
                    stridePairID_subfolder.joinpath("GtPar_RawFeatures.dat"), sep=' ',
                    index=True, header=False
                )

                # Extracting the features, per pair of patient's stride data
                # === === === ===
                # Entire stride
                stride_phase = process_phaseData(
                    idx, patRB_group, hData, stridePairID,
                    "initialContact", "endOfTerminalSwing"
                )
                # Entire stance
                stance_phase = process_phaseData(
                    idx, patRB_group, hData, stridePairID,
                    "initialContact", "endOfPreswing"
                )
                # Entire swing
                swing_phase = process_phaseData(
                    idx, patRB_group, hData, stridePairID,
                    "endOfPreswing", "endOfTerminalSwing"
                )

                # Save phase data
                stride_phase.to_csv(stridePairID_subfolder.joinpath("Stride.dat"), sep=' ', index=True)
                stance_phase.to_csv(stridePairID_subfolder.joinpath("Stance.dat"), sep=' ', index=True)
                swing_phase.to_csv(stridePairID_subfolder.joinpath("Swing.dat"), sep=' ', index=True)

                sys.exit()

# If the trial has no common pair at all due to all data being faulty
else:
    print("Warning: This trial data has no valid stride pairs") 
