# === === === ===
# Liaw dataset
# === === === ===
python .\feature_selection.py liaw Trunk && `
python .\feature_selection.py liaw Leg && `
python .\feature_selection.py liaw Arm && `
python .\feature_selection.py liaw Speed && `
python .\feature_selection.py liaw Fluency && `
python .\feature_selection.py liaw Stability && `


# === === === ===
# STD dataset
# === === === ===
python .\feature_selection.py std Trunk && `
python .\feature_selection.py std Leg && `
python .\feature_selection.py std Arm && `
python .\feature_selection.py std Speed && `
python .\feature_selection.py std Fluency && `
python .\feature_selection.py std Stability 