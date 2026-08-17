#exp-10

import kagglehub
path = kagglehub.dataset_download("fares279/customers-transactions")
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

data = pd.read_csv(f'{path}/Customer_Transactions.csv')

# Identify categorical and numerical columns
categorical_features = data.select_dtypes(include=['object']).columns
numerical_features = data.select_dtypes(include=['number']).columns

# Create a column transformer for one-hot encoding categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough' # Keep numerical features as they are
)

# Apply the transformations to X and convert to a dense array
X = preprocessor.fit_transform(data).toarray()

gmm = GaussianMixture(n_components=3, random_state=0)

gmm.fit(X)

labels = gmm.predict(X)

print("Cluster Labels")

print(labels)
