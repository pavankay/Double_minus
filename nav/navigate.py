import math
import constants

# Short-sighted navigation class with backtracking and shore avoidance
class GreedyNavigate:
    def __init__(self, boat):
        self.boat = boat
        self.target = constants.BOAT_TARGET_POS
        self.visited = set()  # Keep track of visited positions
        self.path_stack = []   # Stack to track the backtracking path

    @staticmethod
    def calculate_distance(pos1, pos2):
        """Calculate Euclidean distance between two positions."""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def is_near_shore(self, x, y):
        """
        Check if the cell (x, y) is adjacent to a non-navigable cell (shore).
        Return True if near shore, False otherwise.
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < constants.ROWS and 0 <= ny < constants.COLS:
                    if not self.boat.grid[nx, ny].get("navigable"):
                        return True  # Shore found nearby
        return False

    def get_best_move(self):
        """
        This method looks at the available navigable cells around the boat
        and picks the one that gets the closest to the target based on Euclidean distance.
        Penalizes moves that get too close to the shore.
        """
        available_moves = self.boat.get_availability()
        best_move = None
        best_score = float('inf')  # We'll minimize the score: distance + shore_penalty

        for move in available_moves:
            predicted_x = self.boat.x + move[0]
            predicted_y = self.boat.y + move[1]
            predicted_position = (predicted_x, predicted_y)

            # Ignore positions we've already visited
            if predicted_position in self.visited:
                continue

            distance_to_target = self.calculate_distance(predicted_position, self.target)

            # Add a penalty if the move is near the shore
            shore_penalty = 10 if self.is_near_shore(predicted_x, predicted_y) else 0

            score = distance_to_target + shore_penalty

            if score < best_score:
                best_score = score
                best_move = move

        return best_move

    def navigate(self):
        """
        Navigate the boat by making the best short-sighted move towards the target.
        If no valid move is found, backtrack and try a different path.
        """
        best_move = self.get_best_move()

        if best_move:
            # Record the current position in the stack before moving
            self.path_stack.append((self.boat.x, self.boat.y))

            # Move the boat
            dx, dy = best_move
            self.boat.move(dx, dy)

            # Mark the current position as visited
            self.visited.add((self.boat.x, self.boat.y))

            print(f"Boat moved to ({self.boat.x}, {self.boat.y})")

        else:
            # No valid moves, so backtrack
            if self.path_stack:
                # Pop the last position and move the boat back
                last_position = self.path_stack.pop()
                self.boat.x, self.boat.y = last_position
                print(f"Backtracking to {last_position}")
            else:
                print("No more moves to backtrack. Boat is stuck.")
