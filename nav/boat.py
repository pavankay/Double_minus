from itertools import count

import grid.grid_cells as grid_cells
import grid.grid as grid
import constants

class Boat:
    def __init__(self, grid_, xy = constants.BOAT_STARTING_POS):
        self.x, self.y = xy
        self.grid = grid_


        #abs(a[0] - b[0]) + abs(a[1] - b[1])
    def get_neighbors(self):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                #if 0 <= nx < constants.ROWS and 0 <= ny < constants.COLS and self.grid[nx][ny]:
                if 0 <= constants.ROWS and 0 <= ny < constants.COLS:

                    if grid[nx, ny].get("navigable"):
                        print(nx, ny)
                        print(grid[nx, ny].get("navigable"))
                        count += 1
                    else:
                        print(nx, ny)
                        print(grid[nx, ny].get("navigable"))
        return count


#usage

grid = grid.Grid()

boat = Boat(grid)

print(boat.get_neighbors())
