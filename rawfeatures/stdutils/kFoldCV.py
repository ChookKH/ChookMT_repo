import time
import os, sys
import numpy as np
import pandas as pd
from collections import defaultdict
from numpy.random import default_rng

cdir = os.path.dirname(os.path.realpath(__file__)); sys.path.append(cdir)
from sampleWeights import balance_classDistribution_patient
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import balanced_accuracy_score

def identify_repTrials(_stridePairIDs, _repTrialsDF):
    '''
    Identifies the representative strides used during feature selection in the dataframe.

    Parameters
    ----------
    _stridePairIDs : pandas.core.indexes.base.Index
    Pandas index object of initial dataset's indices

    _repTrialDF : pandas.DataFrame
    DataFrame of representative trials used during feature selection

    Returns
    -------
    stridePairIdx : dict
    Dictionary with integer as keys, mapped to stride pair ID

    repTrialsIdxs : list
    List of indices corresponding to stride pair IDs of representative strides used during feature selection
    '''
    # n number of representative trials from each patient
    repTrials = list(_repTrialsDF.index)

    # First assigning an index to every StridePairID
    stridePairIdx = defaultdict(int)
    for i, id in enumerate(_stridePairIDs):
        stridePairIdx[i] = id

    repTrialsIdx = []
    for idx, pair in stridePairIdx.items():
        if pair in repTrials:
            repTrialsIdx.append(idx)

    return stridePairIdx, repTrialsIdx


