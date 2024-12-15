from grid.grid_cells import GridCells
import json
import constants
import random


class Grid:
    def __init__(self):
        self.rows = constants.ROWS
        self.cols = constants.COLS
        # Generate the landmass map
        self.landmass_map = GridCells.generate_landmass_map(self.rows, self.cols)
        # Create the grid with correct landmass map access
        self.grid = [[GridCells.default(i, j, self.landmass_map) for j in range(self.cols)] for i in range(self.rows)]
        self.randomize_target = constants.RANDOMIZE_TARGET_POS

    def check_for_water(self, x, y):
        """Check if a location and its surrounding cells are navigable"""
        if x < 0 or y < 0 or x >= self.rows or y >= self.cols:
            return False

        # Check center cell first
        if not self.is_navigable(x, y):
            return False

        # Check surrounding cells (8-directional)
        neighbors = [
            (x - 1, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1),
            (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)
        ]

        for nx, ny in neighbors:
            if not (0 <= nx < self.rows and 0 <= ny < self.cols):
                continue
            if not self.is_navigable(nx, ny):
                return False

        return True

    def find_random_location(self):
        """Find a random navigable location with navigable neighbors"""
        max_attempts = 1000
        attempts = 0

        while attempts < max_attempts:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)

            if self.check_for_water(x, y):
                return (x, y)

            attempts += 1

        # If we couldn't find a good spot, try to find any navigable spot
        for x in range(self.rows):
            for y in range(self.cols):
                if self.is_navigable(x, y):
                    return (x, y)

        raise ValueError("No navigable locations found in grid")

    @classmethod
    def from_json(cls, data):
        """Create a Grid instance from JSON data"""
        instance = cls()
        instance.rows = data["rows"]
        instance.cols = data["cols"]
        instance.grid = [[GridCells(**cell_data) for cell_data in row] for row in data["grid"]]
        return instance

    @classmethod
    def load(cls, filename):
        """Load grid from a JSON file or create new if file doesn't exist"""
        try:
            with open(filename, 'r') as f:
                return cls.from_json(json.load(f))
        except FileNotFoundError:
            # If file doesn't exist, create a new grid
            instance = cls()
            instance.save(filename)
            return instance
        except json.JSONDecodeError:
            # If file is corrupted, create a new grid
            print(f"Warning: {filename} was corrupted. Creating new grid.")
            instance = cls()
            instance.save(filename)
            return instance

    def set_cell(self, xy, value):
        """Set a cell at position xy to value"""
        x, y = xy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[y][x] = value

    def get_cell(self, xy):
        """Get the cell at position xy"""
        x, y = xy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[y][x]
        return None

    def is_navigable(self, x, y):
        """Check if a position is navigable"""
        return self.grid[y][x].dict["navigable"]

    def get_neighbors(self, x, y):
        """Get all valid neighboring positions"""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.rows and
                        0 <= ny < self.cols and
                        self.is_navigable(nx, ny)):
                    neighbors.append((nx, ny))
        return neighbors

    def save(self, filename):
        """Save grid to a JSON file"""
        with open(filename, "w") as file:
            json.dump(self.save_json(), file)

    def save_json(self):
        """Convert grid to JSON format"""
        return {
            "rows": self.rows,
            "cols": self.cols,
            "grid": [[cell.save() for cell in row] for row in self.grid]
        }

    def __str__(self):
        """String representation of the grid"""
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def __repr__(self):
        """Detailed string representation of the grid"""
        return f"Grid({self.rows}x{self.cols})\n{self.__str__()}"

    # Python special methods for accessing grid cells
    __setitem__ = set_cell
    __getitem__ = get_cell

    def get_path_cost(self, path):
        """Calculate the total cost of a path"""
        if not path:
            return float('inf')

        cost = 0
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            # Calculate distance
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            distance = max(dx, dy)  # Diagonal movement costs same as orthogonal

            # Add shore penalty if near land
            if not self.check_for_water(x2, y2):
                distance += constants.SHORE_PENALTY

            cost += distance

        return cost