import math
import constants
from grid.grid import Grid
from nav.boat import Boat

class Navigate:
    def __init__(self, boat):
        self.boat = boat
        self.target = constants.BOAT_TARGET_POS

    def calculate_gps_vector(self):
        """
             Calculate the vector direction towards the target.
             This is a basic Euclidean vector that points from the boat's current position to the target.
        """
        dx = self.target[0] - self.boat.x
        dy = self.target[1] - self.boat.y
        distance = math.hypot(dx, dy)
        return (dx / distance, dy / distance) if distance != 0 else (0, 0)

    def get_best_move(self):
        """
            This method looks at the available navigable cells around the boat
            and picks the one that moves closest to the target based on the GPS vector.
        """
        available_moves = self.boat.get_availability()
        best_move = None
        best_distance = float('inf')
        gps_vector = self.calculate_gps_vector()

        for move in available_moves:
            predicted_x = self.boat.x + move[0]
            predicted_y = self.boat.y + move[1]
            predicted_dx = self.target[0] - predicted_x
            predicted_dy = self.target[1] - predicted_y
            distance_to_target = math.hypot(predicted_dx, predicted_dy)

            if distance_to_target < best_distance:
                best_distance = distance_to_target
                best_move = move

        return best_move

    def navigate(self):
        """
            Navigate the boat by making the best short-sighted move towards the target.
        """
        best_move = self.get_best_move()

        if best_move:
            dx, dy = best_move
            self.boat.move(dx, dy)
            print(f"Boat moved to ({self.boat.x}, {self.boat.y})")
        else:
            print("No navigable moves available.")

# Example usage:
target_position = (10, 10)
grid = Grid.load("grid.json")
boat = Boat(grid)
navigator = Navigate(boat)

for _ in range(10):
    navigator.navigate()