def generate_kFold(
        _n, _k, _seed, _repTrialsIdx, _shuffle, _configuration="noRepresentativeTrials"
):
    '''
    Shuffles the indices ranging from 0 to n-1, corresponding to each sample index and returns k fold.

    Parameters
    ----------
    _n : int
    Number of samples (stride data)

    _k : int
    Number of folds

    _seed : int
    Seed to initialize random number generator

    _repTrialsIdx : List
    List containing indices of represenative trials used for feature selection

    _shuffle : bool
    Option to shuffle the row indices, default is True

    _configuration : str
    Configuration of k-fold, either 'noRepresentativeTrials' or 'withRepresentativeTrials'

     - 'noRepresentativeTrials' will remove all representative trials indices from training and validation
     - 'withRepresentativeTrials' will ensure that all representative trials indices are removed from the
       validation set at each k-fold and instead distributed among the other k-1 folds

    Returns
    -------
    kFoldsDict_Train : dict
    Dictionary for k folds mapping each k to a numpy array of indices for stride pairs to be used for
    training

    kFoldsDict_Test : dict
    Dictionary for k folds mapping each k to a numpy array of indices for stride pairs to be used for
    testing
    '''
    # Initializing the dictionaries for training and testing stride pair indicers
    kFoldsDict_Train = defaultdict(np.array); kFoldsDict_Test = defaultdict(np.array)

    # Numpy's random number routines produce pseudo random numbers using combinations of a
    # BitGenerator to create sequences and a Generator to use those sequences to sample
    # from different statistical distributions

    # === === === ===
    # Generating the dictionary mapping each k-th fold to an array of indices pertaining to each stride pair
    # indices

    # Initializing the random number generator
    idxShuffle = np.arange(0, _n, 1)
    if _shuffle:
        rng = default_rng(_seed); rng.shuffle(idxShuffle)
    else:
        pass

    # Initializing the kFolds dictionary
    kFoldsDict = defaultdict(np.array)

    # Initializing the idx_assigned numpy array and assigning indices to the k folds
    idx_assigned = np.empty(0)

    for i in range(_k):
        start = i * int(len(idxShuffle) / _k)
        end = (i+1) * int(len(idxShuffle) / _k)

        kSplit = idxShuffle[start:end]; kFoldsDict[i] = kSplit

        idx_assigned = np.concatenate((idx_assigned, kSplit), axis=0)

    # Retrieving remainder
    idx_unassigned = np.setdiff1d(idxShuffle, idx_assigned)

    # Check for remainders and randomly appending them to one of the k folds
    folds_idx = np.arange(0, _k, 1)
    if _shuffle:
        rng.shuffle(folds_idx)
    else:
        pass

    if len(idxShuffle) % _k != 0:
        for i, idx in enumerate(idx_unassigned):
            kFoldsDict[folds_idx[i]] = np.append(kFoldsDict[folds_idx[i]], idx)


    # === === === ===
    # Modifying the kFolds indices dictionary according to the given configuration

    # === === === ===
    # All representative trials will be excluded from the training and validation process at every
    # k-th fold
    if _configuration == 'noRepresentativeTrials':

        # First remove the repTrials from all indices in all k folds
        for k_fold, idxs in kFoldsDict.items():
            idxsIntersect = np.intersect1d(idxs, _repTrialsIdx)

            for iToRemove in idxsIntersect:
                kFoldsDict[k_fold] = np.delete(
                    kFoldsDict[k_fold], np.where(kFoldsDict[k_fold] == iToRemove)
                )

        # Balance out the number of indices throughout the k folds
        idxsMerged = np.zeros(0)
        for k_fold, idxs in kFoldsDict.items():
            idxsMerged = np.concatenate((idxsMerged, idxs), axis=0)

        lengthOfEachFold = int(idxsMerged.shape[0] / len(kFoldsDict)); count = 0
        remainingIdxs = idxsMerged[(len(kFoldsDict) * lengthOfEachFold):len(idxsMerged)]

        for k in kFoldsDict.keys():
            i = count * lengthOfEachFold; j = (count + 1) * lengthOfEachFold

            kFoldsDict[k] = idxsMerged[i:j]
            if count < len(remainingIdxs):
                kFoldsDict[k] = np.append(kFoldsDict[k], remainingIdxs[count])

            count += 1

        # Separating the kFoldsDict into dictionaries containing indices for training and testing
        for k_fold in kFoldsDict.keys():

            # Merged idxs across the k-1 for training
            idxsMerged = np.empty(0)

            for kInner_fold, idxs in kFoldsDict.items():
                if k_fold == kInner_fold:
                    kFoldsDict_Test[k_fold] = idxs

                else:
                    idxsMerged = np.concatenate((idxsMerged, idxs))

            kFoldsDict_Train[k_fold] = idxsMerged


    # === === === ===
    # At each k-th fold, the representative trials will be removed from the validation set and equally
    # (as best as possible) distributed among the other k-1 training folds

    # Algorithm:
    # 1. For each fold, the k-th fold (test set) is scanned for stride pairs that are representative
    #    (used in feature selection)
    # 2. The "scanned out" stride pairs are then distributed among the other k-1 folds for training

    elif _configuration == 'withRepresentativeTrials':

        for k_fold, idxs in kFoldsDict.items():

            # Extract the representative stride pairs for the k-th fold
            idxToExclude = list(set(idxs) & set(_repTrialsIdx))

            trimmedIdxs = idxs.copy()
            for repIdx in idxToExclude:
                # Removing the representative stride pairs from the k-th fold
                trimmedIdxs = np.delete(trimmedIdxs, np.where(trimmedIdxs == repIdx))

            kFoldsDict_Test[k_fold] = trimmedIdxs

            # Adding the representative stride pairs into the rest of the k-1 folds for training
            kFoldsDict_Train[k_fold] = idxToExclude

            # Adding the other stride pairs from the k-1 folds
            for k_innerFolds in kFoldsDict.keys():
                if k_innerFolds != k_fold:
                    kFoldsDict_Train[k_fold] = np.append(kFoldsDict_Train[k_fold], kFoldsDict[k_innerFolds])

    else:
        raise ValueError("Please pass a valid configuration")


    # === === === ===
    # Convert the arrays in both dictionaries to int types
    for k_fold in kFoldsDict_Train.keys():
        kFoldsDict_Train[k_fold] = kFoldsDict_Train[k_fold].astype(int)
        kFoldsDict_Test[k_fold]  = kFoldsDict_Test[k_fold].astype(int)

    return kFoldsDict_Train, kFoldsDict_Test


