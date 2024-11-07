from .colors import *
import pygame

font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 32)  # Slightly smaller font for input

def draw_text(screen, text, x, y, color=WHITE, custom_font=None):
    """Utility function to draw centered text"""
    text_surface = (custom_font or font).render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect
