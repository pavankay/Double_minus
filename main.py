import pygame
import random
import math
from collections import deque

# Initialize Pygame
pygame.init()

# === CONSTANTS ===
GRID_SIZE = 100
WIDTH = 900   # Reduced from 1200
HEIGHT = 900  # Reduced from 1000
CELL_SIZE = min(WIDTH, HEIGHT) // GRID_SIZE  # This will now be 8 pixels

# Colors
WATER = (14, 135, 204)
LAND = (0, 0, 0)
BOAT = (255, 0, 255)
BOAT_BORDER = (255, 255, 255)
TARGET = (0, 255, 0)
VISITED = (173, 216, 230)
GRID_LINES = (100, 100, 100)

# Navigation Settings
SHORE_PENALTY = 15  # Reduced shore penalty for more balanced paths
MAX_STUCK_TIME = 10
PATHFINDING_LIMIT = 2000  # Increased limit for better path finding
DIAGONAL_COST = 1.4  # Correct cost for diagonal movement

# Terrain Generation
LAND_CHANCE = 0.45
SMOOTHING_PASSES = 8


def generate_terrain():
    """Generate terrain using cellular automata"""
    grid = [[1 if random.random() < LAND_CHANCE else 0
             for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)]

    for _ in range(SMOOTHING_PASSES):
        new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                land_neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            land_neighbors += grid[ny][nx]
                new_grid[y][x] = 1 if (grid[y][x] == 1 and land_neighbors >= 4) or \
                                      (grid[y][x] == 0 and land_neighbors >= 5) else 0
        grid = new_grid

    return [[LAND if cell else WATER for cell in row] for row in grid]


def count_land_in_radius(grid, x, y, radius=2):
    """Count land cells within radius with improved distance weighting"""
    land_count = 0
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            nx, ny = x + dx, y + dy
            if (0 <= nx < GRID_SIZE and
                    0 <= ny < GRID_SIZE and
                    grid[ny][nx] == LAND):
                # Exponential decay with distance
                distance = math.sqrt(dx * dx + dy * dy)
                land_count += math.exp(-distance)
    return land_count


def get_neighbors(pos, grid):
    """Get valid water neighbors with proper diagonal handling"""
    x, y = pos
    neighbors = []

    # Check all 8 directions
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        new_x = x + dx
        new_y = y + dy

        # Basic bounds and water check
        if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
            continue
        if grid[new_y][new_x] != WATER:
            continue

        # For diagonal moves, check if we can actually get there
        if dx != 0 and dy != 0:
            if grid[y][new_x] == LAND or grid[new_y][x] == LAND:
                continue

        neighbors.append((new_x, new_y))

    return neighbors


def find_water_pos(grid):
    """Find a good water position away from land"""
    best_pos = None
    lowest_land_count = float('inf')

    attempts = 100  # Limit search attempts
    for _ in range(attempts):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == WATER:
            land_count = count_land_in_radius(grid, x, y)
            if land_count < lowest_land_count:
                best_pos = [x, y]
                lowest_land_count = land_count

    return best_pos if best_pos else [GRID_SIZE // 2, GRID_SIZE // 2]


def find_path(grid, start, target):
    """A* pathfinding with improved heuristic and balanced penalties"""

    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def heuristic(pos):
        # Combine manhattan distance with diagonal shortcut potential
        dx = abs(target[0] - pos[0])
        dy = abs(target[1] - pos[1])
        straight = abs(dx - dy)
        diagonal = min(dx, dy)
        return straight + DIAGONAL_COST * diagonal

    start = tuple(start)
    target = tuple(target)

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    cells_checked = 0

    while frontier and cells_checked < PATHFINDING_LIMIT:
        current = min(frontier, key=lambda x: x[0])[1]
        if current == target:
            break

        frontier = [f for f in frontier if f[1] != current]
        cells_checked += 1

        for next_pos in get_neighbors(current, grid):
            # Calculate movement cost (diagonal vs straight)
            dx = abs(next_pos[0] - current[0])
            dy = abs(next_pos[1] - current[1])
            move_cost = DIAGONAL_COST if (dx + dy) == 2 else 1

            # Add shore penalty with distance falloff
            shore_penalty = SHORE_PENALTY * count_land_in_radius(grid, next_pos[0], next_pos[1])

            # Calculate total cost
            new_cost = cost_so_far[current] + move_cost + shore_penalty

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos)
                frontier.append((priority, next_pos))
                came_from[next_pos] = current

    # Reconstruct path
    path = []
    current = target
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()

    # Smooth the path
    if len(path) > 2:
        smoothed_path = [path[0]]
        for i in range(1, len(path) - 1):
            prev = smoothed_path[-1]
            current = path[i]
            next_pos = path[i + 1]

            # Only keep points that represent significant direction changes
            dx1 = current[0] - prev[0]
            dy1 = current[1] - prev[1]
            dx2 = next_pos[0] - current[0]
            dy2 = next_pos[1] - current[1]

            if dx1 != dx2 or dy1 != dy2:
                smoothed_path.append(current)

        smoothed_path.append(path[-1])
        path = smoothed_path

    return path


