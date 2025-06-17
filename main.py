import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# fetch dataset
wholesale_customers = fetch_ucirepo(id=292)

# data (as pandas dataframes)
X = wholesale_customers.data.features
y = wholesale_customers.data.targets

# scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# apply PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# determine the number of components
explained_variance = pca.explained_variance_ratio_
cumulative_variance = explained_variance.cumsum()
n_components = 0
for i, var in enumerate(cumulative_variance):
    if var >= 0.95:
        n_components = i + 1
        break

print(f'Number of components needed to capture 95% of the variance: {n_components}')

# plot the explained variance
plt.figure(figsize=(8, 6))
plt.plot(explained_variance, label='Explained Variance')
plt.plot(cumulative_variance, label='Cumulative Variance')
plt.xlabel('Principal Components')
plt.ylabel('Variance')
plt.title('Screen Plot')
plt.legend()
plt.show()

# find the optimal number of clusters
silhouette = []
inertia = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_pca[:, :n_components])
    silhouette.append(silhouette_score(X_pca[:, :n_components], kmeans.labels_))
    inertia.append(kmeans.inertia_)

optimal_k = silhouette.index(max(silhouette)) + 2
print(f'Optimal number of clusters: {optimal_k}')

# plot the silhouette score and inertia
plt.figure(figsize=(8, 6))
plt.plot(range(2, 11), silhouette, label='Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score Plot')
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(range(2, 11), inertia, label='Inertia')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Inertia Plot')
plt.legend()
plt.show()

# create KMeans model with optimal number of clusters
kmeans_raw = KMeans(n_clusters=optimal_k)
kmeans_raw.fit(X_scaled)

kmeans_pca = KMeans(n_clusters=optimal_k)
kmeans_pca.fit(X_pca[:, :n_components])

# evaluate the models
silhouette_raw = silhouette_score(X_scaled, kmeans_raw.labels_)
silhouette_pca = silhouette_score(X_pca[:, :n_components], kmeans_pca.labels_)

print(f'Silhouette score on raw data: {silhouette_raw}')
print(f'Silhouette score on PCA-reduced data: {silhouette_pca}')

# visualize the clusters
pca_2d = PCA(n_components=2)
X_pca_2d = pca_2d.fit_transform(X_scaled)
kmeans_2d = KMeans(n_clusters=optimal_k)
kmeans_2d.fit(X_pca_2d)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], c=kmeans_2d.labels_)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Cluster Visualization')
plt.show()

# examine the components
print('PC1 is most strongly correlated with:')
print(X.columns[abs(pca_2d.components_[0]).argsort()[::-1][:3]])

print('PC2 is most strongly correlated with:')
print(X.columns[abs(pca_2d.components_[1]).argsort()[::-1][:3]])

# analyze the clusters
for cluster in range(optimal_k):
    cluster_data = X_scaled[kmeans_raw.labels_ == cluster]
    print(f'Cluster {cluster} characteristics:')
cluster_df = pd.DataFrame(cluster_data, columns=X.columns)
print(f'Cluster {cluster} characteristics:')
print(cluster_df.describe())