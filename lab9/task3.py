import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('customer_segmentation.csv')


customer_data = df.groupby('CustomerID').agg({
    'Quantity': 'sum',
    'UnitPrice': 'mean',
    'InvoiceNo': 'nunique',  
    'Country': 'first'  
}).reset_index()

customer_data['TotalSpending'] = df.groupby('CustomerID').apply(
    lambda x: (x['Quantity'] * x['UnitPrice']).sum()
).values


df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
date_range = df['InvoiceDate'].max() - df['InvoiceDate'].min()
months = date_range.days / 30
customer_data['PurchaseFrequency'] = customer_data['InvoiceNo'] / months

customer_data = customer_data.rename(columns={
    'InvoiceNo': 'VisitCount',
    'UnitPrice': 'AvgItemPrice'
})

customer_data = customer_data.dropna()


threshold = customer_data['TotalSpending'].quantile(0.8)
customer_data['HighValue'] = (customer_data['TotalSpending'] >= threshold).astype(int)

def handle_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column] = np.where(df[column] > upper_bound, upper_bound, 
                         np.where(df[column] < lower_bound, lower_bound, df[column]))
    return df

for col in ['TotalSpending', 'VisitCount', 'PurchaseFrequency']:
    customer_data = handle_outliers(customer_data, col)

features = ['TotalSpending', 'VisitCount', 'PurchaseFrequency', 'AvgItemPrice']
X = customer_data[features]
y = customer_data['HighValue']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y)


lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(X_train, y_train)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.2f}")
    print("="*50)

print("Logistic Regression Performance:")
evaluate_model(lr_model, X_test, y_test)

print("SVM Performance:")
evaluate_model(svm_model, X_test, y_test)

print("Random Forest Performance:")
evaluate_model(rf_model, X_test, y_test)


print("\nLogistic Regression Coefficients (Hyperplane weights):")
for feature, coef in zip(features, lr_model.coef_[0]):
    print(f"{feature}: {coef:.4f}")

print("\nRandom Forest Feature Importance:")
for feature, importance in zip(features, rf_model.feature_importances_):
    print(f"{feature}: {importance:.4f}")

print("\nExample Decision Rules:")
print("1. IF TotalSpending > £X AND VisitCount > Y THEN HighValue")
print("2. IF PurchaseFrequency > Z THEN HighValue")
print("3. IF AvgItemPrice > A AND VisitCount > B THEN HighValue")

plt.figure(figsize=(10, 6))
sns.barplot(x=rf_model.feature_importances_, y=features)
plt.title('Feature Importance for Customer Value Prediction')
plt.show()


def classify_customer(features_dict, model=rf_model, scaler=scaler):
    """Classify a new customer based on their features"""
    input_df = pd.DataFrame([features_dict])
    
    scaled_input = scaler.transform(input_df)
    
    prediction = model.predict(scaled_input)
    probability = model.predict_proba(scaled_input)[0][1]
    
    return {
        'prediction': 'HighValue' if prediction[0] == 1 else 'LowValue',
        'probability': probability
    }

new_customer = {
    'TotalSpending': 1200,
    'VisitCount': 15,
    'PurchaseFrequency': 2.5,
    'AvgItemPrice': 45
}

print("\nNew Customer Classification:")
print(classify_customer(new_customer))