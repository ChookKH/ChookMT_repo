import os, sys
import pickle
from pathlib import Path
from collections import defaultdict

# Appending the stdutils package path to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if len(sys.argv) < 2:
    print("Possible usage: python3 print_pat_trial_metadata.py <dirOfPatientsInfo>")
    print(
        "\nExample usage: python3 print_pat_trial_metadata.py " +
        "../process-rawdata/pat_trial_metadata/Export_v00_07062021-DevSamples"
    )
    sys.exit(1)
else:
    _collections_dir = Path(sys.argv[1])

# Getting the subjects pickled data
subjects_pkl_path = _collections_dir.joinpath(f"{_collections_dir.name}-Patients.pkl")
subjects_pkl = open(subjects_pkl_path, 'rb')
Subjects = pickle.load(subjects_pkl)
subjects_pkl.close()

# Getting the trials pickled data
trials_pkl_path = _collections_dir.joinpath(f"{_collections_dir.name}-Trials.pkl")
trials_pkl = open(trials_pkl_path, 'rb')
Trials = pickle.load(trials_pkl)
trials_pkl.close()


# === === === ===
# Patients/Test Subjects
print("Number of patients/test subjects: " + str(len(Subjects)))

# === === === ===
# Strides
print("Number of trials: " + str(len(Trials)))

# Printing a random trial object
randomSelectedTrial = Trials[0]

sys.exit(0)
