import sys
import numpy
from geopy.distance import great_circle
from pyspark import SparkContext
from pyspark import SparkConf


def euclideanDistance(point1, point2):
  return numpy.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def closestPoint(point, centroids, formula):
  closestIndex = 0
  closestDist = float("+inf")

  for i in range(len(centroids)):
    if formula == "euclidean":
      currentDist = euclideanDistance(point, centroids[i])
    else:
      currentDist = great_circle(point, centroids[i]).miles

    if currentDist < closestDist:
      closestDist = currentDist
      closestIndex = i
  return closestIndex

def addPoints(point1, point2):
  return (point1[0] + point2[0], point1[1] + point2[1])

def getCentroidDifference(oldCentroids, newCentroids, formula):
  if formula == "euclidean":
    answer = numpy.mean([euclideanDistance(oldCentroids[index], newPoint) for (index, newPoint) in newCentroids])
  else:
    answer = numpy.mean([great_circle(oldCentroids[index], newPoint) for (index, newPoint) in newCentroids])

  return answer

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print >> sys.stderr, "Usage: KMeans <file> <euclidean or greatCircle> <k>"
    exit(-1)

  sc = SparkContext()

  data = sc.textFile(sys.argv[1]).map(lambda abc: abc.split(',')).map(lambda fields: numpy.array([float(fields[0]), float(fields[1])])).persist()
  
  measure = sys.argv[2]
  k = int(sys.argv[3])
  centroids = data.takeSample(False, k)
  print str(centroids)
  currentDist = 1.0
  convergeDist = 0.1

  while currentDist > convergeDist:
	clusteredPts = data.map(lambda point: (closestPoint(point, centroids, measure), (point, 1)))
	clusters = clusteredPts.reduceByKey(addPoints)

	# Recalculate centroids
	newCentroids = clusters.map(lambda pt: (pt[0], pt[1][0]/pt[1][1])).collect()

	# Determine if there's a convergence yet
	currentDist = getCentroidDifference(centroids, newCentroids, measure)

	print currentDist

	# Set new centroids
	for (index, newPoint) in newCentroids:
		centroids[index] = newPoint

  print "Final Centers:"
  for point in centroids:
	print str(point)

  #Save clusters
  for i in range(len(centroids)):
    cluster = clusteredPts.filter(lambda num: num[0] == i)
    cluster = cluster.map(lambda field: str(field[0]) + "," + str(field[1][0][0]) + "," + str(field[1][0][1])) # saves as format: cluster#,lat,lon

    cluster.saveAsTextFile("file:/home/training/final_project/cluster" + str(i))
