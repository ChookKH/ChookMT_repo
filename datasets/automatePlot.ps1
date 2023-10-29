# === === === ===
# Liaw dataset
# === === === ===
# SKlearn tree based regressors
python .\plotDT.py .\SK_models\SK_Datasets_Liaw_TR\TR_Trunk_borda.pickle TrunkLiaw && `
python .\plotDT.py .\SK_models\SK_Datasets_Liaw_TR\TR_Leg_borda.pickle LegLiaw && `
python .\plotDT.py .\SK_models\SK_Datasets_Liaw_TR\TR_Arm_borda.pickle ArmLiaw && `
python .\plotDT.py .\SK_models\SK_Datasets_Liaw_TR\TR_Speed_borda.pickle SpeedLiaw && `
python .\plotDT.py .\SK_models\SK_Datasets_Liaw_TR\TR_Fluency_borda.pickle FluencyLiaw && `
python .\plotDT.py .\SK_models\SK_Datasets_Liaw_TR\TR_Stability_borda.pickle StabilityLiaw && `


# === === === ===
# Chook dataset
# === === === ===
# SKlearn tree based regressors
python .\plotDT.py .\SK_models\SK_Datasets_SD_TR\TR_Trunk_borda.pickle TrunkSD && `
python .\plotDT.py .\SK_models\SK_Datasets_SD_TR\TR_Leg_borda.pickle LegSD && `
python .\plotDT.py .\SK_models\SK_Datasets_SD_TR\TR_Arm_borda.pickle ArmSD && `
python .\plotDT.py .\SK_models\SK_Datasets_SD_TR\TR_Speed_borda.pickle SpeedSD && `
python .\plotDT.py .\SK_models\SK_Datasets_SD_TR\TR_Fluency_borda.pickle FluencySD && `
python .\plotDT.py .\SK_models\SK_Datasets_SD_TR\TR_Stability_borda.pickle StabilitySD