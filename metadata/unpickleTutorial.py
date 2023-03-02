import stdutils
import pickle as pkl

# "rb" means read binary
with open("exportedData-Patients.pkl", "rb") as handle:
    patientsList = pkl.load(handle)

for pat in patientsList:
    print(pat)
    print(type(pat))

with open("exportedData-Trials.pkl", "rb") as handle:
    trialsList = pkl.load(handle)

for trial in trialsList:
    print(trial)
    print(type(trial))