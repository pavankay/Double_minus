import pygame
from grid.grid import Grid
from nav.boat import Boat
import constants
import sys
#initialize classes
pygame.init()

if constants.REPLACE_DATA:
    print("Replacing data...")
    grid = Grid()
    grid.save(constants.DATAPATH)
else:
    print("Using same data...")


grid_map = Grid.load(constants.DATAPATH)
boat = Boat(grid_map)
print(boat.get_neighbors())



width, height =  constants.WIDTH,  constants.HEIGHT
rows, cols = grid_map.rows, grid_map.cols
cell_size = width // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(constants.PYGAME_TITLE)
WHITE = (255, 255, 255)
BLUE = NAVIGABLE = (14, 135, 204)
BOAT = (128,0,128)

BLACK = NON_NAVIGABLE = (0, 0, 0)

START = (255, 165, 0)
END = (0, 255, 0)

clock = pygame.time.Clock()
target = constants.BOAT_TARGET_POS

def draw_grid():
    for y in range(cols):
        for x in range(rows):
            if grid_map[x, y].get("navigable"):
                pygame.draw.rect(screen, NAVIGABLE, (x*cell_size, y*cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, NON_NAVIGABLE, (x*cell_size, y*cell_size, cell_size, cell_size))
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (width, y))



    start_x = constants.BOAT_STARTING_POS[0] * cell_size
    start_y = constants.BOAT_STARTING_POS[1] * cell_size
    pygame.draw.rect(screen, START, (start_x, start_y, cell_size, cell_size))

    end_x = constants.BOAT_TARGET_POS[0] * cell_size
    end_y = constants.BOAT_TARGET_POS[1] * cell_size
    pygame.draw.rect(screen, END, (end_x, end_y, cell_size, cell_size))

    boat_x = boat.x * cell_size
    boat_y = boat.y * cell_size
    pygame.draw.rect(screen, BOAT, (boat_x, boat_y, cell_size, cell_size))


import math

pygame.font.init()
font = pygame.font.Font(None, 36)


def draw_gps_marker():
    dx = target_x - boat_x
    dy = target_y - boat_y

    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance == 0:
        return
    angle = math.degrees(math.atan2(dy, dx))

    marker_distance = min(100, distance)
    gps_x = boat_x + dx / distance * marker_distance
    gps_y = boat_y + dy / distance * marker_distance

    # Calculate the perpendicular offset
    perp_offset = -20  # Distance to move the text slightly above the line
    perp_dx = -dy / distance * perp_offset
    perp_dy = dx / distance * perp_offset

    # Position the text slightly above the line
    text_x = gps_x + perp_dx
    text_y = gps_y + perp_dy

    text_surface = font.render("GPS Target", True, (0, 255, 0))
    rotated_text = pygame.transform.rotate(text_surface, -angle)

    text_rect = rotated_text.get_rect(center=(int(text_x), int(text_y)))
    screen.blit(rotated_text, text_rect)

    pygame.draw.line(screen, (0, 255, 0), (boat_x, boat_y), (target_x, target_y), 2)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        boat.move(0, -1)
    elif keys[pygame.K_DOWN]:
        boat.move(0, 1)
    elif keys[pygame.K_LEFT]:
        boat.move(-1, 0)
    elif keys[pygame.K_RIGHT]:
        boat.move(1, 0)

    clock.tick(30)

    screen.fill(WHITE)
    draw_grid()

    boat_x = (boat.x * cell_size) + cell_size // 2
    boat_y = (boat.y * cell_size) + cell_size // 2

    target_x = (target[0] * cell_size) + cell_size // 2
    target_y = (target[1] * cell_size) + cell_size // 2

    pygame.draw.line(screen, (255, 0, 0), (boat_x, boat_y), (target_x, target_y), 2)

    draw_gps_marker()

    pygame.display.flip()
