#exp-3

import kagglehub
path = kagglehub.dataset_download("thedevastator/jobs-dataset-from-glassdoor")

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv(f'{path}/salary_data_cleaned.csv')

X = data.iloc[:, :-1]
Y = data.iloc[:, -1]

encoders = {}

for column in X.columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    encoders[column] = le

target = LabelEncoder()
Y = target.fit_transform(Y)

model = DecisionTreeClassifier(criterion="entropy")
model.fit(X, Y)

print("Decision Tree Built Successfully")

sample = [list(X.iloc[0])]
prediction = model.predict(sample)

print("Prediction:", target.inverse_transform(prediction))
