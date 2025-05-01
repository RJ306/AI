import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = {
    'square_footage': [1500, 2000, 1800, 2200, 1900, 2100, 1700, 2400, None, 1950, 2300, 1600, 2050, 1850, 2500],
    'bedrooms': [3, 4, 3, 4, 3, 4, 3, 4, 3, 3, 4, 3, 4, 3, 5],
    'bathrooms': [2, 2.5, 2, 3, 2, 2.5, 2, 3, 2, 2, 3, 2, 2.5, 2, 3.5],
    'age': [10, 5, 15, 2, 8, 3, 12, 1, 20, 7, 4, 18, 6, 9, 0],
    'neighborhood': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'B'],
    'price': [300000, 400000, 320000, 450000, 350000, 420000, 310000, 480000, 280000, 340000, 470000, 290000, 430000, 330000, 520000]
}

df = pd.DataFrame(data)


num_cols = ['square_footage', 'bedrooms', 'bathrooms', 'age']
for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

cat_cols = ['neighborhood']

X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols)])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

model.fit(X_train, y_train)

preprocessor.fit(X)
feature_names = (num_cols + 
                list(model.named_steps['preprocessor']
                    .named_transformers_['cat']
                    .named_steps['onehot']
                    .get_feature_names_out(cat_cols)))

importances = model.named_steps['regressor'].feature_importances_

feature_importance = pd.DataFrame({'feature': feature_names, 'importance': importances})
feature_importance = feature_importance.sort_values('importance', ascending=False)

print("=== Feature Importance ===")
print(feature_importance)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n=== Model Performance Metrics ===")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"R-squared (R2): {r2:.2f}")

new_house = pd.DataFrame({
    'square_footage': [2100],
    'bedrooms': [3],
    'bathrooms': [2.5],
    'age': [5],
    'neighborhood': ['B']
})

predicted_price = model.predict(new_house)

print("\n=== Price Prediction for New House ===")
print(f"Features:\n{new_house}")
print(f"\nPredicted Price: ${predicted_price[0]:,.2f}")