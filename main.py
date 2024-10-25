import pygame
import sys
from grid.grid import Grid
from nav.boat import Boat
from nav.navigate import GreedyNavigate
import constants

pygame.init()

# Screen settings
width, height = constants.WIDTH, constants.HEIGHT
sidebar_width = 200
screen = pygame.display.set_mode((width + sidebar_width, height))
pygame.display.set_caption("Navigation Demo")

# Colors
WHITE = (255, 255, 255)
BLUE = (14, 135, 204)
BLACK = (0, 0, 0)
BOAT_COLOR = (128, 0, 128)
START_COLOR = (255, 165, 0)
END_COLOR = (0, 255, 0)
BUTTON_COLOR = (100, 100, 100)
SIDEBAR_COLOR = (200, 200, 200)
INPUT_ACTIVE_COLOR = (150, 150, 150)
INPUT_BG_COLOR = (240, 240, 240)  # Light gray background for input boxes

# Setup
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 32)  # Slightly smaller font for input
clock = pygame.time.Clock()
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
boat_input_text = f"{boat_pos[0]},{boat_pos[1]}"
target_input_text = f"{target_pos[0]},{target_pos[1]}"


def draw_text(text, x, y, color=WHITE, custom_font=None):
    """Utility function to draw centered text"""
    text_surface = (custom_font or font).render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect


def draw_button(text, y_pos):
    """Draw a button with text at specified vertical position"""
    button_rect = pygame.Rect(width // 2 - 100, y_pos, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    draw_text(text, width // 2, y_pos + 25)
    return button_rect


def draw_input_box(text, rect, active, label=""):
    """Draw an input box with text, active state, and label"""
    # Draw label
    if label:
        draw_text(label, rect.centerx, rect.y - 15, BLACK, input_font)

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


def update_coordinates(input_text, is_boat=True):
    """Update boat or target coordinates from input text"""
    try:
        coords = [int(x.strip()) for x in input_text.split(',')]
        if len(coords) == 2:
            x, y = coords
            if 0 <= x < grid_map.cols and 0 <= y < grid_map.rows:
                if is_boat:
                    global boat_pos
                    boat_pos = [x, y]
                    boat.x, boat.y = x, y  # Update boat position
                else:
                    global target_pos
                    target_pos = [x, y]
                return True
    except ValueError:
        pass
    return False


def draw_grid():
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


def draw_navigation():
    """Draw the navigation view with boat, start, and target positions"""
    global navigating
    if navigating:
        navigator.navigate()
        if (boat.x, boat.y) == tuple(target_pos):
            navigating = False

    draw_grid()

    # Draw start, target, and boat positions
    pygame.draw.rect(screen, START_COLOR, (boat_pos[0] * cell_size, boat_pos[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, END_COLOR, (target_pos[0] * cell_size, target_pos[1] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, BOAT_COLOR, (boat.x * cell_size, boat.y * cell_size, cell_size, cell_size))


def draw_sidebar():
    """Draw sidebar with menu button, coordinate inputs, and navigation controls"""
    # Sidebar background
    pygame.draw.rect(screen, SIDEBAR_COLOR, (width, 0, sidebar_width, height))

    # Menu button
    menu_rect = pygame.Rect(width + 20, 20, sidebar_width - 40, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, menu_rect)
    draw_text("Menu", width + sidebar_width // 2, 40)

    # Input boxes for coordinates
    boat_input_rect = pygame.Rect(width + 20, 100, sidebar_width - 40, 40)
    target_input_rect = pygame.Rect(width + 20, 180, sidebar_width - 40, 40)

    draw_input_box(boat_input_text, boat_input_rect, boat_input_active, "Boat Position (x,y)")
    draw_input_box(target_input_text, target_input_rect, target_input_active, "Target Position (x,y)")

    # Start/Stop button (only shown on navigation page)
    start_stop_rect = None
    if current_page == 2:
        start_stop_rect = pygame.Rect(width + 20, 260, sidebar_width - 40, 40)
        text = "Stop" if navigating else "Start"
        draw_input_box(text, start_stop_rect, False)

    return menu_rect, boat_input_rect, target_input_rect, start_stop_rect


def draw_page():
    """Draw the current page content"""
    screen.fill(WHITE if current_page == 2 else BLUE)

    if current_page == 0:
        draw_text("Main Menu", width // 2, 100)
        return draw_button("Go to Page 2", 200)
    elif current_page == 1:
        draw_text("Page 2", width // 2, 100)
        return draw_button("Go to Page 3", 200)
    else:  # Page 3 (Navigation)
        draw_navigation()
        return pygame.Rect(0, 0, 0, 0)  # Return empty rect since we don't need a button


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = draw_page()
            menu_rect, boat_input_rect, target_input_rect, start_stop_rect = draw_sidebar()

            # Handle navigation between pages
            if button_rect.collidepoint(mouse_pos):
                current_page = (current_page + 1) % 3
            elif menu_rect.collidepoint(mouse_pos):
                current_page = 0
                navigating = False

            # Handle input box activation
            prev_boat_active = boat_input_active
            prev_target_active = target_input_active

            boat_input_active = boat_input_rect.collidepoint(mouse_pos)
            target_input_active = target_input_rect.collidepoint(mouse_pos)

            # Update coordinates when clicking away
            if prev_boat_active and not boat_input_active:
                update_coordinates(boat_input_text, True)
            if prev_target_active and not target_input_active:
                update_coordinates(target_input_text, False)

            # Handle Start/Stop button
            if start_stop_rect and start_stop_rect.collidepoint(mouse_pos):
                navigating = not navigating

        # Handle keyboard input for coordinate boxes
        if event.type == pygame.KEYDOWN:
            if boat_input_active:
                if event.key == pygame.K_BACKSPACE:
                    boat_input_text = boat_input_text[:-1]
                else:
                    boat_input_text += event.unicode
                # Live update
                update_coordinates(boat_input_text, True)
            elif target_input_active:
                if event.key == pygame.K_BACKSPACE:
                    target_input_text = target_input_text[:-1]
                else:
                    target_input_text += event.unicode
                # Live update
                update_coordinates(target_input_text, False)

    draw_page()
    draw_sidebar()
    pygame.display.flip()
    clock.tick(30)