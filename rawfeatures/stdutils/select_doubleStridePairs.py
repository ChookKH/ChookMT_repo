import pandas as pd
from pathlib import Path
from collections import defaultdict


def assigning_complementPairs(_complementSet, _commonSet, _longList, _rLonger, _commonPairs):
    '''
    Sub-function to assign pairs of right and left normalized double strides that will not
    have the same indices

    Parameters
    ----------
    _complementSet : list
    List containing indices pertaining to the complement set of the indices, which have been paired with
    identical indices

    _commonSet : list
    List containing indices pertaining to the set of indices, which have been paired with identical indices

    _longList : list
    The longer list of indices

    _rLonger : bool
    Indicating if the indices pertaining to the right normalized stride is longer or not

    _commonPairs : dict
    Dictionary mapping the index pair with a pair of indices
    '''
    if len(_complementSet) != 0:
        for i in _complimentSet:
            pairingFound = False
            # For every index in the set of compliment indices,
            # find if i-1 is in the longer list
            if (i-1 in _longList and not i-1 in _commonSet):
                if _rLonger:
                    _leftDSIdx = i; _rightDSIdx = i-1; pairingFound = True
                else:
                    _leftDSIdx = i-1; _rightDSIdx = i; pairingFound = True
            else:
                if (i+1 in _longList and not i+1 in _commonSet):
                    if _rLonger:
                        _leftDSIdx = i; _rightDSIdx = i+1; pairingFound = True
                    else:
                        _leftDSIdx = i+1; _rightDSIdx = i; pairingFound = True

            # _commonPairs[<idx>] = [<left> <right>]
            if pairingFound:
                print("Pair with different stride indices added ... ")
                _commonPair = [_leftDSIdx, _rightDSIdx]
                _commonPairs[len(_commonPairs)] = _commonPair


def select_commonPairs(_trial):
    '''
    Function that takes a list of right and left normalized strides and match
    them into appropriate pairs
    '''
    # === === === ===
    # Dictionaries that map stride index to file name
    # Key: DoubleStrideIndex, Value=PathOfKinematicsFile
    idxFileMapR = defaultdict(); idxFileMapL = defaultdict()

    for i in _trial.KinematicsR:
        idxFileMapR[int((Path(i).name).split("_")[-2])] = Path(i)

    for i in _trial.KinematicsL:
        idxFileMapL[int((Path(i).name).split("_")[-2])] = Path(i)


    # === === === ===
    # Determining common stride indices and determining the longer and shorter list
    _rList = list(idxFileMapR.keys()); _lList = list(idxFileMapL.keys())

    if len(_rList) < len(_lList):
        c = list(set(_rList).intersection(_lList)); uc = list(set(_rList).difference(_lList))
        shortList = _rList; longList = _lList; longList_R = False
    else:
        c = list(set(_lList).intersection(_rList)); uc = list(set(_lList).difference(_rList))
        shortList = _lList; longList = _rList; longList_R = True

    commonPairs = defaultdict(list)

    # === === === ===
    # Assigning the corresponding pair of strides
    # For pairs that have the same indices
    for idx, pair in enumerate(c):
        commonPair = [pair, pair]
        commonPairs[idx] = commonPair


    # For pairs that will have different indices
    assigning_complementPairs(uc, c, longList, longList_R, commonPairs)

    return commonPairs, idxFileMapR, idxFileMapL


def initialize_gaitParametersIdxFileMap(_trial):
    '''
    Function that takes a Trial object and initializes a dictionary mapping the stride index to
    the corresponding gait parameters file
    '''
    # === === === ===
    # Dictionaries that map gait parameters index to file name
    # Key: GaitParameterIndex, Value=PathOfKinematicsFile
    idxFileMapR = defaultdict(); idxFileMapL = defaultdict()

    for i in _trial.GaitParametersR:
        idxFileMapR[int((Path(i).name).split("_")[-2])] = Path(i)
    for i in _trial.GaitParametersL:
        idxFileMapL[int((Path(i).name).split("_")[-2])] = Path(i)

    return idxFileMapR, idxFileMapL

