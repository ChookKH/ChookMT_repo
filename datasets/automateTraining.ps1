# === === === ===
# Liaw dataset
# === === === ===
# SKlearn tree based regressors
python .\ML.py liaw Trunk && `
python .\ML.py liaw Leg && `
python .\ML.py liaw Arm && `
python .\ML.py liaw Speed && `
python .\ML.py liaw Fluency && `
python .\ML.py liaw Stability && `


# === === === ===
# Chook dataset
# === === === ===
# SKlearn tree based regressors
python .\ML.py std Trunk && `
python .\ML.py std Leg && `
python .\ML.py std Arm && `
python .\ML.py std Speed && `
python .\ML.py std Fluency && `
python .\ML.py std Stability && `

python .\ML.py ci Trunk && `
python .\ML.py ci Leg && `
python .\ML.py ci Arm && `
python .\ML.py ci Speed && `
python .\ML.py ci Fluency && `
python .\ML.py ci Stability 