def generate_kInnerFold(
        _idxList, _k, _seed, _repTrialsIdx, _shuffle, _configuration="noRepresentativeTrials"
):
    '''
    Shuffles the indices ranging from 0 to n-1, corresponding to each sample index and returns k fold.

    This function serves for the inner k fold.

    Parameters
    ----------
    _idxList : list
    Number of samples (stride data)

    _k : int
    Number of folds

    _seed : int
    Seed to initialize random number generator

    _repTrialsIdx : List
    List containing indices of represenative trials used for feature selection

    _configuration : str
    Configuration of k-fold, either 'noRepresentativeTrials' or 'withRepresentativeTrials'

     - 'noRepresentativeTrials' will remove all representative trials indices from training and validation
     - 'withRepresentativeTrials' will ensure that all representative trials indices are removed from the
       validation set at each k-fold and instead distributed among the other k-1 folds

    _shuffle : bool
    Option to shuffle the row indices, default is True

    Returns
    -------
    kFoldsDict_Train : dict
    Dictionary for k folds mapping each k to a numpy array of indices for stride pairs to be used for
    training

    kFoldsDict_Test : dict
    Dictionary for k folds mapping each k to a numpy array of indices for stride pairs to be used for
    testing
    '''
    # Initializing the dictionaries for training and testing stride pair indicers
    kFoldsDict_Train = defaultdict(np.array); kFoldsDict_Test = defaultdict(np.array)

    # === === === ===
    # Generating the dictionary mapping each k-th fold to an array of indices pertaining to each stride pair
    # indices

    # Initializing the kFolds dictionary
    kFoldsDict = defaultdict(np.array)

    # Initializing the idx_assigned numpy array and assigning indices to the k folds
    idx_assigned = np.empty(0)

    for i in range(_k):
        start = i * int(len(_idxList) / _k)
        end = (i+1) * int(len(_idxList) / _k)

        kSplit = _idxList[start:end]; kFoldsDict[i] = kSplit

        idx_assigned = np.concatenate((idx_assigned, kSplit), axis=0)

    # Retrieving remainder
    idx_unassigned = np.setdiff1d(_idxList, idx_assigned)

    # Check for remainders and randomly appending them to one of the k folds
    folds_idx = np.arange(0, _k, 1)
    if _shuffle:
        rng = default_rng(_seed); rng.shuffle(folds_idx)
    else:
        pass

    if len(_idxList) % _k != 0:
        for i, idx in enumerate(idx_unassigned):
            kFoldsDict[folds_idx[i]] = np.append(kFoldsDict[folds_idx[i]], idx)


    # === === === ===
    # Modifying the kFolds indices dictionary according to the given configuration

    # === === === ===
    # All representative trials will be excluded from the training and validation process at every
    # k-th fold
    if _configuration == 'noRepresentativeTrials':

        # First remove the repTrials from all indices in all k folds
        for k_fold, idxs in kFoldsDict.items():
            idxsIntersect = np.intersect1d(idxs, _repTrialsIdx)

            for iToRemove in idxsIntersect:
                kFoldsDict[k_fold] = np.delete(
                    kFoldsDict[k_fold], np.where(kFoldsDict[k_fold] == iToRemove)
                )

        # Balance out the number of indices throughout the k folds
        idxsMerged = np.zeros(0)
        for k_fold, idxs in kFoldsDict.items():
            idxsMerged = np.concatenate((idxsMerged, idxs), axis=0)

        lengthOfEachFold = int(idxsMerged.shape[0] / len(kFoldsDict)); count = 0
        remainingIdxs = idxsMerged[(len(kFoldsDict) * lengthOfEachFold):len(idxsMerged)]

        for k in kFoldsDict.keys():
            i = count * lengthOfEachFold; j = (count + 1) * lengthOfEachFold

            kFoldsDict[k] = idxsMerged[i:j]

            if count < len(remainingIdxs):
                kFoldsDict[k] = np.append(kFoldsDict[k], remainingIdxs[count])

            count += 1

        # Separating the kFoldsDict into dictionaries containing indices for training and testing
        for k_fold in kFoldsDict.keys():

            # Merged idxs across the k-1 for training
            idxsMerged = np.empty(0)

            for kInner_fold, idxs in kFoldsDict.items():
                if k_fold == kInner_fold:
                    kFoldsDict_Test[k_fold] = idxs

                else:
                    idxsMerged = np.concatenate((idxsMerged, idxs))

            kFoldsDict_Train[k_fold] = idxsMerged


    # === === === ===
    # At each k-th fold, the representative trials will be removed from the validation set and equally
    # (as best as possible) distributed among the other k-1 training folds

    # Algorithm:
    # 1. For each fold, the k-th fold (test set) is scanned for stride pairs that are representative
    #    (used in feature selection)
    # 2. The "scanned out" stride pairs are then distributed among the other k-1 folds for training

    elif _configuration == 'withRepresentativeTrials':

        for k_fold, idxs in kFoldsDict.items():

            # Extract the representative stride pairs for the k-th fold
            idxToExclude = list(set(idxs) & set(_repTrialsIdx))

            trimmedIdxs = idxs.copy()
            for repIdx in idxToExclude:
                # Removing the representative stride pairs from the k-th fold
                trimmedIdxs = np.delete(trimmedIdxs, np.where(trimmedIdxs == repIdx))

            kFoldsDict_Test[k_fold] = trimmedIdxs

            # Adding the representative stride pairs into the rest of the k-1 folds for training
            kFoldsDict_Train[k_fold] = idxToExclude

            # Adding the other stride pairs from the k-1 folds
            for k_innerFolds in kFoldsDict.keys():
                if k_innerFolds != k_fold:
                    kFoldsDict_Train[k_fold] = np.append(kFoldsDict_Train[k_fold], kFoldsDict[k_innerFolds])

    else:
        raise ValueError("Please pass a valid configuration")


    # === === === ===
    # Convert the arrays in both dictionaries to int types
    for k_fold in kFoldsDict_Train.keys():
        kFoldsDict_Train[k_fold] = kFoldsDict_Train[k_fold].astype(int)
        kFoldsDict_Test[k_fold]  = kFoldsDict_Test[k_fold].astype(int)

    return kFoldsDict_Train, kFoldsDict_Test


