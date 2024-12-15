import math
import constants
from typing import Optional, Tuple, Set
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GreedyNavigate:
    """
    Implements a greedy navigation strategy with backtracking and shore avoidance.

    The navigator uses a combination of distance-based heuristics and shore
    avoidance penalties to guide a boat towards a target position. It includes
    backtracking capabilities when stuck in local minima.

    Attributes:
        boat: Reference to the boat being navigated
        target (tuple): Target coordinates (x, y)
        visited (set): Set of previously visited positions
        path_stack (list): Stack of positions for backtracking
    """

    def __init__(self, boat):
        """
        Initialize the navigator with a boat.

        Args:
            boat: The boat to navigate
        """
        self.boat = boat
        self.target = constants.BOAT_TARGET_POS
        self.visited: Set[Tuple[int, int]] = set()
        self.path_stack: list[Tuple[int, int]] = []
        logger.info(f"Navigator initialized with target at {self.target}")

    @staticmethod
    def calculate_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance between two positions.

        Args:
            pos1: First position (x1, y1)
            pos2: Second position (x2, y2)

        Returns:
            float: Euclidean distance between the positions
        """
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        return math.sqrt(dx * dx + dy * dy)

    def is_near_shore(self, x: int, y: int) -> bool:
        """
        Check if a position is adjacent to non-navigable cells (shore).

        Args:
            x: X-coordinate to check
            y: Y-coordinate to check

        Returns:
            bool: True if position is near shore, False otherwise
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                if (0 <= nx < constants.ROWS and
                        0 <= ny < constants.COLS and
                        not self.boat.grid[nx, ny].get("navigable")):
                    return True

        return False

    def get_best_move(self) -> Optional[Tuple[int, int]]:
        """
        Determine the best available move based on distance and shore penalties.

        Returns:
            Optional[Tuple[int, int]]: Best movement vector (dx, dy) or None if no valid moves
        """
        available_moves = self.boat.get_availability()
        best_move = None
        best_score = float('inf')

        for move in available_moves:
            predicted_x = self.boat.x + move[0]
            predicted_y = self.boat.y + move[1]
            predicted_position = (predicted_x, predicted_y)

            if predicted_position in self.visited:
                continue

            distance_to_target = self.calculate_distance(
                predicted_position,
                self.target
            )

            shore_penalty = (constants.SHORE_PENALTY
                             if self.is_near_shore(predicted_x, predicted_y)
                             else 0)

            score = distance_to_target + shore_penalty

            if score < best_score:
                best_score = score
                best_move = move

        return best_move

    def navigate(self) -> None:
        """
        Perform one step of navigation towards the target.

        This method uses the following strategy:
        1. Find the best available move using distance and shore penalties
        2. If a valid move is found, take it and record the position
        3. If no valid move is found, backtrack to the previous position
        """
        current_pos = (self.boat.x, self.boat.y)

        if current_pos == self.target:
            logger.info("Target reached!")
            return

        best_move = self.get_best_move()

        if best_move:
            # Record current position before moving
            self.path_stack.append(current_pos)

            # Move the boat
            dx, dy = best_move
            if self.boat.move(dx, dy):
                new_pos = (self.boat.x, self.boat.y)
                self.visited.add(new_pos)
                logger.info(f"Moved to {new_pos}")
            else:
                logger.warning(f"Failed to move {best_move}")
        else:
            # Backtrack if possible
            if self.path_stack:
                last_pos = self.path_stack.pop()
                self.boat.x, self.boat.y = last_pos
                logger.info(f"Backtracking to {last_pos}")
            else:
                logger.warning("No moves available and no positions to backtrack to")