def get_next_move(grid, boat_pos, target_pos, visited):
    """Get next move with pathfinding and unstuck behavior"""
    path = find_path(grid, boat_pos, target_pos)

    if len(path) > 1:
        next_pos = path[1]
        return [next_pos[0] - boat_pos[0], next_pos[1] - boat_pos[1]]

    # If stuck, try to move to least visited water away from shore
    neighbors = get_neighbors(boat_pos, grid)
    if neighbors:
        best_pos = min(neighbors, key=lambda n: (
                sum(1 for v in visited if v == n) +
                count_land_in_radius(grid, n[0], n[1]) * SHORE_PENALTY
        ))
        return [best_pos[0] - boat_pos[0], best_pos[1] - boat_pos[1]]

    return None


def draw_boat(screen, pos, size):
    """Draw boat with visibility features"""
    center_x = pos[0] * CELL_SIZE + CELL_SIZE // 2
    center_y = pos[1] * CELL_SIZE + CELL_SIZE // 2
    radius = int(CELL_SIZE * 0.8) // 2

    # Draw white border
    pygame.draw.circle(screen, BOAT_BORDER, (center_x, center_y), radius)
    # Draw boat interior
    pygame.draw.circle(screen, BOAT, (center_x, center_y), radius - 2)


def reset_simulation():
    """Reset the simulation state"""
    grid = generate_terrain()
    boat_pos = find_water_pos(grid)
    target_pos = find_water_pos(grid)
    while target_pos == boat_pos:
        target_pos = find_water_pos(grid)
    return grid, boat_pos, target_pos, set()


# === SETUP ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Minus Demo")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Initialize simulation
grid, boat_pos, target_pos, path = reset_simulation()
moving = True
running = True

# === MAIN LOOP ===
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving = not moving
            elif event.key == pygame.K_r:
                grid, boat_pos, target_pos, path = reset_simulation()
                moving = True
            elif event.key == pygame.K_g:  # Added key for new grid only
                grid = generate_terrain()
                path.clear()
                moving = True

    # Draw background
    screen.fill((50, 50, 50))

    # Draw terrain and visited paths
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            # Draw terrain
            pygame.draw.rect(screen, grid[y][x], rect)

            # Draw visited path
            if (x, y) in path:
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.fill(VISITED)
                s.set_alpha(128)
                screen.blit(s, rect)

            # Draw grid lines
            pygame.draw.rect(screen, GRID_LINES, rect, 1)

    # Draw target
    target_center = (
        target_pos[0] * CELL_SIZE + CELL_SIZE // 2,
        target_pos[1] * CELL_SIZE + CELL_SIZE // 2
    )
    target_radius = int(CELL_SIZE * 0.6) // 2
    pygame.draw.circle(screen, TARGET, target_center, target_radius)

    # Draw boat
    draw_boat(screen, boat_pos, CELL_SIZE)

    # Update boat position
    if moving and boat_pos != target_pos:
        move = get_next_move(grid, boat_pos, target_pos, path)
        if move:
            boat_pos[0] += move[0]
            boat_pos[1] += move[1]
            path.add((boat_pos[0], boat_pos[1]))

            # Check if stuck
            if len(path) > MAX_STUCK_TIME:
                recent_positions = list(path)[-MAX_STUCK_TIME:]
                position_counts = {}
                for pos in recent_positions:
                    position_counts[pos] = position_counts.get(pos, 0) + 1
                    if position_counts[pos] > 3:  # If visited same spot 3 times
                        # Clear recent history and try new path
                        path = set(list(path)[:-MAX_STUCK_TIME])

    # Draw UI text
    if boat_pos == target_pos:
        status = "TARGET REACHED!"
    else:
        status = "NAVIGATING" if moving else "PAUSED"
    text = font.render(status, True, (255, 255, 255))
    screen.blit(text, (10, 10))

    instructions = font.render("SPACE: Pause/Resume   R: Reset   G: New Grid", True, (255, 255, 255))
    screen.blit(instructions, (10, HEIGHT - 30))

    # Update display
    pygame.display.flip()
    clock.tick(10)  # Slightly higher framerate

pygame.quit()