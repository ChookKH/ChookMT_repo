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

                subject_gp = print(gpSeriesAff)

                bool_gp = bool_output(gpSeriesAff)
                
                
                # Extracting the features, per pair of patient's stride data
                # === === === ===
                # Entire stride
                print('Entire stride:')
                stride = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfTerminalSwing"
                )
                
                # Stance phase
                print('Stance phase:')
                stance = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="initialContact", _phaseEnd="endOfPreswing"
                )

                stance_hMetadata = stance.get_hMetadata("initialContact", "endOfPreswing")
                p_stance = stance.Metadata
                h_stance = stance_hMetadata
                stance_bool = series_compare(p_stance, h_stance)

                # Swing phase
                print('Swing phase:')
                swing = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfTerminalSwing"
                )

                swing_hMetadata = swing.get_hMetadata("endOfPreswing", "endOfTerminalSwing")
                p_swing = swing.Metadata
                h_swing = swing_hMetadata
                swing_bool = series_compare(p_swing, h_swing)

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

                LdRsp_hMetadata = LdRsp.get_hMetadata("initialContact", "endOfLoadingResponse")
                p_LdRsp = LdRsp.Metadata
                h_LdRsp = LdRsp_hMetadata
                LdRsp_bool = series_compare(p_LdRsp, h_LdRsp)

                # Mid stance
                print('Mid stance:')
                MdStn = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfLoadingResponse", _phaseEnd="endOfMidstance"
                )

                MdStn_hMetadata = MdStn.get_hMetadata("endOfLoadingResponse", "endOfMidstance")
                p_MdStn = MdStn.Metadata
                h_MdStn = MdStn_hMetadata
                MdStn_bool = series_compare(p_MdStn, h_MdStn)

                # Terminal stance
                print('Terminal stance:')
                TrStn = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfMidstance", _phaseEnd="endOfTerminalStance"
                )

                TrStn_hMetadata = swing.get_hMetadata("endOfMidstance", "endOfTerminalStance")
                p_TrStn = TrStn.Metadata
                h_TrStn = TrStn_hMetadata
                TrStn_bool = series_compare(p_TrStn, h_TrStn)

                # Pre swing
                print('Pre swing:')
                PrSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfTerminalStance", _phaseEnd="endOfPreswing"
                )

                PrSwg_hMetadata = swing.get_hMetadata("endOfTerminalStance", "endOfPreswing")
                p_PrSwg = PrSwg.Metadata
                h_PrSwg = PrSwg_hMetadata
                PrSwg_bool = series_compare(p_PrSwg, h_PrSwg)

                # Initial Swing
                print('Initial swing:')
                InSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfPreswing", _phaseEnd="endOfInitialSwing"
                )

                InSwg_hMetadata = InSwg.get_hMetadata("endOfPreswing", "endOfInitialSwing")
                p_InSwg = InSwg.Metadata
                h_InSwg = InSwg_hMetadata
                InSwg_bool = series_compare(p_InSwg, h_InSwg)

                # Mid swing
                print('Mid swing:')
                MdSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfInitialSwing", _phaseEnd="endOfMidswing"
                )

                MdSwg_hMetadata = MdSwg.get_hMetadata("endOfInitialSwing", "endOfMidswing")
                p_MdSwg = MdSwg.Metadata
                h_MdSwg = MdSwg_hMetadata
                MdSwg_bool = series_compare(p_MdSwg, h_MdSwg)

                # Terminal swing
                print('Terminal swing:')
                TrSwg = extract_gaitphase_rawfeatures(
                    idx, patRB_group, stridePairID,
                    _phaseStart="endOfMidswing", _phaseEnd="endOfTerminalSwing"
                )

                TrSwg_hMetadata = TrSwg.get_hMetadata("endOfMidswing", "endOfTerminalSwing")
                p_TrSwg = TrSwg.Metadata
                h_TrSwg = TrSwg_hMetadata
                TrSwg_bool = series_compare(p_TrSwg, h_TrSwg)
                
                time.sleep(5)

# If the trial has no common pair at all due to all data being faulty
else:
    print("Warning: This trial data has no valid stride pairs")

sys.exit(0)  