from grid.grid_cells import GridCells
import json
import constants
import random


class Grid:
    def __init__(self):
        self.rows = constants.ROWS
        self.cols = constants.COLS
        landmass_map = GridCells.generate_landmass_map(self.rows, self.cols)
        self.grid = [[GridCells.default(i, j, landmass_map) for j in range(self.cols)] for i in range(self.rows)]
        self.randomize_target = constants.RANDOMIZE_TARGET_POS


    def check_for_water(self, x, y):
        neighbors = [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x, y)]

        for neighbor in neighbors:
            if not (0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols):
                return False

            if not self.is_navigable(*neighbor):
                return False

        return True

    def find_random_location(self):
        x, y = -1, -1

        while not self.check_for_water(x, y):
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)

        return x, y

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = [[GridCells(**y) for y in x] for x in data["grid"]]
        return self

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            return cls.from_json(json.load(f))


    def set_cell(self, xy, value):
        x, y = xy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[y][x] = value

    def get_cell(self, xy):
        x, y = xy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[y][x]
        return None

    def is_navigable(self, x, y):
        return self.grid[y][x].dict["navigable"]

    __setitem__ = set_cell
    __getitem__ = get_cell

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    __repr__ = __str__

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.save_json(), f, indent=4)

    def save_json(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "grid": [[y.save() for y in x] for x in self.grid]
        }
