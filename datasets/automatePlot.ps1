# === === === ===
# Liaw dataset
# === === === ===
# SKlearn tree based regressors
python .\plotDT.py .\Models\Datasets_Liaw_TR\TR_Trunk_borda.pickle TrunkLiaw && `
python .\plotDT.py .\Models\Datasets_Liaw_TR\TR_Leg_borda.pickle LegLiaw && `
python .\plotDT.py .\Models\Datasets_Liaw_TR\TR_Arm_borda.pickle ArmLiaw && `
python .\plotDT.py .\Models\Datasets_Liaw_TR\TR_Speed_borda.pickle SpeedLiaw && `
python .\plotDT.py .\Models\Datasets_Liaw_TR\TR_Fluency_borda.pickle FluencyLiaw && `
python .\plotDT.py .\Models\Datasets_Liaw_TR\TR_Stability_borda.pickle StabilityLiaw && `


# === === === ===
# Chook dataset
# === === === ===
# SKlearn tree based regressors
python .\plotDT.py .\Models\Datasets_SD_TR\TR_Trunk_borda.pickle TrunkTR && `
python .\plotDT.py .\Models\Datasets_SD_TR\TR_Leg_borda.pickle LegTR && `
python .\plotDT.py .\Models\Datasets_SD_TR\TR_Arm_borda.pickle ArmTR && `
python .\plotDT.py .\Models\Datasets_SD_TR\TR_Speed_borda.pickle SpeedTR && `
python .\plotDT.py .\Models\Datasets_SD_TR\TR_Fluency_borda.pickle FluencyTR && `
python .\plotDT.py .\Models\Datasets_SD_TR\TR_Stability_borda.pickle StabilityTR