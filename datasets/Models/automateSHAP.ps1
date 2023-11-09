# === === === ===
# SVM SD Dataset
# === === === ===
# Subscore 0
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Arm_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Arm.csv Arm 0 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Fluency_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Fluency.csv Fluency 0 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Leg_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Leg.csv Leg 0 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Speed_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Speed.csv Speed 0 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Stability_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Stability.csv Stability 0 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Trunk_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Trunk.csv Trunk 0 && `

# Subscore 1
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Arm_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Arm.csv Arm 1 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Fluency_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Fluency.csv Fluency 1 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Leg_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Leg.csv Leg 1 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Speed_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Speed.csv Speed 1 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Stability_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Stability.csv Stability 1 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Trunk_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Trunk.csv Trunk 1 && `

# Subscore 2
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Arm_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Arm.csv Arm 2 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Fluency_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Fluency.csv Fluency 2 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Leg_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Leg.csv Leg 2 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Speed_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Speed.csv Speed 2 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Stability_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Stability.csv Stability 2 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Trunk_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Trunk.csv Trunk 2 && `

# Subscore 3
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Arm_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Arm.csv Arm 3 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Fluency_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Fluency.csv Fluency 3 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Leg_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Leg.csv Leg 3 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Speed_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Speed.csv Speed 3 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Stability_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Stability.csv Stability 3 && `
python .\shapSVM.py .\Datasets_SD_SVM\SVM_Trunk_borda.pickle ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Trunk.csv Trunk 3

# === === === ===
# MLP
# === === === ===
# SD Dataset
# python .\shapSVM.py ..\..\forMLP\post_processSD\Arm_MLP.pkl ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Arm.csv Arm && `
# python .\shapSVM.py ..\..\forMLP\post_processSD\Fluency_MLP.pkl ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Fluency.csv Fluency && `
# python .\shapSVM.py ..\..\forMLP\post_processSD\Leg_MLP.pkl ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Leg.csv Leg && `
# python .\shapSVM.py ..\..\forMLP\post_processSD\Speed_MLP.pkl ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Speed.csv Speed && `
# python .\shapSVM.py ..\..\forMLP\post_processSD\Stability_MLP.pkl ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Stability.csv Stability && `
# python .\shapSVM.py ..\..\forMLP\post_processSD\Trunk_MLP.pkl ..\Datasets_SD\TrainDataset_SD.dat ..\ytrain.csv ..\feature_list\borda_std_Trunk.csv Trunk