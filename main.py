from Grid import *
from parseCSV import csvToDictArray
from utils import silhouette_coefficient, clusterMeans
import csv
import os

def partitionAttributes(values, partitionSize = 5):
    """Divide values equally according to the specified partition size."""

    rangeDistance = (max(values) - min(values)) / (partitionSize + 1)

    ranges = [round(min(values) + ( x * rangeDistance), 2) for x in range(partitionSize)]
    ranges.append(max(values))

    return ranges

def clusterTwoColumns(columnOneIdentifier, columnTwoIdentifier):
    # Build a grid for clustering against columnOneIdentifier vs. columnTwoIdentifier
    xAxisRange = partitionAttributes(valuesPerAttr[columnOneIdentifier])
    yAxisRange = partitionAttributes(valuesPerAttr[columnTwoIdentifier])

    data = [ { columnOneIdentifier: item[columnOneIdentifier], columnTwoIdentifier: item[columnTwoIdentifier], "species": item["species"] } for item in data_set ]

    grid = Grid(gridSize, xAxisRange, yAxisRange)
    grid.buildGrid(min_den)
    grid.addPoints(data, columnOneIdentifier, columnTwoIdentifier)

    # Gather and sort dense cells.
    grid.getDenseCells()
    grid.sortDenseCells()

    # Build clusters.
    clusters = grid.mergeCells()
    clusters = grid.mergeUncertainCells()

    # Flatten data set. See equivalent in commented code below:
    data = [ item for key, cluster in clusters.items() for cell in cluster for item in cell.getCellItems() ]
    # data = []
    # for key, cluster in clusters.items():
    #     for cell in cluster:
    #         for item in cell.getCellItems():
    #             data.append(item)

    # Gather clustering results.
    columns = [columnOneIdentifier, columnTwoIdentifier, "species"]

    outputFolder = "./output/"
    evalFolder = outputFolder + "eval/"
    perClusterFolder = outputFolder + "perCluster/"

    # Create the output directory if it doesn't already exist
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder, 0755)
        os.mkdir(evalFolder, 0755)
        os.mkdir(perClusterFolder, 0755)

    # Write evaluation results for each cluster.
    itemPointsPerCluster = {}

    for key, cluster in clusters.items():
        itemPointsPerCluster[key] = []

        for cell in cluster:
            points = [ [items["xVal"], items["yVal"]] for items in cell.getCellItems() ]
            itemPointsPerCluster[key] = points

        # Write per cluster data to csv
        data_c = [{columnOneIdentifier: item[columnOneIdentifier], columnTwoIdentifier: item[columnTwoIdentifier],
                   "species": item["species"]} for cell in cluster for item in cell.getCellItems()]
        with open(perClusterFolder + columnOneIdentifier + "-VS-" + columnTwoIdentifier + "_cluster_" + str(key) + ".csv", 'wb') as f:
            dictWriter = csv.DictWriter(f, columns)
            dictWriter.writeheader()
            dictWriter.writerows(data_c)

    # Execute evaluation strategy (finding average Silhouette Coefficient per cluster).
    cMeans = { key: clusterMeans(cluster) for key, cluster in itemPointsPerCluster.items() }
    evalsPerCluster = []
    for key, cluster in itemPointsPerCluster.items():
        avgSCs = []
        for idx, point in enumerate(cluster):
            pointsInsideCluster = []
            otherClusters = []

            for _idx, c in enumerate(cluster):
                if idx != _idx:
                    pointsInsideCluster.append(c)

            for _key, _c in cMeans.items():
                if key != _key:
                    otherClusters.append(_c)

            avgSCs.append(silhouette_coefficient(point, pointsInsideCluster, otherClusters))
        evalsPerCluster.append(["Cluster Number: " + str(key), "Silhouette Coefficient: " + str(sum(avgSCs) / len(avgSCs))])

    # Write evaluation results to "evals/".
    f = open(evalFolder + columnOneIdentifier + "_" + columnTwoIdentifier + ".txt", 'w')
    f.write(',\n'.join((str(s[0]) + ", " + (str(s[1]))) for s in evalsPerCluster))

    # Write overall clustered data to csv.
    data_t = [{columnOneIdentifier: item[columnOneIdentifier],
               columnTwoIdentifier: item[columnTwoIdentifier], "species": item["species"]} for item in data]
    with open(outputFolder + columnOneIdentifier + "-VS-" + columnTwoIdentifier + "-Clusters.csv", 'wb') as f:
        dictWriter = csv.DictWriter(f, columns)
        dictWriter.writeheader()
        dictWriter.writerows(data_t)

##############
#   MAIN     #
##############
file = './data/Iris_Data.csv'

# Parse CSV file
parsedData = csvToDictArray(file)
data_set = parsedData[0]
attributes = parsedData[1]
valuesPerAttr = parsedData[2]
min_den = 10
gridSize = len(attributes)

# Execute clustering strategy.
for i in range(len(attributes)-1):
    for j in range(i+1, len(attributes)-1):
        clusterTwoColumns(attributes[i], attributes[j])
