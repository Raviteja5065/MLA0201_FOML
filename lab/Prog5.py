#exp-5

import kagglehub
path = kagglehub.dataset_download("bulentsiyah/knearest-neighbour-knn-classification")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv(f'{path}/data.csv')

Y = data.iloc[:, 1]

X = data.iloc[:, 2:-1]

le = LabelEncoder()
Y = le.fit_transform(Y)

# X should now only contain numerical features, so no need for a separate encoding loop for X.

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=1
)

model = KNeighborsClassifier(n_neighbors=3)

model.fit(X_train, Y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(Y_test, pred))
