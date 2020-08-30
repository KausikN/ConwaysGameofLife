'''
Simulation Utility Functions and Scripts
'''

# Imports
import numpy as np
from tqdm import tqdm

import GIFUtils

# Main Classes
class Cell:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos


class Grid:
    def __init__(self, cells, gridDim, gridParams):
        self.gridDim = gridDim
        self.gridParams = gridParams
        self.cellStructure = self.buildGrid(cells, gridDim)

    def buildGrid(self, cells, gridDim):
        cellStructure = None
        values = None
        if len(gridDim) == 3:
            # Build Initial 3D Grid
            cellStructure = [[[None]*gridDim[2]]*gridDim[1]]*gridDim[0]

            for i in range(gridDim[0]):
                for j in range(gridDim[1]):
                    for k in range(gridDim[2]):
                        cellStructure[i][j][k] = Cell(self.gridParams['DEAD_VALUE'], (i, j, k))

            # Fill with Input Cells
            for cell in cells:
                cellStructure[cell.pos[0]][cell.pos[1]][cell.pos[2]].value = cell.value

        elif len(gridDim) == 2:
            # Build Initial 2D Grid
            cellStructure = [[None]*gridDim[1]]*gridDim[0]

            for i in range(gridDim[0]):
                for j in range(gridDim[1]):
                    cellStructure[i][j] = Cell(self.gridParams['DEAD_VALUE'], (i, j))

            # Fill with Input Cells
            for cell in cells:
                cellStructure[cell.pos[0]][cell.pos[1]].value = cell.value
        
        return cellStructure


class Simulation:
    def __init__(self, grid, Rule, RuleParams):
        self.grid = grid
        self.rule = Rule
        self.rule_params = RuleParams
        self.curGen = 0

        self.grid_history = []
        self.recordGrid()

    def recordGrid(self):
        curGridValues = GetGridValues(self.grid)
        self.grid_history.append(curGridValues)

    def reset(self):
        self.curGen = 0
        self.grid = self.grid_history[0]
        self.grid_history = []
        self.recordGrid()

    def run(self, n_gens, progressBarDisable=False):
        for gen in tqdm(range(n_gens), disable=progressBarDisable):
            self.curGen += 1
            self.grid = self.rule(self.grid, self.rule_params)
            self.recordGrid()
            

# Main Functions
def CreateGrid(size, livelocs=[], gridParams={"LIVE_VALUE": 1, "DEAD_VALUE": 0}):
    liveCells = []
    for loc in livelocs:
        liveCells.append(Cell(gridParams['LIVE_VALUE'], (loc[0], loc[1])))

    return Grid(liveCells, size, gridParams)

def GetGridValues(grid):
    curGridValues = None
    if len(grid.gridDim) == 3:
        curGridValues = [[[None]*grid.gridDim[2]]*grid.gridDim[1]]*grid.gridDim[0]
        for i in range(grid.gridDim[0]):
            for j in range(grid.gridDim[1]):
                for k in range(grid.gridDim[2]):
                    curGridValues[i][j][k] = grid.cellStructure[i][j][k].value
    elif len(grid.gridDim) == 2:
        curGridValues = [[None]*grid.gridDim[1]]*grid.gridDim[0]
        for i in range(grid.gridDim[0]):
            for j in range(grid.gridDim[1]):
                curGridValues[i][j] = grid.cellStructure[i][j].value
                
    return curGridValues

def Grid2Image_GreyScale(gridData):
    gridData = np.array(gridData)
    I = np.array(gridData*255, dtype=np.uint8)
    return I


# Rule Functions
def RuleFunc_StandardConwayRules2D(grid, params):
    initial_grid = GetGridValues(grid)
    # 1. Any live cell with two or three live neighbours survives.
    # 2. Any dead cell with three live neighbours becomes a live cell.
    # 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    for i in range(grid.gridDim[0]):
        for j in range(grid.gridDim[1]):
            liveCount = 0
            TopLeftPoint = [i - int(params['WINDOW_SIZE'][0]/2), j - int(params['WINDOW_SIZE'][1]/2)]
            for wi in range(params['WINDOW_SIZE'][0]):
                for wj in range(params['WINDOW_SIZE'][1]):
                    curPoint = [TopLeftPoint[0] + wi, TopLeftPoint[1] + wj]
                    if curPoint[0] == i and curPoint[1] == j:
                        continue
                    if curPoint[0] >= grid.gridDim[0] or curPoint[0] < 0:
                        continue
                    if curPoint[1] >= grid.gridDim[1] or curPoint[1] < 0:
                        continue
                    if not grid.gridParams['CheckEqual'](initial_grid[curPoint[0]][curPoint[1]], grid.gridParams['DEAD_VALUE']):
                        liveCount += 1
                # 1
                livePart = liveCount / ((params['WINDOW_SIZE'][0]*params['WINDOW_SIZE'][1])-1)
                if grid.gridParams['CheckEqual'](initial_grid[i][j], grid.gridParams['LIVE_VALUE']) and livePart >= (2/8) and livePart <= (3/8):
                    grid.cellStructure[i][j].value = grid.gridParams['LIVE_VALUE']
                # 2
                elif grid.gridParams['CheckEqual'](initial_grid[i][j], grid.gridParams['DEAD_VALUE']) and int(livePart) == int(3/8):
                    grid.cellStructure[i][j].value = grid.gridParams['LIVE_VALUE']
                # 3
                else:
                    grid.cellStructure[i][j].value = grid.gridParams['DEAD_VALUE']

    return grid

# Check Functions
def CheckEqual_Basic(a, b):
    # Check if list or similar
    if type(a) in [list, tuple, set]:
        if not len(a) == len(b):
            return False
        for i in range(len(a)):
            if not a[i] == b[i]:
                return False
    
    # Check if dict
    if type(a) in [dict]:
        for k in a.keys():
            if not k in b.keys():
                return False
            if not a[k] == b[k]:
                return False
    
    # Other Check
    if not a == b:
        return False

    return True

# Driver Code
# Params
Grid_Size = [10, 10]
Live_Cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
Grid_Parameters = {
    "DEAD_VALUE": 0, 
    "LIVE_VALUE": 1, 
    "CheckEqual": CheckEqual_Basic
}

Rule_Func = RuleFunc_StandardConwayRules2D
Rule_Parameters = {
    "WINDOW_SIZE": [3, 3]
}

N_Generations = 1000

progressBar = True
delay = 1

savePath = 'sim.gif'
fps = 25

# Form grid and Simulate
grid = CreateGrid(Grid_Size, Live_Cells, Grid_Parameters)
sim = Simulation(grid, Rule_Func, Rule_Parameters)

sim.run(N_Generations, not progressBar)

# Form Images and Save and Display GIF
GridImages = []
for gridData in sim.grid_history:
    GridImages.append(Grid2Image_GreyScale(gridData))

GIFUtils.SaveImageSequence(GridImages, savePath, 'gif', fps=fps)
GIFUtils.DisplayImageSequence(GridImages, delay, gray=True)