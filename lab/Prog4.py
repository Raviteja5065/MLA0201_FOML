#exp-4

import kagglehub
path = kagglehub.dataset_download("shubh0799/churn-modelling")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv(f'{path}/Churn_Modelling.csv')

X = data.iloc[:, :-1]
Y = data.iloc[:, -1]

# Encode categorical features
for column in X.columns:
    if X[column].dtype == 'object':
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=0
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000)

model.fit(X_train, Y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(Y_test, pred))