def initialize_decisionTree(
        _nature, _clfDepth, _clfWeightFractions, _clfSplitOption, _clfMaxFeatOpt, _randomState
):
    '''
    Function to initialize the decision tree object based on given inputs.

    Parameters
    ----------
    _nature : str
    The nature of the model. Possible options are "classification", "regression_mse", "regression_mae"

    _clfDepth : int
    Max depth of the decision tree classifier

    _clfWeightFractions : float
    Minimum weight fraction at each tree node

    _clfSplitOption : str
    Split option at each tree node

    _clfMaxFeatOpt : str
    Options for number of maximum features to be considered at each node

    _randomState : int
    Controls the randomness of the estimator
    '''
    if _nature == 'classification':
        # Initializing the decision tree classifier
        _clf = DecisionTreeClassifier(
            max_depth=_clfDepth, min_weight_fraction_leaf=_clfWeightFractions,
            splitter=_clfSplitOption, max_features=_clfMaxFeatOpt, random_state=_randomState
        )
    elif _nature == 'regression_mse':
        # Initializing the decision tree regressor
        _clf = DecisionTreeRegressor(
            criterion='mse',
            max_depth=_clfDepth, min_weight_fraction_leaf=_clfWeightFractions,
            splitter=_clfSplitOption, max_features=_clfMaxFeatOpt, random_state=_randomState
        )
    elif _nature == 'regression_mae':
        # Initializing the decision tree regressor
        _clf = DecisionTreeRegressor(
            criterion='mae',
            max_depth=_clfDepth, min_weight_fraction_leaf=_clfWeightFractions,
            splitter=_clfSplitOption, max_features=_clfMaxFeatOpt, random_state=_randomState
        )

    return _clf


