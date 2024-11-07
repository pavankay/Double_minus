import pygame
from .colors import *
from .text import *
import constants
from grid.grid import Grid
from nav.navigate import GreedyNavigate
from nav.boat import Boat

width, height = constants.WIDTH, constants.HEIGHT
sidebar_width = 200


# Setup
grid_map = Grid.load(constants.DATAPATH)
boat = Boat(grid_map)
navigator = GreedyNavigate(boat)
cell_size = width // grid_map.cols

# Game state
current_page = 0
navigating = False
boat_pos = list(constants.BOAT_STARTING_POS)
target_pos = list(constants.BOAT_TARGET_POS)

# Input state
boat_input_active = False
target_input_active = False
boat_input_text = f"{boat_pos[0]}, {boat_pos[1]}"
target_input_text = f"{target_pos[0]}, {target_pos[1]}"


def generate_new_grid():
    """Generate a new grid and save it"""
    global grid_map, boat, navigator, navigating, boat_pos, target_pos, boat_input_text, target_input_text

    # Create new grid instance using your existing Grid class
    grid_map = Grid()

    # Save to grid.json using your existing save method
    grid_map.save(constants.DATAPATH)

    # Reinitialize boat and navigator with new grid
    boat = Boat(grid_map)
    navigator = GreedyNavigate(boat)

    # Reset positions to valid water locations
    new_boat_pos = grid_map.find_random_location()
    new_target_pos = grid_map.find_random_location()

    # Update all positions
    boat_pos = list(new_boat_pos)
    target_pos = list(new_target_pos)
    print(target_pos)
    boat.x, boat.y = boat_pos[0], boat_pos[1]
    constants.BOAT_TARGET_POS = tuple(target_pos)

    # Update input text displays
    boat_input_text = f"{boat_pos[0]}, {boat_pos[1]}"
    target_input_text = f"{target_pos[0]}, {target_pos[1]}"

    # Stop navigation when generating new map
    navigating = False

def draw_button(screen, text, y_pos):
    """Draw a button with text at specified vertical position"""
    button_rect = pygame.Rect(width // 2 - 100, y_pos, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    draw_text(screen, text, width // 2, y_pos + 25)
    return button_rect


def draw_input_box(screen, text, rect, active, label=""):
    """Draw an input box with text, active state, and label"""
    # Draw label
    if label:
        draw_text(screen, label, rect.centerx, rect.y - 15, BLACK, input_font)

    # Draw input box background
    pygame.draw.rect(screen, INPUT_BG_COLOR, rect)

    # Draw border
    border_color = INPUT_ACTIVE_COLOR if active else BUTTON_COLOR
    pygame.draw.rect(screen, border_color, rect, 2)

    # Draw text
    text_surface = input_font.render(text, True, BLACK)
    # Align text to the left with padding
    text_x = rect.x + 5
    text_y = rect.centery - text_surface.get_height() // 2
    screen.blit(text_surface, (text_x, text_y))

    return rect


def draw_grid(screen):
    """Draw the navigation grid with walls and paths"""
    for y in range(grid_map.rows):
        for x in range(grid_map.cols):
            color = BLUE if grid_map[x, y].get("navigable") else BLACK
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw grid lines
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, BLACK, (0, y), (width, y))


def draw_navigation(screen):
    """Draw the navigation view with boat, start, and target positions"""
    global navigating
    if navigating:
        navigator.navigate()
        if (boat.x, boat.y) == tuple(target_pos):
            navigating = False

    draw_grid(screen)

    # Draw start, target, and boat positions
    pygame.draw.rect(screen, START_COLOR, (boat_pos[0] * cell_size, boat_pos[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, END_COLOR, (target_pos[0] * cell_size, target_pos[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, BOAT_COLOR, (boat.x * cell_size, boat.y * cell_size, cell_size, cell_size))


def draw_sidebar(screen):
    """Draw sidebar with menu button, coordinate inputs, and navigation controls"""
    # Sidebar background
    pygame.draw.rect(screen, SIDEBAR_COLOR, (width, 0, sidebar_width, height))

    # Menu button
    menu_rect = pygame.Rect(width + 20, 20, sidebar_width - 40, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, menu_rect)
    draw_text(screen, "Menu", width + sidebar_width // 2, 40)

    # Input boxes for coordinates
    boat_input_rect = pygame.Rect(width + 20, 100, sidebar_width - 40, 40)
    target_input_rect = pygame.Rect(width + 20, 180, sidebar_width - 40, 40)

    draw_input_box(screen, boat_input_text, boat_input_rect, boat_input_active, "Boat Position (x,y)")
    draw_input_box(screen, target_input_text, target_input_rect, target_input_active, "Target Position (x,y)")

    # Start/Stop button and Generate Map button (only shown on navigation page)
    start_stop_rect = None
    generate_map_rect = None
    if current_page == 2:
        start_stop_rect = pygame.Rect(width + 20, 260, sidebar_width - 40, 40)
        text = "Stop" if navigating else "Start"
        draw_input_box(screen, text, start_stop_rect, False)

        # Add Generate Map button
        generate_map_rect = pygame.Rect(width + 20, 320, sidebar_width - 40, 40)
        draw_input_box(screen, "Generate Map", generate_map_rect, False)

    return menu_rect, boat_input_rect, target_input_rect, start_stop_rect, generate_map_rect


def draw_page(screen):
    """Draw the current page content"""
    screen.fill(WHITE if current_page == 2 else BLUE)

    if current_page == 0:
        draw_text(screen, "Main Menu", width // 2, 100)
        return draw_button(screen, "Go to Page 2", 200)
    elif current_page == 1:
        draw_text(screen, "Page 2", width // 2, 100)
        return draw_button(screen, "Go to Page 3", 200)
    else:  # Page 3 (Navigation)
        draw_navigation(screen)
        return pygame.Rect(0, 0, 0, 0)  # Return empty rect since we don't need a button
