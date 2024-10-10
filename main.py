import pygame
import sys
from grid import Grid

#initialize classes
pygame.init()
grid = Grid(20, 20)
grid.save("grid.json")
grid_map = Grid.load("grid.json")


width, height = 400, 400
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