def build_test_decisionTree(
        _XTrain, _XTest, _score, _nature,
        _clfDepth, _clfWeightFractions, _clfSplitOption, _clfMaxFeatOpt, _randomState,
        _preLearning=False, _returnX=False
):
    '''
    Build a decision tree based on the given data and its corresponding score.

    Wrapper to include a pre-selection for SMS-Stability, where all patients with a walking cane
    immediately gets a score of 3.

    Parameters
    ----------
    _XTrain : pandas.DataFrame
    DataFrame of (nSamplesTrain, nFeatures+Score)

    _XTest : pandas.DataFrame or None
    DataFrame of (nSamplesTest, nFeatures+Score). To simply fit the model without testing it,
    simply enter None

    _score: str
    Medical score to predict

    _nature : str
    The nature of the model. Possible options are "classification", "regression_mse", "regression_mae"

    _clfDepth : int
    Max depth of the decision tree classifier

    _clfWeightFractions : float
    Minimum weight fraction at each tree node

    _clfSplitOption : str
    Split option at each tree node

    _clfMaxFeatOpt : str
    Options for number of maximum features to be considered at each node

    _randomState : int
    Controls the randomness of the estimator

    _preLearning : bool
    Option for including pre-learning step for Stability-SMS models by automatically assigning
    Stability-SMSs of 3 for patients with a walking cane

    _returnX : bool
    Option to return the trimmed X (mainly for /plotter-datavalidation/trees/plotDecisionTrees/plot_trees.py

    Returns
    -------
    _yPredict : pandas.Series
    Pandas series of the predicted target for the given test dataset with the trained model

    _yTest : pandas.Series
    Pandas series of the actual target for the given test dataset

    clf : sklearn.tree.DecisionTreeClassifier or sklearn.tree.DecisionTreeRegressor
    Trained model
    '''
    # Update 20.10.2022 :: Include the option of having a manual pre-learning step for Stability-SMS
    # models

    # Also making sure that _preLearning is only turned on for SMSStability

    # All patients with a walking cane will be pre-filtered when it comes to Stability
    if _score == 'SMSStability':
        if _preLearning:
            print("Dealing with Stability :: All patients with a walking cane will be assigned a score of 3")
            _XTrain = _XTrain.drop(labels=_XTrain.loc[_XTrain['Cane'] == 1].index, axis=0)

            if not _XTest is None:
                _XTest_wCane = _XTest.loc[_XTest['Cane'] == 1]
                _XTest  = _XTest.drop(labels=_XTest_wCane.index, axis=0)
        else:
            print("Dealing with Stability :: No pre-learning with Cane. Will be carried out as usual")
    else:
        if _preLearning:
            raise ValueError("_preLearning can only be toggled for SMSStability!")

    # Extracting the target column
    _yTrain = _XTrain[_score]

    if not _XTest is None:
        _yTest = _XTest[_score]

    # Balancing the sample weights done on the cross validation level
    _XsampleWeights = balance_classDistribution_patient(_XTrain, _score)

    # Step taken to ensure that weights are matched accordingly
    _XTrain = pd.concat([_XTrain, _XsampleWeights], axis=1)

    # Extracting the weights
    _weights = _XTrain['Weight']

    # Dropping the following columns from _XTrain and _XTest
    # 1. Class feature (feature to be predicted)
    # 2. Sample weight (if needed)
    # 3. Pre-Learning step for sms-Stability with Cane (Update 20.10.2022)
    if _preLearning:
        print(f"Columns dropped: Weight, Cane, {_score}")
        _XTrain = _XTrain.drop(columns=['Weight', 'Cane', _score])
    else:
        print(f"Columns dropped: Weight, {_score}")
        _XTrain = _XTrain.drop(columns=['Weight', _score])

    if not _XTest is None:
        if _preLearning:
            _XTest  = _XTest.drop(columns=['Cane', _score])
        else:
            _XTest  = _XTest.drop(columns=[_score])

    clf = initialize_decisionTree(
        _nature, _clfDepth, _clfWeightFractions, _clfSplitOption, _clfMaxFeatOpt, _randomState
    )

    # Building the model from the training set (X_train, y_train)
    clf.fit(_XTrain, _yTrain, sample_weight=_weights)

    if _XTest is None:
        _yPredict = 0.0; _yTest = 0.0

    else:
        # Testing the model with the test dataset
        _yPredict = pd.Series(
            data=clf.predict(_XTest), index=_XTest.index, name=f"Predicted{_score}"
        )

        # Special modification when dealing with SMS-Stability
        if _score == 'SMSStability':

            # All patients with a walking cane gets a score of 3 for pre-learn option
            if _preLearning:
                _yPredict_wCane = pd.Series(
                    data=[3.0 for i in range(_XTest_wCane.shape[0])], index=_XTest_wCane.index
                )
                _yPredict = _yPredict.append(_yPredict_wCane)

                _yTest = _yTest.append(_XTest_wCane['SMSStability'])

    if _returnX:
        return _yPredict, _yTest, clf, _XTrain
    else:
        return _yPredict, _yTest, clf


