# GeoLocationClustering
K-means is an unsupervised, clustering algorithm that groups a given dataset into k clusters based on a provided similarity measure such as euclidean distance, great-circle distance, or cosine similarity. The similarity measure used depends on the domain and context of the dataset, especially when working with real-world application. In our case, we are implementing a geo-location clustering from dataset with latitude-longitude pairs. The results will be displayed on the map of the world to visualize the distribution of the clusters. Considering the sphere shape of the earth, we will be using the great-circle distance as our similarity measure. We will also use the euclidean distance for comparison.
Generally, the problem that k-means tries to solve is as follows: Given a dataset D= {x1, x2, ..., xn}, a similarity measure {sim(xi, xj)for xi, xj ∈D},
and an integer k, we want to define a mapping f : D –> {1, 2, ..., k}, so that
- each xi is assigned to a cluster Cl, l ∈ {1, 2, ..., k}
- sim(xu, xv) > sim(xu, xw), for any xu and xv belong to the same cluster and any xu and xw belong to different clusters. 
-NOTE: In our case xi would be a latitude-longitude pair
