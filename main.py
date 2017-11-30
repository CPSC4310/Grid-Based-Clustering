from clusterData import clusterTwoColumns
from parseCSV import csvToDictArray

file = './data/Iris_Data.csv'

# Parse CSV file
parsedData = csvToDictArray(file)
attributes = parsedData[1]
min_den = 10
gridSize = len(attributes)

# Execute clustering strategy.
for i in range(len(attributes)-1):
    for j in range(i+1, len(attributes)-1):
        clusterTwoColumns(attributes[i], attributes[j], parsedData, min_den, gridSize)
