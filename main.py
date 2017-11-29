from Grid import *
from parseCSV import csvToDictArray
import csv
import os

file = './data/Iris_Data.csv'

# Parse CSV file
parsedData = csvToDictArray(file)
data_set = parsedData[0]
attributes = parsedData[1]
valuesPerAttr = parsedData[2]
min_den = 10
gridSize = len(attributes)

def partitionAttributes(values, partitionSize = 5):
    """Divide values equally according to the specified partition size."""

    rangeDistance = (max(values) - min(values)) / partitionSize

    ranges = [round(min(values) + ( x * rangeDistance), 2) for x in range(partitionSize)]
    ranges.append(max(values))

    return ranges

def clusterTwoColumns(columnOneIdentifier, columnTwoIdentifier):
    # Build a grid for clustering against "petal_length" vs. "petal_width"
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

    # Perform some black magic. See equivalent in commented code below:
    data = [ item for key, cluster in clusters.items() for cell in cluster for item in cell.getCellItems() ]
    # data = []
    # for key, cluster in clusters.items():
    #     for cell in cluster:
    #         for item in cell.getCellItems():
    #             data.append(item)

    columns = [columnOneIdentifier, columnTwoIdentifier, "species"]

    outputFolder = "./output/"

    # Create the output directory if it doesn't already exist
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder, 0755)

    # Write clustered data to csv
    with open(outputFolder + columnOneIdentifier + "-VS-" + columnTwoIdentifier + "-Clusters.csv", 'wb') as f:
        dictWriter = csv.DictWriter(f, columns)
        dictWriter.writeheader()
        dictWriter.writerows(data)

# TODO: make this get the column identifiers from row 1 in the csv instead of hardcoded values
columnIdentifiers = ["sepal_width", "sepal_length", "petal_length", "petal_width"]

for i in range(len(columnIdentifiers)):
    for j in range(i+1, len(columnIdentifiers)):
        clusterTwoColumns(columnIdentifiers[i], columnIdentifiers[j])