def kFoldInnerCV(
        _df, _score, _kFoldsDictTrain, _kFoldsDictTest, _stridePair_idx_dict,
        _clfDepth, _clfWeightFractions, _clfSplitOption, _clfMaxFeatOpt, _randomState, _nature,
        _returnClf=False, _predict=True, _preLearning=False
):
    '''
    Carry out k-fold inner cross validation

    Parameters
    ----------
    _df : pandas.DataFrame
    DataFrame of (nSamples, nFeatures)

    _score : str
    Medical score to predict

    _kFoldsDictTrain : dict
    Dictionary for k folds mapping each k to a numpy array of indices to be used for training. The numpy array
    of indices (dictionary value) correspondonds to the k-1 folds being joined together

    _kFoldsDictTest : dict
    Dictionary for k folds mapping each k to a numpy array of indices to be used as test (validation set)

    _stridePair_idx_dict : dict
    Dictionary mapping the stride pair to a corresponding idx (integer)

    _clfDepth : int
    Max depth of the decision tree classifier

    _clfWeightFractions : float
    Minimum weight fraction at each tree node

    _clfSplitOption : str
    Split option at each tree node

    _clfMaxFeatOpt : str
    Options for number of maximum features to be considered at each node

    _randomState : int
    Controls the randomness of the estimator

    _nature : str
    The nature of the model. Possible options are "classification", "regression_mse", "regression_mae"

    _preLearning : bool
    Option for including pre-learning step for Stability-SMS models by automatically assigning
    Stability-SMSs of 3 for patients with a walking cane

    Returns
    -------
    kFold_y_real : dict(numpy.ndarray)
    Dictionary mapping each k-th fold to its corresponding validation set's real medical scores

    kFold_y_predict : dict(numpy.ndarray)
    Dictionary mapping each k-th fold to its corresponding validation set's predicted medical scores
    '''
    natureTypes = ['classification', 'regression_mse', 'regression_mae']
    if not _nature in natureTypes:
        raise ValueError('Invalid argument for <_nature> (classification, regression_mse/mae)')

    # === === === ===
    # Initializing the dictionaries to store the real and predicted scores at each k-th fold
    kFold_y_real = defaultdict(); kFold_y_predict = defaultdict(); clfs = defaultdict()

    accList = []
    for k in _kFoldsDictTrain.keys():
        print(f"Training {k} fold ... ")

        # Initializing the training and test dataframes
        X_train = pd.DataFrame(); X_test = pd.DataFrame()

        idx_train = [_stridePair_idx_dict[x] for x in _kFoldsDictTrain[k]]
        idx_test  = [_stridePair_idx_dict[x] for x in _kFoldsDictTest[k]]
        # Debug : print(f"{k}-Fold: Train ({len(idx_train)}) - Test ({len(idx_test)})")

        # Extracting the corresponding training and testing samples for this k-fold
        X_train = _df.loc[idx_train]; X_test = _df.loc[idx_test]

        # Update 12.05.2022 :: All patients with a walking cane gets a SMS-Stability of 3
        y_predict, y_test, clf = build_test_decisionTree(
            X_train, X_test, _score, _nature,
            _clfDepth, _clfWeightFractions, _clfSplitOption, _clfMaxFeatOpt, _randomState,
            _preLearning=_preLearning
        )

        clfs[k] = clf; print(clf)

        # Validate model on the k-th validation fold
        if _predict:
            if (_nature == 'regression_mse') or (_nature == 'regression_mae'):
                acc = balanced_accuracy_score(y_predict.round(), y_test)
            elif _nature == 'classification':
                acc = balanced_accuracy_score(y_predict, y_test)

            print(f"Balanced accuracy from the {k} fold : {acc}\n---")
            accList.append(acc)

            # Saving the results
            kFold_y_real[k] = y_test; kFold_y_predict[k] = y_predict

    if _predict:
        print("========================================================")
        print(f" >> Average balanced accuracy : {sum(accList)/len(accList)}")
        print("========================================================\n")

    if _returnClf:
        return kFold_y_predict, kFold_y_real, clfs
    else:
        return kFold_y_predict, kFold_y_real


