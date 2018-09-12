# GeoLocationClustering
K-means is an unsupervised, clustering algorithm that groups a given dataset into k clusters based on a provided similarity measure such as euclidean distance, great-circle distance, or cosine similarity. The similarity measure used depends on the domain and context of the dataset, especially when working with real-world application. In our case, we are implementing a geo-location clustering from dataset with latitude-longitude pairs. The results will be displayed on the map of the world to visualize the distribution of the clusters. Considering the sphere shape of the earth, we will be using the great-circle distance as our similarity measure. We will also use the euclidean distance for comparison.
Generally, the problem that k-means tries to solve is as follows: Given a dataset D= {x1, x2, ..., xn}, a similarity measure {sim(xi, xj)for xi, xj ∈D},
and an integer k, we want to define a mapping f : D –> {1, 2, ..., k}, so that
- each xi is assigned to a cluster Cl, l ∈ {1, 2, ..., k}
- sim(xu, xv) > sim(xu, xw), for any xu and xv belong to the same cluster and any xu and xw belong to different clusters. 
-NOTE: In our case xi would be a latitude-longitude pair

Approach
The clustering approach that we decided to go with is adding all the points in a particular cluster, then adjusting the cluster points based on what the cluster averages are. In order to do this, we first import the original data into an RDD. This RDD contains the latitude and longitude for each respective point. Since there are hundreds of thousands of points, this points RDD needs to be persisted into memory in order to speed up execution. In order to get the program started, we decided to take a sample of k random points and assign it to a centroids RDD. Even though there is a chance that the sampled points could be similar, we trust that our algorithm will eventually balance out the points. This is since during our convergence calculation in which the distance will start to go down but then increase out of nowhere before decreasing down again to 0.1. Next, we obtain the k value and the measure (Euclidean or Great Circle Distance) that a user wanted to do. Based on the instructions, we set the converge distance to 0.1 and use an arbitrary value of 1.0 to have an initial distance to work with.

In a continual while loop that only stops when the mean distance between the old and new cen- troids is less than 0.1, we create a new RDD that contains the points and which cluster each point is assigned to. After that, a reduceByKey() operation is performed in which all the points within the same cluster are in the same row. The new centroids are then obtained after mapping an average of all the points in each respective cluster. To determine if there is a convergence, we get the old centroids and the new centroids and then calculate either the Euclidean or Great Circle distance between them. Lastly, we set the new centroids into the centroids RDD and repeated the process all over again.

After the centroids have converged, we then print out the final values and then store the points 1
for a particular cluster inside a folder to be further analyzed.

Our prediction:
Persisting the RDD for the original data points in memory will save a lot of execution time since that RDD won’t be recomputed for each iteration.

The following is a high-level pseudo code for our algorithm for 5 clusters:

    k = 5; keepGoing = true;
    Pick k "random" points for centroids from dataset 
    while(keepGoing):


        for every remaining point:
            compare distance to each centroid
            assign point to cluster with smallest distance recalculate the centroid for each cluster
            if difference between old and new centroids < 0.01:
                keepGoing = false;
