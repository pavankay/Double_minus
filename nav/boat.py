import constants
from typing import Set, Tuple, Optional


class Boat:
    """
    Represents a boat that can navigate through a grid-based environment.

    The boat can move in 8 directions (including diagonals) and keeps track of its position
    and the navigable areas in the grid.

    Attributes:
        x (int): Current x-coordinate of the boat
        y (int): Current y-coordinate of the boat
        grid: Reference to the navigation grid
    """

    def __init__(self, grid_, xy: Optional[Tuple[int, int]] = None):
        """
        Initialize a boat with a grid and optional starting position.

        Args:
            grid_: The navigation grid the boat will move in
            xy (tuple, optional): Starting coordinates (x, y). Defaults to BOAT_TARGET_POS
        """
        if xy is None:
            xy = constants.BOAT_TARGET_POS
        self.x, self.y = xy
        self.grid = grid_
        self._validate_position()

    def _validate_position(self) -> None:
        """
        Validate that the boat's current position is within grid bounds and navigable.

        Raises:
            ValueError: If the position is invalid or not navigable
        """
        if not (0 <= self.x < constants.ROWS and 0 <= self.y < constants.COLS):
            raise ValueError(f"Position ({self.x}, {self.y}) is outside grid bounds")
        if not self.grid[self.x, self.y].get("navigable"):
            raise ValueError(f"Position ({self.x}, {self.y}) is not navigable")

    def update_xy(self) -> None:
        """Reset the boat's position to the starting position."""
        self.x, self.y = constants.BOAT_STARTING_POS
        self._validate_position()

    def get_availability(self) -> Set[Tuple[int, int]]:
        """
        Get all available moves from the current position.

        Returns:
            Set[Tuple[int, int]]: Set of valid movement vectors (dx, dy)
        """
        available_moves = set()

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = self.x + dx, self.y + dy

                if (0 <= nx < constants.ROWS and
                        0 <= ny < constants.COLS and
                        self.grid[nx, ny].get("navigable")):
                    available_moves.add((dx, dy))

        return available_moves

    def get_neighbors(self) -> int:
        """
        Get the number of navigable neighboring cells.

        Returns:
            int: Count of navigable neighbors
        """
        return len(self.get_availability())

    def move(self, dx: int, dy: int) -> bool:
        """
        Attempt to move the boat by the given vector.

        Args:
            dx (int): Change in x-coordinate (-1, 0, or 1)
            dy (int): Change in y-coordinate (-1, 0, or 1)

        Returns:
            bool: True if move was successful, False otherwise
        """
        nx, ny = self.x + dx, self.y + dy

        if (0 <= nx < constants.ROWS and
                0 <= ny < constants.COLS and
                self.grid[nx, ny].get("navigable")):
            self.x, self.y = nx, ny
            return True

        return False