import os, sys
import shutil
import pickle
from pathlib import Path
from collections import defaultdict

'''
This script updates the metadata of the pickled list of stdutils.patient.Trials objects in the given
metadata folder if the user decides to rename the directory of the stored exported data
'''

# Appending the stdutils package path to sys.path
sys.path.append(os.path.dirname(os.getcwd()))
from stdutils.patient import Patient, Trial

if len(sys.argv) < 3:
    print("Possible usage:\npython3 edit_metadata.py <dirOfExportedMetadata> <newDirOfMetadata>")
    sys.exit(1)
else:
    dirOfExportedMetadata = Path(sys.argv[1])
    newDirOfMetadata = Path(sys.argv[2])


# === === === ===
# Only the Trials pickled list if of interest
for f in os.scandir(dirOfExportedMetadata):
    if "-Trials.pkl" in f.name:
        trialsPklPath = f

# Pickling the list of Trial objects
with open(trialsPklPath, 'rb') as f:
    Trials = pickle.load(f)


# === === === ===
# Asking the user for the new desired name of the directory of the exported data
dirOfExportedData = Path(Trials[0].FolderPath).parent
print(f"The directory of the exported data is currently : \n{dirOfExportedData}")

usrNewDirInput = input("What would you like to rename the directory to?\n")

newDirOfExportedData = Path(usrNewDirInput)


# === === === ===
# Renaming the folder paths in the Trial objects and saving the new pickled data

# Updating the trial objects properties appending them to a list
newTrials = []

for t in Trials:
    t.FolderPath = newDirOfExportedData.joinpath(t.TrialID)
    t.cleanProperties(); t.getData([])

    newTrials.append(t)

# Saving the trials list in a pickled file
with open(newDirOfMetadata.joinpath("Trials.pkl"), 'wb') as f:
    pickle.dump(newTrials, f)

# Copying the other metadata files that did not have to be modified
for f in os.scandir(dirOfExportedMetadata):
    if not "Trials.pkl" in f.name:
        shutil.copyfile(f, newDirOfMetadata.joinpath(f.name))

sys.exit(0)
