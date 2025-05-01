import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score

data = {
    'vehicle_serial_no': [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
    'mileage': [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000, 75000, 280000],
    'fuel_efficiency': [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
    'maintenance_cost': [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
    'vehicle_type': ['SUV', 'Sedan', 'Truck', 'Hatchback', 'Sedan', 'Truck', 'SUV', 'Truck', 'Hatchback', 'SUV']
}

df = pd.DataFrame(data)

X = df.drop('vehicle_serial_no', axis=1)
le = LabelEncoder()
X['vehicle_type'] = le.fit_transform(X['vehicle_type'])
wcss = []
for i in range(1, 6):  
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 6), wcss, marker='o')
plt.title('Elbow Method (Without Scaling)')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
kmeans_unscaled = KMeans(n_clusters=3, init='k-means++', random_state=42)
y_unscaled = kmeans_unscaled.fit_predict(X)

sil_unscaled = silhouette_score(X, y_unscaled)
print(f"Silhouette Score (Unscaled): {sil_unscaled:.4f}")

#selective feature scaling #
X_scaled = X.copy()
scaler = StandardScaler()
cols_to_scale = ['mileage', 'fuel_efficiency', 'maintenance_cost']
X_scaled[cols_to_scale] = scaler.fit_transform(X_scaled[cols_to_scale])

wcss_scaled = []
for i in range(1, 6):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss_scaled.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 6), wcss_scaled, marker='o')
plt.title('Elbow Method (With Selective Scaling)')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans_scaled = KMeans(n_clusters=3, init='k-means++', random_state=42)
y_scaled = kmeans_scaled.fit_predict(X_scaled)

sil_scaled = silhouette_score(X_scaled, y_scaled)
print(f"Silhouette Score (Scaled): {sil_scaled:.4f}")

df['Cluster_Unscaled'] = y_unscaled
df['Cluster_Scaled'] = y_scaled

def cluster_stats(df, cluster_col):
    stats = df.groupby(cluster_col).agg({
        'vehicle_type': lambda x: x.mode()[0],
        'mileage': ['mean', 'std'],
        'fuel_efficiency': ['mean', 'std'],
        'maintenance_cost': ['mean', 'std']
    })
    return stats

print("\nCluster Characteristics (Unscaled):")
print(cluster_stats(df, 'Cluster_Unscaled'))

print("\nCluster Characteristics (Scaled):")
print(cluster_stats(df, 'Cluster_Scaled'))

plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)
for i in range(3):
    plt.scatter(df[df['Cluster_Unscaled'] == i]['mileage'], 
                df[df['Cluster_Unscaled'] == i]['maintenance_cost'], 
                label=f'Cluster {i}')
plt.title('Clusters Without Scaling\n(Mileage vs Maintenance Cost)')
plt.xlabel('Mileage')
plt.ylabel('Maintenance Cost')
plt.legend()

plt.subplot(1, 2, 2)
for i in range(3):
    plt.scatter(df[df['Cluster_Scaled'] == i]['mileage'], 
                df[df['Cluster_Scaled'] == i]['maintenance_cost'], 
                label=f'Cluster {i}')
plt.title('Clusters With Selective Scaling\n(Mileage vs Maintenance Cost)')
plt.xlabel('Mileage')
plt.ylabel('Maintenance Cost')
plt.legend()

plt.tight_layout()
plt.show()

print("\nComplete Cluster Assignments:")
print(df[['vehicle_serial_no', 'vehicle_type', 'Cluster_Unscaled', 'Cluster_Scaled']])