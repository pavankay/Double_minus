import random
import constants

class GridCells:
    REQUIRED = {"navigable"}

    def __init__(self, **kwds):
        self.dict = kwds
        if "name" in kwds:
            self.name = kwds["name"]

        for key in self.REQUIRED:
            if key not in kwds:
                raise ValueError(f"Missing required key: {key}")
        self.navigable = self.dict["navigable"]

    def __bool__(self):
        return self.dict["navigable"]

    def set(self, key, value):
        self.dict[key] = value

    def get(self, key):
        return self.dict[key]

    def __contains__(self, item):
        return item in self.dict

    def save(self):
        return self.dict

    @staticmethod
    def generate_landmass_map(rows, cols):
        # Initialize the grid randomly
        grid = [[random.random() < constants.LAND_PROBABILITY for _ in range(cols)] for _ in range(rows)]

        # Helper function to count land neighbors
        def count_land_neighbors(x, y):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny]:
                        count += 1
            return count

        # Smooth the map to create more natural-looking landmasses
        for _ in range(constants.SMOOTHING_ITERATIONS):
            new_grid = [[False for _ in range(cols)] for _ in range(rows)]
            for i in range(rows):
                for j in range(cols):
                    land_neighbors = count_land_neighbors(i, j)
                    if grid[i][j]:
                        new_grid[i][j] = land_neighbors >= 4
                    else:
                        new_grid[i][j] = land_neighbors >= 5
            grid = new_grid
        return grid

    @classmethod
    def default(cls, row, col, landmass_map):
        # Now landmass_map is the full 2D array, so we access it with row and col
        return cls(navigable=not landmass_map[row][col], default=True)