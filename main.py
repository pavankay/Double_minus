# main.py
import pygame
from grid.grid import Grid
from nav.boat import Boat
import constants
from nav.navigate import GreedyNavigate  # Import the updated GreedyNavigate class
import sys

# Initialize pygame and load the grid/boat
pygame.init()

if constants.REPLACE_DATA:
    print("Replacing data...")
    grid = Grid()
    grid.save(constants.DATAPATH)
else:
    print("Using same data...")

grid_map = Grid.load(constants.DATAPATH)
boat = Boat(grid_map)

if constants.RANDOMIZE_TARGET_POS:
    constants.BOAT_TARGET_POS = grid_map.find_random_location()

# Initialize the greedy navigator
navigator = GreedyNavigate(boat)

# Set up screen and grid settings
width, height = constants.WIDTH, constants.HEIGHT
rows, cols = grid_map.rows, grid_map.cols
cell_size = width // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(constants.PYGAME_TITLE)

# Colors
WHITE = (255, 255, 255)
BLUE = NAVIGABLE = (14, 135, 204)
BOAT = (128, 0, 128)
BLACK = NON_NAVIGABLE = (0, 0, 0)
START = (255, 165, 0)
END = (0, 255, 0)

clock = pygame.time.Clock()
target = constants.BOAT_TARGET_POS

# Draw the grid
def draw_grid():
    for y in range(cols):
        for x in range(rows):
            if grid_map[x, y].get("navigable"):
                pygame.draw.rect(screen, NAVIGABLE, (x * cell_size, y * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, NON_NAVIGABLE, (x * cell_size, y * cell_size, cell_size, cell_size))

    for x in range(0, width, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (width, y))

# Draw the start and end points of the path
def draw_start_end():
    # Draw the start position
    start_x = constants.BOAT_STARTING_POS[0] * cell_size
    start_y = constants.BOAT_STARTING_POS[1] * cell_size
    pygame.draw.rect(screen, START, (start_x, start_y, cell_size, cell_size))

    # Draw the end position
    end_x = constants.BOAT_TARGET_POS[0] * cell_size
    end_y = constants.BOAT_TARGET_POS[1] * cell_size
    pygame.draw.rect(screen, END, (end_x, end_y, cell_size, cell_size))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Navigate the boat using the greedy navigator
    navigator.navigate()

    screen.fill(WHITE)

    # Draw the grid and start/end points
    draw_grid()
    draw_start_end()

    # Draw the boat at its current position
    pygame.draw.rect(screen, BOAT, (boat.x * cell_size, boat.y * cell_size, cell_size, cell_size))

    pygame.display.flip()
    clock.tick(10)

    # Stop the loop if the boat has reached the target
    if (boat.x, boat.y) == constants.BOAT_TARGET_POS:
        print("Boat reached the target!")
        clock.tick(1)
        break
