# Initialization file for the common-utils package
# Initialization date: 28.04.2021
from .patient_refband_grouping import patient_refband_grouping
from .gaitphase_patient_rawfeatures import extract_gaitphase_rawfeatures

from .sampleWeights import balance_classDistribution_patient
from .sampleWeights import balance_patientnTrials

import os
import pickle
from pathlib import Path
dir = os.path.dirname(os.path.realpath(__file__))

def returnSeconds_inHMSFormat(_seconds):
    '''
    Returns time taken in seconds in HH:MM:SS format
    '''
    if _seconds >= 60:
        minutes = int(_seconds / 60)
        seconds = _seconds - (minutes * 60)
    else:
        minutes = 0
        seconds = _seconds

    if minutes >= 60:
        hours = int(minutes / 60)
        minutes = minutes - (hours * 60)
    else:
        hours = 0

    seconds = round(seconds)
    if hours < 10:
        hours = f"0{hours}"
    if minutes < 10:
        minutes = f"0{minutes}"
    if seconds < 10:
        seconds = f"0{seconds}"

    return (f"{hours}:{minutes}:{seconds}")

def get_patient_scores():
    '''
    Get patient scores as a pandas DataFrame
    '''
    import pandas as pd

    datfile = Path(dir).joinpath("patient_scores.dat")

    patient_scores = pd.read_csv(
        datfile,
        sep=' ', index_col=0
    )

    return patient_scores

def get_score_distribution():
    '''
    Gives a list of medical scores and the patient's that have been evaluated according
    to that medical score
    '''
    from collections import defaultdict

    f = open(Path(dir).joinpath("score_distribution.dat"), "r")
    lines = f.read()
    lines = lines.replace("\n", "")
    opener_idx = []
    closer_idx = []
    for idx, c in enumerate(lines):
        if c == '{':
            opener_idx.append(idx)
        elif c == '}':
            closer_idx.append(idx)

    patients_score_count = defaultdict(list)

    for i in range(len(opener_idx)):
        if i == 0:
            score_type = lines[0:opener_idx[i]-1]
        else:
            score_type = lines[closer_idx[i-1]+1:opener_idx[i]-1]

        patient_ids = lines[opener_idx[i]+1:closer_idx[i]]

        patient_idx_split = patient_ids.split(", ")
        patients_score_count[score_type] = patient_idx_split

    f.close()

    return patients_score_count

def load_patients_trials(_collections_dir):
    '''
    Function to load and return the lists of Patient and Trials pickle objects contained in
    the given directory
    '''
    # Getting the subjects pickled data
    subjects_pkl_path = _collections_dir.joinpath(f"{_collections_dir.name}-Patients.pkl")
    subjects_pkl = open(subjects_pkl_path, 'rb')
    subjects = pickle.load(subjects_pkl)
    subjects_pkl.close()

    # Getting the trials pickled data
    trials_pkl_path = _collections_dir.joinpath(f"{_collections_dir.name}-Trials.pkl")
    trials_pkl = open(trials_pkl_path, 'rb')
    trials = pickle.load(trials_pkl)
    trials_pkl.close()

    return subjects, trials

def map_patients_trials(_patients, _trials):
    '''
    Function to map each trial object to the corresponding patient object.

    Returns a dictionary
    <Patient.ID>: [<TrialA1>, <TrialA2>]
    '''
    from collections import defaultdict
    patient_trials_dict = defaultdict(list)

    for pat in _patients:
        for t in _trials:
            if pat.ID in t.TrialID:
                patient_trials_dict[pat.ID].append(t)

    return patient_trials_dict