def kFoldOuterCV(
        _df, _score, _kFoldsDictTrain, _kFoldsDictTest, _stridePair_idx_dict,
        _parametersPerOuterKFold, _randomState, _nature, _returnClf=False, _preLearning=False
):
    '''
    Carry out OUTER k-fold cross validation, each k-fold has the optimal parameters obtained from its
    corresponding INNER k-fold cross validation

    Parameters
    ----------
    _df : pandas.DataFrame
    DataFrame of (nSamples, nFeatures)

    _score : str
    Medical score to predict

    _kFoldsDictTrain : dict
    Dictionary for k folds mapping each k to a numpy array of indices to be used for training. The numpy array
    of indices (dictionary value) correspondonds to the k-1 folds being joined together

    _kFoldsDictTest : dict
    Dictionary for k folds mapping each k to a numpy array of indices to be used as test (validation set)

    _stridePair_idx_dict : dict
    Dictionary mapping the stride pair to a corresponding idx (integer)

    _parametersPerOuterKFold : dict
    Dictionary containing parameters for each OUTER kFold, obtained from its corresponding INNER kFold

    _randomState : int
    Controls the randomness of the estimator

    _nature : str
    The nature of the model. Possible options are "classification", "regression_mse", "regression_mae"

    _preLearning : bool
    Option for including pre-learning step for Stability-SMS models by automatically assigning
    Stability-SMSs of 3 for patients with a walking cane

    Returns
    -------
    kFold_y_real : dict(numpy.ndarray)
    Dictionary mapping each k-th fold to its corresponding validation set's real medical scores

    kFold_y_predict : dict(numpy.ndarray)
    Dictionary mapping each k-th fold to its corresponding validation set's predicted medical scores
    '''
    natureTypes = ['classification', 'regression_mse', 'regression_mae']
    if not _nature in natureTypes:
        raise ValueError('Invalid argument for <_nature> (classification, regression_mse/mae)')

    # === === === ===
    # Initializing the dictionaries to store the real and predicted scores at each k-th fold
    kFold_y_real = defaultdict(); kFold_y_predict = defaultdict(); clfs = defaultdict()

    for k in _kFoldsDictTrain.keys():
        print(f"Training {k} fold ... ")

        depth = _parametersPerOuterKFold[f'{k}Fold']['maxDepths']
        weightFraction = _parametersPerOuterKFold[f'{k}Fold']['minWeightFractionLeaf']
        splitOption = _parametersPerOuterKFold[f'{k}Fold']['splitOptions']
        maxFeatOption = _parametersPerOuterKFold[f'{k}Fold']['maxFeatOptions']

        print(
            "Decision tree parameters\n---\n" +
            f"Split Option                 : {splitOption}\n" +
            f"Max Features                 : {maxFeatOption}\n" +
            f"Max Tree Depth               : {depth}\n" +
            f"Min Weight Fractions in Leaf : {weightFraction}\n---\n" +
            f"Dealing with the outer {k}-Fold\n---"
        )

        # Initializing the training and test dataframes
        X_train = pd.DataFrame(); X_test = pd.DataFrame()

        idx_train = [_stridePair_idx_dict[x] for x in _kFoldsDictTrain[k]]
        idx_test  = [_stridePair_idx_dict[x] for x in _kFoldsDictTest[k]]
        # Debug : print(f"{k}-Fold: Train ({len(idx_train)}) - Test ({len(idx_test)})")

        # Extracting the corresponding training and testing samples for this k-fold
        X_train = _df.loc[idx_train]; X_test = _df.loc[idx_test]

        # Update 12.05.2022 :: All patients with a walking cane gets a SMS-Stability of 3
        y_predict, y_test, clf = build_test_decisionTree(
            X_train, X_test, _score, _nature,
            _clfDepth, _clfWeightFractions, _clfSplitOption, _clfMaxFeatOpt, _randomState,
            _preLearning=_preLearning
        )

        clfs[k] = clf; print(clf)

        if (_nature == 'regression_mse') or (_nature == 'regression_mae'):
            acc = balanced_accuracy_score(y_predict.round(), y_test)
        elif _nature == 'classification':
            acc = balanced_accuracy_score(y_predict, y_test)

        print(f"Balanced accuracy from the {k} fold : {acc}\n---")

        # Saving the results
        kFold_y_real[k] = y_test; kFold_y_predict[k] = y_predict

    if _returnClf:
        return kFold_y_predict, kFold_y_real, clfs
    else:
        return kFold_y_predict, kFold_y_real


