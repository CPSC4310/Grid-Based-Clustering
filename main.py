from Grid import *
from parseCSV import csvToDictArray
import csv

file = './data/Iris_Data.csv'

# Parse CSV file
parsedData = csvToDictArray(file)
data_set = parsedData[0]
attributes = parsedData[1]
valuesPerAttr = parsedData[2]

def partitionAttributes(values, partitionSize = 5):
    """Divide values equally according to the specified partition size."""

    rangeDistance = (max(values) - min(values)) / partitionSize

    ranges = [round(min(values) + ( x * rangeDistance), 2) for x in range(partitionSize)]
    ranges.append(max(values))

    return ranges

min_den = 10
gridSize = len(attributes)

# Build a grid for clustering against "petal_length" vs. "petal_width"
xAxisRange = partitionAttributes(valuesPerAttr["sepal_length"])
yAxisRange = partitionAttributes(valuesPerAttr["sepal_width"])

grid = Grid(gridSize, xAxisRange, yAxisRange)
grid.buildGrid(min_den)
grid.addPoints(data_set, "sepal_length", "sepal_width")

# Gather and sort dense cells.
grid.getDenseCells()
grid.sortDenseCells()

# Build clusters.
clusters = grid.mergeCells()
clusters = grid.mergeUncertainCells()

clusterData = [ gridCell.getCellItems() for key, cluster in clusters.items() for gridCell in cluster]
clusterData = [ item for cell in clusterData for item in cell]

## Write clustered data to csv

# with open('test.csv', 'wb') as f:
#     dictWriter = csv.DictWriter(f, attributes)
#     dictWriter.writeheader()
#     dictWriter.writerows(clusterData)
