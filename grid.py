
class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * cols for _ in range(rows)]

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

    people = {"name": "John", "age": 30, "location": "New York"}



