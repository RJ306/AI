import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score


df = pd.read_csv('Mall_Customers.csv')

X = df.drop('CustomerID', axis=1)

le = LabelEncoder()
X['Gender'] = le.fit_transform(X['Gender'])

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Method (Without Scaling)')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans_unscaled = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_unscaled = kmeans_unscaled.fit_predict(X)

sil_unscaled = silhouette_score(X, y_unscaled)
print(f"Silhouette Score (Unscaled): {sil_unscaled:.4f}")

#selective feature scaling (all features except Age) 

X_scaled = X.copy()

scaler = StandardScaler()

cols_to_scale = ['Gender', 'Annual Income (k$)', 'Spending Score (1-100)']
X_scaled[cols_to_scale] = scaler.fit_transform(X_scaled[cols_to_scale])

wcss_scaled = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss_scaled.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss_scaled, marker='o')
plt.title('Elbow Method (With Selective Scaling)')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans_scaled = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_scaled = kmeans_scaled.fit_predict(X_scaled)

sil_scaled = silhouette_score(X_scaled, y_scaled)
print(f"Silhouette Score (Scaled): {sil_scaled:.4f}")


df['Cluster_Unscaled'] = y_unscaled
df['Cluster_Scaled'] = y_scaled

def cluster_stats(df, cluster_col):
    stats = df.groupby(cluster_col).agg({
        'Gender': lambda x: x.mode()[0],
        'Age': 'mean',
        'Annual Income (k$)': 'mean',
        'Spending Score (1-100)': 'mean'
    })
    return stats

print("\nCluster Characteristics (Unscaled):")
print(cluster_stats(df, 'Cluster_Unscaled'))

print("\nCluster Characteristics (Scaled):")
print(cluster_stats(df, 'Cluster_Scaled'))

plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)
for i in range(5):
    plt.scatter(df[df['Cluster_Unscaled'] == i]['Annual Income (k$)'], 
                df[df['Cluster_Unscaled'] == i]['Spending Score (1-100)'], 
                label=f'Cluster {i}')
plt.title('Clusters Without Scaling')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()

plt.subplot(1, 2, 2)
for i in range(5):
    plt.scatter(df[df['Cluster_Scaled'] == i]['Annual Income (k$)'], 
                df[df['Cluster_Scaled'] == i]['Spending Score (1-100)'], 
                label=f'Cluster {i}')
plt.title('Clusters With Selective Scaling')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()

plt.tight_layout()
plt.show()