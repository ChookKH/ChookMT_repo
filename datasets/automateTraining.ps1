# === === === ===
# Liaw dataset
# === === === ===
# Neural networks
# python .\ML.py liaw NN Trunk Train && `
# python .\ML.py liaw NN Leg Train && `
# python .\ML.py liaw NN Arm Train && `
# python .\ML.py liaw NN Speed Train && `
# python .\ML.py liaw NN Fluency Train && `
# python .\ML.py liaw NN Stability Train && `

# SKlearn tree based regressors
python .\ML.py liaw SK Trunk Train && `
python .\ML.py liaw SK Leg Train && `
python .\ML.py liaw SK Arm Train && `
python .\ML.py liaw SK Speed Train && `
python .\ML.py liaw SK Fluency Train && `
python .\ML.py liaw SK Stability Train && `


# === === === ===
# Chook dataset
# === === === ===
# Neural networks
# python .\ML.py std NN Trunk Train && `
# python .\ML.py std NN Leg Train && `
# python .\ML.py std NN Arm Train && `
# python .\ML.py std NN Speed Train && `
# python .\ML.py std NN Fluency Train && `
# python .\ML.py std NN Stability Train && `

# SKlearn tree based regressors
python .\ML.py std SK Trunk Train && `
python .\ML.py std SK Leg Train && `
python .\ML.py std SK Arm Train && `
python .\ML.py std SK Speed Train && `
python .\ML.py std SK Fluency Train && `
python .\ML.py std SK Stability Train && `

python .\ML.py ci SK Trunk Train && `
python .\ML.py ci SK Leg Train && `
python .\ML.py ci SK Arm Train && `
python .\ML.py ci SK Speed Train && `
python .\ML.py ci SK Fluency Train && `
python .\ML.py ci SK Stability Train 