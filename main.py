from Grid import *

data_set = []
attributes = []

file = './data/Iris_Data.csv'

########################
# FUNCTION DEFINITIONS #
########################

def partitionAttributes(values, partitionSize = 5):
    """Divide values equally according to the specified partition size."""

    rangeDistance = (max(values) - min(values)) / partitionSize

    ranges = [round(min(values) + ( x * rangeDistance), 2) for x in range(partitionSize)]
    ranges.append(max(values))

    return ranges

def parseValue(value):
    """Parses string values into floats, otherwise return origin string."""

    try:
        float(value)
        return float(value)
    except:
        return value

## Parse incoming data set into an array of dictionaries
f = open(file, 'r')
lines = f.read().split('\n')

attributes = lines[0].split(',')                    # List of data attributes.
valuesPerAttr = { attr: [] for attr in attributes } # Dictionary of all values per data attribute.

for idx, line in enumerate(lines):
    if idx > 0:
        item = {}
        row = line.split(',')

        for _idx, attr in enumerate(attributes):
            if len(row) == len(attributes):
                value = parseValue(row[_idx])

                item[attr] = value
                valuesPerAttr[attr].append(value)

        # Only add items with data in it.
        if bool(item):
            data_set.append(item)

gridSize = len(attributes)
xAxisRange = partitionAttributes(valuesPerAttr["petal_length"])
yAxisRange = partitionAttributes(valuesPerAttr["petal_width"])
min_den = 10

grid = Grid(gridSize, xAxisRange, yAxisRange)
grid.buildGrid(min_den)
grid.addPoints(data_set, "petal_length", "petal_width")
grid.getDenseCells()