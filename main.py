import pygame
from grid.grid import Grid
from nav.boat import Boat
import constants
import sys
import math
import time
import os
from NeuralNetwork.NavigateNN import RouteplanningNN, create_training_data, train_network, plan_route

# Colors
WHITE = (255, 255, 255)
BLUE = NAVIGABLE = (14, 135, 204)
BOAT_COLOR = (128, 0, 128)
BLACK = NON_NAVIGABLE = (0, 0, 0)
START = (255, 165, 0)
END = (0, 255, 0)
ROUTE = (255, 0, 0)
PLANNED_ROUTE = (255, 192, 203)  # Light pink for the planned route


def draw_grid(screen, grid_map, boat, planned_route, current_route_index, cell_size):
    """Draw the game grid, boat, and planned route."""
    for y in range(grid_map.cols):
        for x in range(grid_map.rows):
            color = NAVIGABLE if grid_map[x, y].get("navigable") else NON_NAVIGABLE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw planned route
    for i, pos in enumerate(planned_route):
        color = ROUTE if i <= current_route_index else PLANNED_ROUTE
        pygame.draw.rect(screen, color, (pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size))

    # Draw grid lines
    for x in range(0, constants.WIDTH, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, constants.HEIGHT))
    for y in range(0, constants.HEIGHT, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (constants.WIDTH, y))

    # Draw start and end positions
    pygame.draw.rect(screen, START, (
    constants.BOAT_STARTING_POS[0] * cell_size, constants.BOAT_STARTING_POS[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, END, (
    constants.BOAT_TARGET_POS[0] * cell_size, constants.BOAT_TARGET_POS[1] * cell_size, cell_size, cell_size))

    # Draw boat
    pygame.draw.rect(screen, BOAT_COLOR, (boat.x * cell_size, boat.y * cell_size, cell_size, cell_size))


def draw_gps_marker(screen, boat, target, cell_size, font):
    """Draw GPS marker and line to target."""
    boat_x = (boat.x * cell_size) + cell_size // 2
    boat_y = (boat.y * cell_size) + cell_size // 2
    target_x = (target[0] * cell_size) + cell_size // 2
    target_y = (target[1] * cell_size) + cell_size // 2

    pygame.draw.line(screen, (0, 255, 0), (boat_x, boat_y), (target_x, target_y), 2)

    dx = target_x - boat_x
    dy = target_y - boat_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance == 0:
        return
    angle = math.degrees(math.atan2(dy, dx))

    marker_distance = min(100, distance)
    gps_x = boat_x + dx / distance * marker_distance
    gps_y = boat_y + dy / distance * marker_distance

    text_surface = font.render("GPS Target", True, (0, 255, 0))
    rotated_text = pygame.transform.rotate(text_surface, -angle)
    text_rect = rotated_text.get_rect(center=(int(gps_x), int(gps_y)))
    screen.blit(rotated_text, text_rect)


def main():
    print("Starting main function")
    pygame.init()
    print("Pygame initialized")

    try:
        if constants.REPLACE_DATA:
            print("Replacing data...")
            grid = Grid()
            grid.save(constants.DATAPATH)
        else:
            print("Using existing data...")

        grid_map = Grid.load(constants.DATAPATH)
        boat = Boat(grid_map)
        print(f"Boat starting position: ({boat.x}, {boat.y})")
        print(f"Number of navigable neighbors: {boat.get_neighbors()}")

        input_size = constants.ROWS * constants.COLS + 4
        hidden_size = constants.NN_HIDDEN_SIZE
        output_size = 9

        if os.path.exists(constants.NN_SAVE_PATH) and not constants.REPLACE_DATA:
            print("Loading existing model...")
            model = RouteplanningNN(grid_size=constants.ROWS, hidden_size=constants.NN_HIDDEN_SIZE, output_size=9)
        else:
            print("Initializing new neural network...")
            model = RouteplanningNN(input_size, hidden_size, output_size)

            print("Generating training data...")
            train_data, train_labels = create_training_data(grid_map, boat, constants.BOAT_TARGET_POS)
            print("Training neural network...")
            train_network(model, train_data, train_labels)

        width, height = constants.WIDTH, constants.HEIGHT
        rows, cols = constants.ROWS, constants.COLS
        cell_size = width // cols
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(constants.PYGAME_TITLE)
        print("Pygame display set up")

        clock = pygame.time.Clock()
        target = constants.BOAT_TARGET_POS
        pygame.font.init()
        font = pygame.font.Font(None, 36)

        planned_route = []
        current_route_index = 0

        def update_display(current_pos, route):
            nonlocal planned_route
            planned_route = route
            screen.fill(WHITE)
            draw_grid(screen, grid_map, boat, planned_route, len(planned_route) - 1, cell_size)
            draw_gps_marker(screen, boat, target, cell_size, font)
            pygame.display.flip()
            pygame.time.wait(100)  # Add a small delay to see the planning process

        print("Planning route...")
        planned_route = plan_route(model, grid_map, boat, constants.BOAT_TARGET_POS, callback=update_display)
        print(f"Planned route length: {len(planned_route)}")

        print("Entering main game loop")
        running = True
        auto_move = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        auto_move = not auto_move
                        print(f"Auto-move {'enabled' if auto_move else 'disabled'}")

            if auto_move and current_route_index < len(planned_route):
                next_pos = planned_route[current_route_index]
                boat.x, boat.y = next_pos
                current_route_index += 1
                print(f"Boat moved to: ({boat.x}, {boat.y})")

                screen.fill(WHITE)
                draw_grid(screen, grid_map, boat, planned_route, current_route_index, cell_size)
                draw_gps_marker(screen, boat, target, cell_size, font)
                pygame.display.flip()

                #time.sleep(0.5)  # Adjust this value to change the speed of movement

            screen.fill(WHITE)
            draw_grid(screen, grid_map, boat, planned_route, current_route_index, cell_size)
            draw_gps_marker(screen, boat, target, cell_size, font)

            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Game loop ended")
        pygame.quit()
        print("Pygame quit")
        sys.exit()


if __name__ == "__main__":
    main()