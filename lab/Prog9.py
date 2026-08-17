#exp-9

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error

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

X_train, X_test, Y_train, Y_test = train_test_split(
    X_processed, Y, test_size=0.3, random_state=0
)

# Linear Regression
linear = LinearRegression()
linear.fit(X_train, Y_train)
linear_pred = linear.predict(X_test)

# Polynomial Regression
poly = PolynomialFeatures(degree=2)

X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

poly_model = LinearRegression()

poly_model.fit(X_train_poly, Y_train)

poly_pred = poly_model.predict(X_test_poly)

print("Linear Regression MSE")
print(mean_squared_error(Y_test, linear_pred))

print("Polynomial Regression MSE")
print(mean_squared_error(Y_test, poly_pred))
