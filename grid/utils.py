import math

def clusterMeans(cluster):
    """Calculates cluster mean."""

    xVal = sum([ point[0] for point in cluster ]) / len(cluster)
    yVal = sum([point[1] for point in cluster]) / len(cluster)

    return [xVal, yVal]


def eucideanDistance(obj1, obj2):
    """ Euclidean distance calculation between two objects."""
    xDissimilarity = (float(obj1[0] - float(obj2[0])))**2
    yDissimilarity = (float(obj1[1] - float(obj2[1])))**2

    return math.sqrt(xDissimilarity + yDissimilarity)


def calculate_a_AvgDistance(_object, aObjects):
    xPos = _object[0]
    yPos = _object[1]

    distances = [ eucideanDistance(_object, point) for point in aObjects  ]

    return sum(distances) / max(len(aObjects), 1)

def calculate_b_AvgDistance(_object, aObjects):
    xPos = _object[0]
    yPos = _object[1]

    distances = [eucideanDistance(_object, point) for point in aObjects]

    return min(distances)

def silhouette_coefficient(_object, acluster, bClusters):
    """ Calculates the silhouette coefficient of a single cluster object."""

    # Calculate the average distance between input object and all other objects in containing cluster.
    avgADist = calculate_a_AvgDistance(_object, acluster)

    # Calculate the average distance between input object and all other clusters it does not belong to.
    avgbDist = calculate_b_AvgDistance(_object, bClusters)

    return (avgbDist - avgADist) / (max(avgADist, avgbDist))
