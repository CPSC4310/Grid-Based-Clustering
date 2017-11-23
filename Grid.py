from GridCell import *

class Grid:
    """A grid to represent density-based clustering"""

    def __init__(self, data, size, xAxis, yAxis, min_den):
        """Constructor for Grid class."""

        # Instance Variables
        self.data = data        # An array of data objects, each object keyed by its data attribute.
        self.size = size        # The size of the grid. Eg, size=5 will build a 5x5 grid.
        self.cells = []         # Contains the arrangement of grid cells.
        self.dense_cells = []   # An array of all dense cells contained in grid.
        self.min_den = min_den  # Minimum density for each cell.
        self.xAxis = xAxis      # Tuple containing attribute name and range of values for X-Axis of grid.
        self.yAxis = yAxis      # Tuple containing attribute name and range of values for Y-Axis of grid.

    def buildGrid(self):
        """Composes a 2-dimensional grid structure."""

        for y in range(self.size):
            row = []

            for x in range(self.size):
                min_y = self.yAxis[1][(self.size - y) - 1]
                max_y = self.yAxis[1][(self.size - y)]

                min_x = self.xAxis[1][(self.size - x) - 1]
                max_x = self.xAxis[1][(self.size - x)]

                cell = GridCell(self.min_den, [min_x, max_x], [min_y, max_y])
                row.append(cell)

            self.cells.append(row)

    def getDenseGrids(self):
        """Retrieves all cells that are equal or greater than the density threshold."""
        self.dense_cells = []

    def sortCells(self):
        """Sorts cell list in descending order."""
        return []



