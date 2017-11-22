class Grid:
    """A grid to represent density-based clustering"""

    def __init__(self, data, height, width):
        """Constructor for Grid class."""

        # Instance Variables
        self.data = data        # An array of data objects, each object keyed by its data attribute.
        self.height = height    # The height, in # of cells, of the grid.
        self.width = width      # The width, in # of cells, of the grid.
        self.cells = []         # Contains the arrangement of grid cells.
        self.dense_cells = []

    def buildGrid(self):
        """Composes a 2-dimensional grid structure."""
        self.cells = []

    def getDenseGrids(self, min_den = 1):
        """Retrieves all cells that are equal or greater than the density threshold."""
        self.dense_cells = []

    def sortCells(self):
        """Sorts cell list in descending order."""
        return []



