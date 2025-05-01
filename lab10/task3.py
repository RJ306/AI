import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

df = pd.read_csv('student_performance_dataset.csv') 
features = ['Final_Exam_Score', 'Study_Hours_per_Week', 'Attendance_Rate']
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
for i in range(2, 7):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(2, 7), wcss, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

sil_score = silhouette_score(X_scaled, df['Cluster'])
print(f"Silhouette Score: {sil_score:.4f}")

plt.figure(figsize=(10, 6))
colors = ['red', 'blue', 'green', 'purple', 'orange']
for i in range(optimal_k):
    cluster_data = df[df['Cluster'] == i]
    plt.scatter(cluster_data['Study_Hours_per_Week'], 
                cluster_data['Final_Exam_Score'], 
                c=colors[i], 
                label=f'Cluster {i}')

plt.title('Student Clusters by Study Hours and Final Exam Score')
plt.xlabel('Weekly Study Hours')
plt.ylabel('Final Exam Score')
plt.legend()
plt.grid(True)
plt.show()

cluster_stats = df.groupby('Cluster').agg({
    'Final_Exam_Score': ['mean', 'std'],
    'Study_Hours_per_Week': ['mean', 'std'],
    'Attendance_Rate': ['mean', 'std'],
    'Student_ID': 'count'
})

print("\nCluster Characteristics:")
print(cluster_stats)
print("\nSample Student Cluster Assignments:")
print(df[['Student_ID', 'Cluster']].head(10))