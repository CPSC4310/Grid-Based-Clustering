from GridCell import *

class Grid:
    """A grid to represent density-based clustering"""

    def __init__(self, size, xAxis, yAxis):
        """Constructor for Grid class."""

        # Instance Variables
        self.size = size        # The size of the grid. Eg, size=5 will build a 5x5 grid.
        self.xAxis = xAxis      # Array containing range of values for X-Axis of grid.
        self.yAxis = yAxis      # Array containing range of values for Y-Axis of grid.
        self.cells = []         # Contains the arrangement of grid cells.
        self.dense_cells = []   # An array of all dense cells contained in grid.

    def buildGrid(self, min_den):
        """Composes a 2-dimensional grid structure."""
        for y in range(self.size):
            row = []

            for x in range(self.size):
                min_y = self.yAxis[(self.size - y) - 1]
                max_y = self.yAxis[(self.size - y)]

                min_x = self.xAxis[(self.size - x) - 1]
                max_x = self.xAxis[(self.size - x)]

                cell = GridCell(min_den, [min_x, max_x], [min_y, max_y], self.size - x, self.size - y)
                row.append(cell)

            self.cells.append(row)

    def addPoints(self, data, xAttr, yAttr):
        """Add data points to grid."""
        for point in data:
            for row in self.cells:
                for cell in row:
                    isInCell = cell.isWithinValueRange({ "x": point[xAttr], "y": point[yAttr] })

                    if isInCell:
                        cell.addItem(point)

    def getDenseCells(self):
        """Retrieves all cells that are equal or greater than the density threshold."""
        for row in self.cells:
            for cell in row:
                if cell.isDense():
                    self.dense_cells.append(cell)

    def sortCells(self):
        """Sorts cell list in descending order."""
        return []