def kFoldOuterCV_wFinalHP(
        _df, _score, _kFoldsDictTrain, _kFoldsDictTest, _stridePair_idx_dict,
        _parameters, _randomState, _nature, _returnClf=False, _preLearning=False
):
    '''
    Carry out OUTER k-fold cross validation, each k-fold has the optimal parameters obtained from its
    corresponding INNER k-fold cross validatin

    Parameters
    ----------
    _df : pandas.DataFrame
    DataFrame of (nSamples, nFeatures)

    _score : str
    Medical score to predict

    _kFoldsDictTrain : dict
    Dictionary for k folds mapping each k to a numpy array of indices to be used for training. The numpy array
    of indices (dictionary value) correspondonds to the k-1 folds being joined together

    _kFoldsDictTest : dict
    Dictionary for k folds mapping each k to a numpy array of indices to be used as test (validation set)

    _stridePair_idx_dict : dict
    Dictionary mapping the stride pair to a corresponding idx (integer)

    _parameters : dict
    Dictionary containing parameters

    Update 12.04.2022 :: These parameters are obtained by "averaging" the optimal hyperparameters obtained
    from the outer cross validation (refer to documentation for more details on the "averaging" process

    _randomState : int
    Controls the randomness of the estimator

    _nature : str
    The nature of the model. Possible options are "classification", "regression_mse", "regression_mae"

    _preLearning : bool
    Option for including pre-learning step for Stability-SMS models by automatically assigning
    Stability-SMSs of 3 for patients with a walking cane

    Returns
    -------
    kFold_y_real : dict(numpy.ndarray)
    Dictionary mapping each k-th fold to its corresponding validation set's real medical scores

    kFold_y_predict : dict(numpy.ndarray)
    Dictionary mapping each k-th fold to its corresponding validation set's predicted medical scores
    '''
    natureTypes = ['classification', 'regression_mse', 'regression_mae']
    if not _nature in natureTypes:
        raise ValueError('Invalid argument for <_nature> (classification, regression_mse/mae)')

    # === === === ===
    # Initializing the dictionaries to store the real and predicted scores at each k-th fold
    kFold_y_real = defaultdict(); kFold_y_predict = defaultdict(); clfs = defaultdict()

    depth = _parameters['maxDepths']
    weightFraction = _parameters['minWeightFractionLeaf']
    splitOption = _parameters['splitOptions']
    maxFeatOption = _parameters['maxFeatOptions']

    for k in _kFoldsDictTrain.keys():
        print(f"Training {k} fold ... ")

        print(
            "Decision tree parameters\n---\n" +
            f"Split Option                 : {splitOption}\n" +
            f"Max Features                 : {maxFeatOption}\n" +
            f"Max Tree Depth               : {depth}\n" +
            f"Min Weight Fractions in Leaf : {weightFraction}\n---\n" +
            f"Dealing with the outer {k}-Fold\n---"
        )

        # Initializing the training and test dataframes
        X_train = pd.DataFrame(); X_test = pd.DataFrame()

        idx_train = [_stridePair_idx_dict[x] for x in _kFoldsDictTrain[k]]
        idx_test  = [_stridePair_idx_dict[x] for x in _kFoldsDictTest[k]]
        # Debug : print(f"{k}-Fold: Train ({len(idx_train)}) - Test ({len(idx_test)})")

        # Extracting the corresponding training and testing samples for this k-fold
        X_train = _df.loc[idx_train]; X_test = _df.loc[idx_test]

        # Update 12.05.2022 :: All patients with a walking cane gets a SMS-Stability of 3
        y_predict, y_test, clf = build_test_decisionTree(
            X_train, X_test, _score, _nature,
            depth, weightFraction, splitOption, maxFeatOption, _randomState,
            _preLearning=_preLearning
        )

        clfs[k] = clf; print(clf)

        if (_nature == 'regression_mse') or (_nature == 'regression_mae'):
            acc = balanced_accuracy_score(y_predict.round(), y_test)
        elif _nature == 'classification':
            acc = balanced_accuracy_score(y_predict, y_test)

        print(f"Balanced accuracy from the {k} fold : {acc}\n---")

        # Saving the results
        kFold_y_real[k] = y_test; kFold_y_predict[k] = y_predict

    if _returnClf:
        return kFold_y_predict, kFold_y_real, clfs
    else:
        return kFold_y_predict, kFold_y_real
