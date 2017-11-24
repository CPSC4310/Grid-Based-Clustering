class GridCell:
    """Grid cell class"""

    # We create the density_threshold variable outside of the constructor
    # because we want to share this value amongst ALL instantiations of
    # the Grid Cell class.
    min_den = 1

    def __init__(self, min_den, xVals, yVals, xPos, yPos):
        """Constructor for Grid cell class."""

        # Instance Variables
        self.cluster = -1       # Cluster cell belongs to.
        self.items = []         # Array of objects contained in cell.
        self.min_den = min_den  # Minimum density of cell.
        self.xVals = xVals      # Tuple containing the minimum and maximum x-values for cell.
        self.yVals = yVals      # Tuple containing the minimum and maximum y-values for cell.
        self.xPos = xPos        # X-Position of the cell.
        self.yPos = yPos        # Y-Position of the cell.

    def isWithinValueRange(self, data):
        """Checks if an attribute value falls within the min and max value range of cell."""
        withinXRange = False
        withinYRange = False

        if data['x'] >= self.xVals[0] and data['x'] <= self.xVals[1]:
            withinXRange = True

        if data['y'] >= self.yVals[0] and data['y'] <= self.yVals[1]:
            withinYRange = True

        return withinXRange and withinYRange

    def addItem(self, item):
        """Adds item to cell."""
        self.items.append(item)

    def assignToCluster(self, cluster):
        """Assigns cell to a cluster"""
        self.cluster = cluster

    def getDensityCount(self):
        """Returns a count of the cell's density."""
        return len(self.items)

    def getPosition(self):
        """Returns a count of the cell's density."""
        return [self.xPos, self.yPos]

    def isAssignedToCluser(self):
        """Returns whether or not cell is assigned to cluster."""
        return self.cluster > 0

    def isDense(self):
        """Returns whether or not grid cell is dense."""
        return len(self.items) >= self.min_den

    def isAdjacentCell(self, cell):
        """Checks if the input dense-cell is adjacent to itself."""
        xPos = cell.getPosition()[0]
        yPos = cell.getPosition()[1]

        # Check if input cell is above cell
        if xPos == self.xPos and (yPos - 1) == self.yPos:
            return True

        # Check if input cell is below cell
        if xPos == self.xPos and (yPos + 1) == self.yPos:
            return True

        # Check if input cell is to the right of cell
        if (xPos - 1) == self.xPos and yPos == self.yPos:
            return True

        # Check if input cell is to the left of cell
        if (xPos + 1) == self.xPos and yPos == self.yPos:
            return True

        return False






