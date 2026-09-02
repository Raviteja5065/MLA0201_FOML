#exp-7

import kagglehub
path = kagglehub.dataset_download("dileep070/heart-disease-prediction-using-logistic-regression")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

data = pd.read_csv(f'{path}/framingham.csv')

X = data.iloc[:, :-1]
Y = data.iloc[:, -1]

# Impute missing values in X with the mean of each column
X = X.fillna(X.mean())

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=0
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, Y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(Y_test, pred))
