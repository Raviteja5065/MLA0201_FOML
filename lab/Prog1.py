#exp-1

import kagglehub
path = kagglehub.dataset_download("fredericobreno/play-tennis")
import pandas as pd

# Read dataset
data = pd.read_csv(f'{path}/play_tennis.csv')

concepts = data.iloc[:, :-1].values
target = data.iloc[:, -1].values

def find_s(concepts, target):
    hypothesis = None

    for i, val in enumerate(target):
        if val.lower() == "yes":
            hypothesis = concepts[i].copy()
            break

    for i, val in enumerate(target):
        if val.lower() == "yes":
            for j in range(len(hypothesis)):
                if hypothesis[j] != concepts[i][j]:
                    hypothesis[j] = '?'

    return hypothesis

print("Most Specific Hypothesis:")
print(find_s(concepts, target))
