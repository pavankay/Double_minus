import pygame
import sys
from grid import Grid
pygame.init()
grid = Grid(200, 200)
grid.save("grid.json")
grid_map = Grid.load("grid.json")

print(grid_map[0, 0].get("navigable"))
width, height = 400, 400
rows, cols = 20, 20
cell_size = width // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("20x20 Grid")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_grid():
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (width, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()
