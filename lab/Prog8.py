#exp-8

import kagglehub
path = kagglehub.dataset_download("mirichoi0218/insurance")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

data = pd.read_csv(f'{path}/insurance.csv')

X = data.iloc[:, :-1]
Y = data.iloc[:, -1]

# Identify categorical and numerical columns
categorical_features = X.select_dtypes(include=['object']).columns
numerical_features = X.select_dtypes(include=['number']).columns

# Create a column transformer for one-hot encoding categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ], 
    remainder='passthrough' # Keep numerical features as they are
)

# Apply the transformations
X_processed = preprocessor.fit_transform(X)

# Convert the processed X back to a DataFrame (optional, for better inspection if needed)
# To get feature names after one-hot encoding:
# new_categorical_features = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
# all_features = list(new_categorical_features) + list(numerical_features)
# X = pd.DataFrame(X_processed, columns=all_features)

X_train, X_test, Y_train, Y_test = train_test_split(
    X_processed, Y, test_size=0.3, random_state=0
)

model = LinearRegression()

model.fit(X_train, Y_train)

pred = model.predict(X_test)

print("Mean Squared Error:", mean_squared_error(Y_test, pred))
