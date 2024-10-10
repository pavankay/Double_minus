import grid_cells
import json

class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.grid = [[grid_cells.default()] * cols for _ in range(rows)]

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = [[grid_cells.GridCells(**y) for y in x] for x in data["grid"]]
        return self

    def set_cell(self, xy, value):
        x, y = xy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[y][x] = value

    def get_cell(self, xy):
        x, y = xy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[y][x]
        return None

    __setitem__ = set_cell
    __getitem__ = get_cell

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    __repr__ = __str__

    def save(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "grid": [[y.save() for y in x] for x in self.grid]
        }

def save(filename, grid):
    with open(filename, "w") as f:
        json.dump(grid.save(), f, indent=4)

def load(filename):
    with open(filename, 'r') as f:
        return Grid.from_json(json.load(f))


#grid = Grid(5, 5)
#grid[0, 0].set("depth", 10)

#save("grid.json", grid)
grid = load("grid.json")
print(grid[0, 0].get("depth"))

