data_set = []
attributes = []

file = './data/Iris_Data.csv'

########################
# FUNCTION DEFINITIONS #
########################

def partitionAttributes(values, partitionSize = 5):
    """Divide values equally according to the specified partition size."""


## Parse incoming data set into an array of dictionaries
f = open(file, 'r')
lines = f.read().split('\n')
attributes = lines[0].split(',')

for idx, line in enumerate(lines):
    if idx > 0:
        item = {}
        row = line.split(',')

        for _idx, attr in enumerate(attributes):
            if len(row) == len(attributes):
                item[attr] = row[_idx]

        # Only add items with data in it.
        if bool(item):
            data_set.append(item)
