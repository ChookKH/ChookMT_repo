import pickle
import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict

import kFoldCV as kf

def create_subfolder(_supFolder, _listOfSubLevels):
    '''
    Function to automate checking if a given subfolder has been created
    and if not create it
    '''
    _saveFolder = _supFolder

    # Creating the path of the subdirectories
    for idx, sublevel in enumerate(_listOfSubLevels):
        _saveFolder = _saveFolder.joinpath(sublevel)

        if not os.path.exists(_saveFolder):
            os.mkdir(_saveFolder)

    return _saveFolder


def initializekFold(temp_df, k, seed, repTrialsPath, saveFolder, shuffle):
    '''
    Function to first initialize the k-Fold indices dictionary

    Parameters
    ----------
    temp_df : pd.DataFrame
    A DataFrame of the training dataset, mainly to just extract certain metadata

    k : int
    Number of folds

    seed : int
    Random seed number

    repTrialsPath : str or pathlib.Path
    Path of the file containing the table of representative trials

    saveFolder : str or pathlib.Path
    Folder to save the pickled dictionaries

    shuffle : bool
    Option to shuffle row indices
    '''
    featuresList  = temp_df.columns
    nTotalSamples = temp_df.shape[0]
    stridePairIDs = temp_df.index

    # Representative trials from each patient
    repTrialsDF = pd.read_csv(repTrialsPath, sep=' ', index_col='StridePairID', engine='c')

    # === === === ===
    # Identifying the representative trials in the df
    stridepair_idx_dict, repTrialsIdx = kf.identify_repTrials(stridePairIDs, repTrialsDF)


    # === === === === (Turned off for now, 15.03.2022)
    # Option 1 : Representative trials not used at all for the entire cross-validation process
    # Update 15.03.2022 -- Turned off
    # === === === ===
    # Option 2: Representative trials used during training but not during testing during
    # cross-validation via automatic assignment and reshuffling
    kFoldsDict_Train_Rep, kFoldsDict_Test_Rep = kf.generate_kFold(
        nTotalSamples, k, seed, repTrialsIdx, shuffle, _configuration='withRepresentativeTrials'
    )

    # === === === ===
    # Saving the relevant dictionaries and lists as pickled objects
    with open(saveFolder.joinpath(f"stridePairIdxDict.pkl"), 'wb') as handle:
        pickle.dump(stridepair_idx_dict, handle)
    with open(saveFolder.joinpath(f"repTrialsIdx.pkl"), 'wb') as handle:
        pickle.dump(repTrialsIdx, handle)

    with open(saveFolder.joinpath(f"kFoldsDict_Train_Rep.pkl"), 'wb') as handle:
        pickle.dump(kFoldsDict_Train_Rep, handle)
    with open(saveFolder.joinpath(f"kFoldsDict_Test_Rep.pkl"), 'wb') as handle:
        pickle.dump(kFoldsDict_Test_Rep, handle)

    return saveFolder


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "\nPossible usage: python3 initializekFold.py <trimmedDFsDict> <repTrialsDataset> " +
            "<k> <randomSeed> <saveFolderName> <shuffleOption>\n"
        )
        print(
            "Example usage: python3 initializekFold.py " +
            "~/Paper2022_SMS/<dataExportProj>/Machines/<patientGroup>/<refbandGroup>/Datasets/" +
            "<TrainDataset.dat> " +
            "~/Paper2022_SMS/<dataExportProj>/Machines/<patientGroup>/<refbandGroup>/Datasets/" +
            "RepTrials_n1_featSelection.dat 10 0 <saveFolderName> <shuffleOption>"
        )
        sys.exit(1)
    else:
        datasetPath = Path(sys.argv[1])
        repTrialsPath = Path(sys.argv[2])
        k = int(sys.argv[3])
        seed = int(sys.argv[4])
        saveFolderName = sys.argv[5]
        shuffleOption = sys.argv[6]

        if shuffleOption == 'y':
            shuffleOption = True
        elif shuffleOption == 'n':
            shuffleOption = False
        else:
            raise ValueError('Invalid input arugment for <shuffleOption> (y,n)')

    base_df = pd.read_table(datasetPath, sep=' ', index_col="StridePairID")

    # First creating the folder to contain the cross validation results
    crossValSaveFolder = create_subfolder(
        datasetPath.parent.parent,
        ['CrossValidation', saveFolderName]
    )

    initializekFold(base_df, k, seed, repTrialsPath, crossValSaveFolder, shuffleOption)

    sys.exit(0)
