A = {
    1:'A',
    2:'B',
    3:'C',
    4:'D',
    5:'E'
}

# Via keys()
for k in A.keys():
    print(f"{k}: {A[k]}")

# Via values()
for val in A.values():
    print(val)

# Via items()
for k, val in A.items():
    print(f"{k}: {val}")