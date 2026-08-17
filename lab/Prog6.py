#exp-6

import kagglehub
path = kagglehub.dataset_download("harshilpatel355/autoirrigationdata")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv(f'{path}/data.csv')

X = data.iloc[:, :-1]
Y = data.iloc[:, -1]

# Encode categorical features in X
for column in X.columns:
    if X[column].dtype == 'object':
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=0
)

model = GaussianNB()

model.fit(X_train, Y_train)

pred = model.predict(X_test)

print("Confusion Matrix")

print(confusion_matrix(Y_test, pred))

print("Accuracy")

print(accuracy_score(Y_test, pred))
