import operator
from GridCell import *

class Grid:
    """A grid to represent density-based clustering"""

    def __init__(self, size, xAxis, yAxis):
        """Constructor for Grid class."""

        # Instance Variables
        self.size = size            # The size of the grid. Eg, size=5 will build a 5x5 grid.
        self.xAxis = xAxis          # Array containing range of values for X-Axis of grid.
        self.yAxis = yAxis          # Array containing range of values for Y-Axis of grid.
        self.cells = []             # Contains the arrangement of grid cells.
        self.dense_cells = []       # An array of all dense grid cells that meet the min_den threshold.
        self.uncertain_cells = []   # An array containing all dense grid cells that do not meet min_den threshold.
        self.clusters = {}          # Dictionary containing clusters and their cell items.

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
        """Retrieves all cells with a density."""
        for row in self.cells:
            for cell in row:
                if cell.isDense():
                    # Append cells with densities greater or equal to min_den to dense_cells.
                    self.dense_cells.append(cell)
                elif cell.getDensityCount():
                    # If min_den is not met, append cell to uncertain_cells.
                    self.uncertain_cells.append(cell)

    def getCellAtPosition(self, x, y):
        """Retrieves cell at specified x,y position."""
        try:
            cell = self.cells[y][x]
            return cell
        except:
            return None

    def sortDenseCells(self):
        """Sorts dense cell list in descending order."""
        self.dense_cells = sorted(self.dense_cells, key=operator.methodcaller("getDensityCount"), reverse=True)

    def mergeCells(self):
        """Iterates through list of sorted dense cells and merges direct-density-reachable cells."""
        clusterCount = 1
        cells = self.dense_cells
        for cell in cells:
            cell.assignToCluster(clusterCount)

            self.clusters[clusterCount] = []
            self.clusters[clusterCount].append(cell)

            for _, _cell in enumerate(self.dense_cells[clusterCount:len(self.dense_cells)]):

                if cell.isAdjacentCell(_cell) and not _cell.isAssignedToCluster():
                    _cell.assignToCluster(clusterCount)
                    self.clusters[clusterCount].append(_cell)
                    self.dense_cells.remove(_cell)
                    
            clusterCount += 1

        return self.clusters

    def mergeUncertainCells(self):
        """Checks uncertain cells and merges them with their direct-density-reachable neighbour's cluster."""

        for cell in self.uncertain_cells:

            potentialClusters = []
            adjCells = []

            xPos = cell.getPosition()[0]
            yPos = cell.getPosition()[1]

            # Up
            if self.getCellAtPosition(xPos, yPos - 1):
                adjCell = self.getCellAtPosition(xPos, yPos - 1)

                if adjCell.isAssignedToCluster():
                    adjCells.append(adjCell)

                    clusterIdx = adjCell.getCellCluster()
                    potentialClusters.append(self.clusters[clusterIdx])

            # Down
            if self.getCellAtPosition(xPos, yPos + 1):
                adjCell = self.getCellAtPosition(xPos, yPos + 1)

                if adjCell.isAssignedToCluster():
                    adjCells.append(adjCell)

                    clusterIdx = adjCell.getCellCluster()
                    potentialClusters.append(self.clusters[clusterIdx])

            # Left
            if self.getCellAtPosition(xPos - 1, yPos):
                adjCell = self.getCellAtPosition(xPos - 1, yPos)

                if adjCell.isAssignedToCluster():
                    adjCells.append(adjCell)

                    clusterIdx = adjCell.getCellCluster()
                    potentialClusters.append(self.clusters[clusterIdx])

            # Right
            if self.getCellAtPosition(xPos + 1, yPos):
                adjCell = self.getCellAtPosition(xPos + 1, yPos)

                if adjCell.isAssignedToCluster():
                    adjCells.append(adjCell)

                    clusterIdxk = adjCell.getCellCluster()
                    potentialClusters.append(self.clusters[clusterIdx])

            if len(adjCells) == 1:
                clusterIdx = adjCells[0].getCellCluster()
                self.clusters[clusterIdx].append(cell)
                self.uncertain_cells.remove(cell)
            elif len(adjCells) > 1:
                # TODO
                print "TODO Adjacent Cells: ", adjCells
                
        return self.clusters
