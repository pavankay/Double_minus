from grid.grid_cells import GridCells
from grid.grid import Grid
import constants

class Boat:
    def __init__(self, grid_, xy = constants.BOAT_STARTING_POS):
        self.x, self.y = xy
        self.grid = grid_

    def get_availability(self):
        available_moves = set()

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                #if 0 <= nx < constants.ROWS and 0 <= ny < constants.COLS and self.grid[nx][ny]:
                if 0 <= nx <= constants.ROWS and 0 <= ny < constants.COLS:

                    if self.grid[nx, ny].get("navigable"):
                        print(nx, ny)
                        print(self.grid[nx, ny].get("navigable"))
                        available_moves.add((dx, dy))
                    else:
                        print(nx, ny)
                        print(self.grid[nx, ny].get("navigable"))
        return available_moves


        #abs(a[0] - b[0]) + abs(ap[1] - b[1])
    def get_neighbors(self):
        return len(self.get_availability())



    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < constants.ROWS and 0 <= ny < constants.COLS and self.grid[nx, ny]:
            self.x, self.y = nx, ny
            return True
        return False


#usage
grid = Grid.load(constants.DATAPATH)
boat = Boat(grid)
print(boat.get_neighbors())

