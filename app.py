"""
Stream lit GUI for hosting ConwaysGameofLife
"""

# Imports
import os
import json
import functools
import numpy as np
import streamlit as st
from stqdm import stqdm
from code_editor import code_editor

from Utils.VideoUtils import *

from Simulator import *
from Rules import *

# Main Vars
config = json.load(open("./StreamLitGUI/UIConfig.json", "r"))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose one of the following",
        tuple(
            [config["PROJECT_NAME"]] + 
            config["PROJECT_MODES"]
        )
    )
    
    if selected_box == config["PROJECT_NAME"]:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(" ", "_").lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config["PROJECT_NAME"])
    st.markdown("Github Repo: " + "[" + config["PROJECT_LINK"] + "](" + config["PROJECT_LINK"] + ")")
    st.markdown(config["PROJECT_DESC"])

    # st.write(open(config["PROJECT_README"], "r").read())

#############################################################################################################################
# Repo Based Vars
PATHS = {
    "cache": "StreamLitGUI/CacheData/Cache.json",
    "temp": "StreamLitGUI/TempData/"
}
GRID_PARAMS = {
    "2D": {
        "max_grid_size": (100, 100)
    }
}

# Util Vars
CACHE = {}
SETTINGS = {
    "display_size": 512
}

# Util Functions
def LoadCache():
    '''
    Load Cache
    '''
    global CACHE
    CACHE = json.load(open(PATHS["cache"], "r"))

def SaveCache():
    '''
    Save Cache
    '''
    global CACHE
    json.dump(CACHE, open(PATHS["cache"], "w"), indent=4)

# Main Functions
def CachedFunc_SimRun_2D(GridValues, USERINPUT_Funcs, SimParams):
    '''
    Cached Function - Run Simulation - 2D
    '''
    # Init Grid
    GRID = np.empty((GridValues.shape[0], GridValues.shape[1]), dtype=object)
    for i in range(GridValues.shape[0]):
        for j in range(GridValues.shape[1]):
            GRID[i, j] = Cell(GridValues[i, j], (i, j))
    GRID = Grid(GRID)
    # Init Sim
    SIM = Simulation(GRID, USERINPUT_Funcs, **SimParams)
    # Run Sim
    for i in stqdm(range(SIM.n_iterations), desc="Running Simulation"):
        SIM.step()

    return SIM

# UI Functions
def UI_LoadRuleFunc(dim="2D"):
    '''
    UI - Load Rule Function
    '''
    # Init
    st.markdown("## Rule Function")
    # Load Func
    USERINPUT_RuleFuncName = st.selectbox(
        "Rule Function",
        tuple(RULE_FUNCS[dim].keys())
    )
    USERINPUT_RuleFunc = RULE_FUNCS[dim][USERINPUT_RuleFuncName]
    # Load Params
    USERINPUT_RuleFuncParams_str = st.text_area(
        "Rule Function Params", 
        value=json.dumps(USERINPUT_RuleFunc["params"], indent=8),
        height=200
    )
    USERINPUT_RuleFuncParams = json.loads(USERINPUT_RuleFuncParams_str)
    # Apply Params
    USERINPUT_RuleFunc.update({
        "params": USERINPUT_RuleFuncParams
    })

    return USERINPUT_RuleFunc

def UI_GenerateGrid_2D():
    '''
    UI - Generate Grid - 2D
    '''
    # Init
    st.markdown("## Generate Grid")
    # Get Grid Size
    cols = st.columns(2)
    USERINPUT_GridSize_X = cols[0].slider("Grid Width", min_value=1, max_value=100, value=10)
    USERINPUT_GridSize_Y = cols[0].slider("Grid Height", min_value=1, max_value=100, value=10)
    USERINPUT_GridSize = (USERINPUT_GridSize_X, USERINPUT_GridSize_Y)
    ## Display Grid Size Indicator
    I_GridSizeIndicator = np.zeros(GRID_PARAMS["2D"]["max_grid_size"], dtype=float)
    I_GridSizeIndicator[:USERINPUT_GridSize[0], :USERINPUT_GridSize[1]] = 1.0
    cols[1].image(I_GridSizeIndicator, caption="Grid Size Indicator", use_container_width=True)

    # Generate Grid
    USERINPUT_RandomSeed = int(st.number_input("Random Seed", value=0, step=1))
    cols = st.columns(2)
    USERINPUT_Binary = cols[0].checkbox("Binary", value=True)
    GridValues = np.random.RandomState(seed=USERINPUT_RandomSeed).rand(*USERINPUT_GridSize)
    if USERINPUT_Binary: GridValues = np.array(GridValues >= 0.5, dtype=float)
    ## Display Grid
    st.image(
        ResizeImage_Pixelate(GridValues, maxSize=SETTINGS["display_size"]), 
        caption="Grid", use_container_width=False
    )

    return GridValues

def UI_SimulatorParams_2D():
    '''
    UI - Simulator Params - 2D
    '''
    # Init
    st.markdown("## Simulator Params")
    # Load Params
    USERINPUT_Iterations = st.number_input("Iterations", value=10, step=1)

    USERINPUT_SimParams = {
        "n_iterations": USERINPUT_Iterations
    }
    return USERINPUT_SimParams

def UI_SimVis_2D(SIM):
    '''
    UI - Sim Visualisation - 2D
    '''
    # Init
    st.markdown("## Visualise Simulation")
    # Visualise
    # ## Save History as GIF and Display
    # save_path = os.path.join(PATHS["temp"], "SimHistory.gif")
    # SimHistory_Images = [ResizeImage_Pixelate(h["image"], maxSize=SETTINGS["display_size"]) for h in SIM.history]
    # VideoUtils_SaveFrames2Video(SimHistory_Images, save_path, fps=5.0)
    # st.image(save_path, caption="Simulation", use_container_width=True)
    # ## Display History Slider
    # USERINPUT_HistorySlider = st.slider("Step", min_value=0, max_value=len(SIM.history)-1, value=0)
    # st.image(
    #     ResizeImage_Pixelate(SIM.history[USERINPUT_HistorySlider]["image"], maxSize=SETTINGS["display_size"]), 
    #     caption="Simulation", use_container_width=False
    # )
    ## Save History as Video and Display
    save_path_converted = os.path.join(PATHS["temp"], "SimHistory_Converted.mp4")
    SimHistory_Images = [ResizeImage_Pixelate(h["image"], maxSize=SETTINGS["display_size"]) for h in SIM.history]
    VideoUtils_SaveFrames2Video(SimHistory_Images, save_path_converted, fps=20.0)
    st.video(save_path_converted)

# Repo Based Functions
def cellular_automata_simulator_2d():
    # Title
    st.header("Cellular Automata Simulator")

    # Prereq Loaders
    SETTINGS["display_size"] = st.sidebar.slider("Display Size", min_value=128, max_value=1024, value=512, step=128)

    # Load Inputs
    GridValues = UI_GenerateGrid_2D()
    RuleFunc = UI_LoadRuleFunc(dim="2D")
    SimParams = UI_SimulatorParams_2D()

    # Process Inputs
    USERINPUT_Process = st.checkbox("Stream Process", value=False)
    if not USERINPUT_Process: USERINPUT_Process = st.button("Process")
    if USERINPUT_Process:
        USERINPUT_Funcs = {
            "update": functools.partial(RuleFunc["func"], **RuleFunc["params"])
        }
        SIM = CachedFunc_SimRun_2D(GridValues, USERINPUT_Funcs, SimParams)
        # Display Outputs
        UI_SimVis_2D(SIM)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()