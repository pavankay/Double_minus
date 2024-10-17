import os

os.chdir(r"/Users/arjun/PycharmProjects/Double_minus")

# Land Mass Generation
LAND_PROBABILITY = 0.425
SMOOTHING_ITERATIONS = 7

# Grid
ROWS = 60
COLS = 60

# Pygame
WIDTH = 780
HEIGHT = 780
DATAPATH = "./data/grid.json"

# Boat
BOAT_STARTING_POS = 0, 0
BOAT_TARGET_POS = 59, 59

# NN
NN_HIDDEN_SIZE = 256
NN_MAX_STEPS = 500  # Increased to allow for longer routes
NN_SAVE_PATH = "./data/NN/route_planner_model.pth"
NN_SAVE_MODEL = True  # New constant to control whether to save the model
NN_TRAINING_SAMPLES = 10000  # Increased for better training
NN_TRAINING_EPOCHS = 1000  # Increased for better training

# Other
REPLACE_DATA = True
PYGAME_TITLE = "FLL Double Minus innovation project"