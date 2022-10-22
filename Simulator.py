"""
Conways Game of Life Simulator
"""

# Imports
import cv2
import time
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from Utils.GIFUtils import *

# Main Classes
class Cell:
    '''
    Cell
    '''
    def __init__(self, value, pos, **params):
        self.value = value
        self.pos = list(pos)
        self.__dict__.update(**params)

    def copy(self):
        '''
        Copy Cell
        '''
        return Cell(**self.__dict__)

class Grid:
    '''
    Grid
    '''
    def __init__(self, cell_matrix, **params):
        self.cell_matrix = np.array(cell_matrix)
        self.shape = self.cell_matrix.shape
        self.dim = len(self.shape)
        self.__dict__.update(**params)

    def updateGridCells(self, update_cells, **params):
        '''
        Update Grid Cells
        '''
        if self.dim == 3:
            for cell in update_cells:
                self.cell_matrix[cell.pos[0], cell.pos[1], cell.pos[2]] = cell
        elif self.dim == 2:
            for cell in update_cells:
                self.cell_matrix[cell.pos[0], cell.pos[1]] = cell

    def getImage(self, **params):
        '''
        Get Image from Grid
        '''
        I = np.zeros(self.shape, dtype=float)
        if self.dim == 3:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    for k in range(self.shape[2]):
                        I[i, j, k] = float(self.cell_matrix[i, j, k].value)
            I = np.mean(I, axis=-1)
        elif self.dim == 2:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    I[i, j] = float(self.cell_matrix[i, j].value)

        return I

    def copy(self):
        '''
        Copy Grid
        '''
        # Make Copy of Cells
        cell_matrix_copy = np.empty(self.shape, dtype=object)
        if self.dim == 3:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    for k in range(self.shape[2]):
                        cell_matrix_copy[i, j, k] = self.cell_matrix[i, j, k].copy()
        elif self.dim == 2:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    cell_matrix_copy[i, j] = self.cell_matrix[i, j].copy()
        # Update Values
        params = dict(self.__dict__)
        params.update({"cell_matrix": cell_matrix_copy})

        return Grid(**params)

class Simulation:
    '''
    Simulation
    '''
    def __init__(self, grid, funcs, n_iterations, **params):
        self.grid = grid
        self.funcs = funcs
        self.n_iterations = n_iterations
        self.__dict__.update(**params)
        # Session Params
        self.current = {
            "step": 0,
            "image": self.grid.getImage(),
            "exec_time": 0
        }
        self.history = [self.getCurrentState()]

    def step(self):
        '''
        Step Simulation
        '''
        # Init
        STATE_DATA = {
            "exec_time": time.time()
        }
        time_start = time.time()
        # Get Cells to Update
        update_cells = self.funcs["update"](self.grid)["update_cells"]
        # Update Grid
        self.grid.updateGridCells(update_cells)
        # Update State
        STATE_DATA.update({
            "exec_time": time.time() - STATE_DATA["exec_time"]
        })
        self.current.update({
            "step": self.current["step"] + 1,
            "image": self.grid.getImage(),
            **STATE_DATA
        })
        # Update History
        self.history.append(self.getCurrentState())

        return self.current
        
    def getCurrentState(self):
        '''
        Get Current State
        '''
        return {
            "grid": self.grid.copy(),
            **self.current
        }

# Main Functions