from grid.grid_cells import GridCells
import json
import constants

class Grid:
    def __init__(self):
        self.rows = constants.ROWS
        self.cols = constants.COLS
        landmass_map = GridCells.generate_landmass_map(self.rows, self.cols)
        self.grid = [[GridCells.default(i, j, landmass_map) for j in range(self.cols)] for i in range(self.rows)]

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = [[GridCells(**y) for y in x] for x in data["grid"]]
        return self

    @classmethod
    def load(cls, filename):
        try:
            with open(filename, 'r') as f:
                return cls.from_json(json.load(f))
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file {filename}.")
            return None

    def set_cell(self, xy, value):
        x, y = xy
        if self.is_valid_position(x, y):
            self.grid[y][x] = value
        else:
            print(f"Warning: Attempted to set invalid cell position ({x}, {y})")

    def get_cell(self, xy):
        x, y = xy
        if self.is_valid_position(x, y):
            return self.grid[y][x]
        print(f"Warning: Attempted to get invalid cell position ({x}, {y})")
        return None

    def is_navigable(self, x, y):
        if self.is_valid_position(x, y):
            return self.grid[y][x].navigable
        return False

    def is_valid_position(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    __setitem__ = set_cell
    __getitem__ = get_cell

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    __repr__ = __str__

    def save(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.save_json(), f, indent=4)
            print(f"Grid saved successfully to {filename}")
        except IOError as e:
            print(f"Error saving grid to {filename}: {e}")

    def save_json(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "grid": [[y.save() for y in x] for x in self.grid]
        }

    def get_navigable_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny) and self.is_navigable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def count_navigable_cells(self):
        return sum(cell.navigable for row in self.grid for cell in row)

# Example usage:
# grid = Grid()
# grid[0, 0].set("navigable", True)
# grid.save("./data/grid.json")
# loaded_grid = Grid.load("./data/grid.json")
# print(loaded_grid[0, 0].get("navigable"))
# print(f"Number of navigable cells: {loaded_grid.count_navigable_cells()}")