import grid_cells
import json

class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.grid = [[grid_cells.default() for _ in range(cols)] for _ in range(rows)]

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = [[grid_cells.GridCells(**y) for y in x] for x in data["grid"]]
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



#grid[0, 0].set("navigable", True)

#grid.save("grid.json")
#grid = Grid.load("grid.json")
#print(grid[0, 0].get("navigable"))

