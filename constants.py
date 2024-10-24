import os

os.chdir(r"C:\repos\BIG projects\Double_Minus\Double_minus")
# Land Mass Generation
LAND_PROBABILITY = 0.425
SMOOTHING_ITERATIONS = 7
# Grid
ROWS = 150
COLS = 150
# Pygame
WIDTH = 1050
HEIGHT = 1050
DATAPATH = "./data/grid.json"
# Boat
BOAT_STARTING_POS = 0, 0
BOAT_TARGET_POS = (ROWS - 1, COLS - 1)
# Other
REPLACE_DATA = True
PYGAME_TITLE = "FLL Double Minus innovation project"

