import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, 
                            confusion_matrix, 
                            accuracy_score,
                            roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

df = pd.read_csv('emails.csv')

X = df.drop(['Email No.', 'Prediction'], axis=1, errors='ignore')
y = df['Prediction']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),  # Handle any missing values
    ('scaler', MinMaxScaler()),  # Scale frequencies to [0,1] range
    ('feature_selection', SelectKBest(chi2, k=100)),  # Select top 100 most important words
    ('classifier', RandomForestClassifier(
        n_estimators=100,
        class_weight='balanced',  # Handle class imbalance
        random_state=42))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print("=== Model Evaluation ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

feature_scores = pd.DataFrame({
    'feature': X_train.columns[pipeline.named_steps['feature_selection'].get_support()],
    'importance': pipeline.named_steps['classifier'].feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 20 Important Features:")
print(feature_scores.head(20))

new_email = pd.DataFrame(np.zeros((1, len(X.columns))), columns=X.columns)
new_email['the'] = 5
new_email['free'] = 3  # spam word
new_email['money'] = 2  # spam word

prediction = pipeline.predict(new_email)
print(f"\nNew email prediction: {'SPAM' if prediction[0] == 1 else 'NOT SPAM'}")