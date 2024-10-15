import pygame
from grid.grid import Grid
import constants
import sys
#initialize classes
pygame.init()

if constants.REPLACE_DATA:
    grid = Grid()
    grid.save(constants.DATAPATH)


grid_map = Grid.load(constants.DATAPATH)


width, height =  constants.WIDTH,  constants.HEIGHT
rows, cols = grid_map.rows, grid_map.cols
cell_size = width // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FLL Double Minus innovation project")
WHITE = (255, 255, 255)
BLUE = NAVIGABLE = (14, 135, 204)

BLACK = NON_NAVIGABLE = (0, 0, 0)
def draw_grid():
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (width, y))

    for y in range(cols):
        for x in range(rows):
            if grid_map[x, y].get("navigable"):
                pygame.draw.rect(screen, NAVIGABLE, (x*cell_size, y*cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, NON_NAVIGABLE, (x*cell_size, y*cell_size, cell_size, cell_size))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()