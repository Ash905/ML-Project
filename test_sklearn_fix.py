import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Create sample data
df = pd.DataFrame({
    'num': [1, 2, 3, 4, 5],
    'cat': ['a', 'b', 'a', 'b', 'c'],
    'target': [10, 20, 30, 40, 50]
})

X = df.drop('target', axis=1)
y = df['target']

# Build preprocessor (same as notebook)
num_features = X.select_dtypes(exclude="object").columns
cat_features = X.select_dtypes(include="object").columns

numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer([
    ("OneHotEncoder", categorical_transformer, cat_features),
    ("StandardScaler", numeric_transformer, num_features),
])

# Transform data
X_transformed = preprocessor.fit_transform(X)

# Train Ridge regression (this is where sym_pos error occurred)
ridge = Ridge()
ridge.fit(X_transformed, y)
predictions = ridge.predict(X_transformed)

print("✓ Ridge regression training successful!")
from sklearn import __version__ as sk_version
print(f"✓ scikit-learn version: {sk_version}")
print(f"✓ Predictions: {predictions}")
