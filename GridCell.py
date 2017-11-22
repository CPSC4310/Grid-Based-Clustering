class GridCell:
    """Grid cell class"""

    # We create the density_threshold variable outside of the constructor
    # because we want to share this value amongst ALL instantiations of
    # the Grid Cell class.
    min_den = 1

    def __init__(self, items, min_den):
        """Constructor for Grid class."""

        # Instance Variables
        self.cluster = -1       # Cluster cell belongs to.
        self.items = items      # Array of objects contained in cell.
        self.min_den = min_den  # Minimum density of cell.

    def addItem(self, item):
        """Adds item to cell."""

        self.items.append(item)

    def getDensity(self):
        """Returns whether or not grid cell is dense."""

        return len(self.items) >= self.min_den
