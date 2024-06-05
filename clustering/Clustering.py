import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Sample data
df = pd.read_csv('obfuscated-login.csv', parse_dates=['Login Time'])

# Convert 'Login Time' to timestamp in seconds
df['Login Time'] = (df['Login Time'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

df.sort_values(by=['user', 'Login Time'], inplace=True)
# df.reset_index(drop = True)
df['Previous user'] = df['user'].shift(1)
df['Previous user Login'] = df['Login Time'].shift(1)
df.loc[(df['Previous user'] != df['user']), 'Previous user Login'] = pd.NA
df.drop(columns='Previous user', axis='columns', inplace=True)
df.drop(df[df['Previous user Login'].isna()].index, axis='rows', inplace=True)
df['user inter login time'] = df['Login Time'] - df['Previous user Login']

df.sort_values(by=['device', 'Login Time'], inplace=True)
# df.reset_index(drop = True)
df['Previous device'] = df['device'].shift(1)
df['Previous device Login'] = df['Login Time'].shift(1)
df.loc[(df['Previous device'] != df['device']), 'Previous device Login'] = pd.NA
df.drop(columns='Previous device', axis='columns', inplace=True)
df.drop(df[df['Previous device Login'].isna()].index, axis='rows', inplace=True)
df['device inter login time'] = df['Login Time'] - df['Previous device Login']


# Scale the data
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)
# clusters_backup = []
# for min_samples in range(1, 20):
#     for eps in np.arange(0.1, 1, 0.1):
#         print(f'eps:{eps} min_sample:{min_samples}')
#         # DBSCAN model
#         dbscan = DBSCAN(eps=0.5, min_samples=2)  # You may need to adjust eps and min_samples
#         clusters = dbscan.fit_predict(scaled_features)
#         clusters_backup.append(clusters.copy())
#         print(f'unique clusters:{len(np.unique(clusters))}')
# # Add cluster labels to DataFrame
# df['Cluster'] = clusters


# List of clustering algorithms
clustering_algorithms = [
    ("DBSCAN", DBSCAN(eps=0.5, min_samples=2)),
    ("Agglomerative", AgglomerativeClustering(n_clusters=2)),
    ("KMeans", KMeans(n_clusters=2)),
    ("Spectral", SpectralClustering(n_clusters=2, affinity='nearest_neighbors')),
    ("GMM", GaussianMixture(n_components=2))
]

# Evaluate each algorithm
for name, algorithm in clustering_algorithms:
    if name == "GMM":
        labels = algorithm.fit_predict(scaled_features)
    else:
        algorithm.fit(scaled_features)
        labels = algorithm.labels_

    silhouette_avg = silhouette_score(scaled_features, labels)
    print(f"{name} Silhouette Score: {silhouette_avg} number of labels:{len(np.unique(labels))}")

"""
Output:
C:\Code\SVMtest\.venv\Scripts\python.exe C:\Code\SVMtest\clustering\DBSCAN.py 
DBSCAN Silhouette Score: -0.5573803435972846 number of labels:309
Agglomerative Silhouette Score: 0.26005125860832445 number of labels:2
KMeans Silhouette Score: 0.29592561694161734 number of labels:2
Spectral Silhouette Score: 0.2918628975359127 number of labels:2
GMM Silhouette Score: 0.12180767882841641 number of labels:2
"""