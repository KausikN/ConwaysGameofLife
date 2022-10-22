"""
Rule - Conways Game of Life
"""

# Imports
import cv2
import numpy as np

# Main Functions
# Rule Functions
def RuleFunc_2D_StandardConway(
    GRID,
    window_size=(3, 3),
    live_threshold=0.0,
    **params
    ):
    '''
    Rule Function 2D - Standard Conway

    Cell Rules:
     - Live Cell: Cell value > live_threshold
     - Dead Cell: Cell value <= live_threshold

    Step Rules:
     - Live Cell
        - If 1/5 to 1/3 of neighbors are alive, cell stays alive
        - Else, cell becomes dead
     - Dead Cell
        - If 1/3 to 1/2 of neighbors are alive, cell becomes alive
        - Else, cell stays dead
    '''
    # Init
    update_cells = []
    N_NEIGHBORS = np.prod(window_size)
    # Apply Rules
    for i in range(GRID.shape[0]):
        for j in range(GRID.shape[1]):
            liveCount = 0
            w_topleft = [i - int(window_size[0]/2), j - int(window_size[1]/2)]
            # Get Neighborhood Live Count
            for wi in range(window_size[0]):
                if w_topleft[0]+wi < 0 or w_topleft[0]+wi >= GRID.shape[0]: continue # Out of Bounds
                for wj in range(window_size[1]):
                    if w_topleft[1]+wj < 0 or w_topleft[1]+wj >= GRID.shape[1]: continue # Out of Bounds
                    loc_cur = (w_topleft[0] + wi, w_topleft[1] + wj)
                    if loc_cur[0] == i and loc_cur[1] == j: continue # Ignore self cell
                    if GRID.cell_matrix[loc_cur[0], loc_cur[1]].value > live_threshold: liveCount += 1 # Live Neighbor
            # Check Rules
            # Live Cell
            if GRID.cell_matrix[i, j].value > live_threshold:
                if liveCount <= int(N_NEIGHBORS/5) or liveCount >= int(N_NEIGHBORS/3):
                    updated_cell = GRID.cell_matrix[i, j].copy()
                    updated_cell.value = 0.0
                    update_cells.append(updated_cell)
            # Dead Cell
            else:
                if liveCount >= int(N_NEIGHBORS/3) and liveCount <= int(N_NEIGHBORS/2):
                    updated_cell = GRID.cell_matrix[i, j].copy()
                    updated_cell.value = 1.0
                    update_cells.append(updated_cell)

    OutData = {
        "update_cells": update_cells
    }
    return OutData

# Main Vars
RULE_FUNCS = {
    "2D": {
        "Standard-Conway": {
            "func": RuleFunc_2D_StandardConway,
            "params": {
                "window_size": (3, 3),
                "live_threshold": 0.5
            }
        }
    },
    "3D": {}
}