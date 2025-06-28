import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Orbital Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
CARD_WIDTH = 250
CARD_HEIGHT = 100

# Load the background image
background_image = pygame.image.load('background_menu.jpg')  # Replace with your image path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen

# Draw the back arrow
def draw_back_arrow():
    """Draws a small white arrow on the top left corner."""
    # Draw the arrow using lines to form the '←' shape
    pygame.draw.line(screen, WHITE, (40, 30), (20, 50), 3)  # Diagonal line
    pygame.draw.line(screen, WHITE, (20, 50), (40, 70), 3)  # Bottom diagonal line
    pygame.draw.line(screen, WHITE, (40, 50), (60, 50), 3)  # Horizontal line

def draw_main_menu():
    """Draws the main menu UI with a background image."""
    screen.blit(background_image, (0, 0))

    # Draw the title
    title_text = font.render("ORBITAL SIMULATOR", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw buttons
    buttons = ["Play", "Presets", "Settings"]
    for i, button_text in enumerate(buttons):
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        button_y = 200 + i * (BUTTON_HEIGHT + 20)
        pygame.draw.rect(screen, BLUE, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        text = button_font.render(button_text, True, WHITE)
        text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Draw the back arrow
    draw_back_arrow()

    pygame.display.flip()

def handle_main_menu_click(pos):
    """Handles clicks in the main menu."""
    x, y = pos

    # Check for button clicks
    buttons = ["Play", "Presets", "Settings"]
    for i, button_text in enumerate(buttons):
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        button_y = 200 + i * (BUTTON_HEIGHT + 20)
        if button_x <= x <= button_x + BUTTON_WIDTH and button_y <= y <= button_y + BUTTON_HEIGHT:
            if button_text == "Play":
                return "game"  # Go to game screen
            elif button_text == "Presets":
                return "presets"  # Go to presets page
    return "menu"  # Stay in menu

def draw_presets():
    """Draws the presets page with clickable cards."""
    screen.fill(GRAY)  # Fill the background with gray

    # Draw the title
    title_text = font.render("PRESETS", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw cards for Solar System and Three-Body Problem
    cards = ["Solar System", "Three-Body Problem"]
    for i, card_text in enumerate(cards):
        card_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2
        card_y = 200 + i * (CARD_HEIGHT + 20)
        pygame.draw.rect(screen, BLUE, (card_x, card_y, CARD_WIDTH, CARD_HEIGHT))
        
        text = button_font.render(card_text, True, WHITE)
        text_rect = text.get_rect(center=(card_x + CARD_WIDTH // 2, card_y + CARD_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Draw the back arrow
    draw_back_arrow()

    pygame.display.flip()

def handle_presets_click(pos):
    """Handles clicks on the presets page."""
    x, y = pos

    # Check for back arrow click
    if 30 <= x <= 60 and 20 <= y <= 60:
        return "menu"  # Go back to the main menu

    # Check for card clicks (Solar System and Three-Body Problem)
    if SCREEN_WIDTH // 2 - CARD_WIDTH // 2 <= x <= SCREEN_WIDTH // 2 + CARD_WIDTH // 2:
        if 200 <= y <= 200 + CARD_HEIGHT:
            return "game"  # Solar System clicked
        elif 200 + CARD_HEIGHT + 20 <= y <= 200 + 2 * CARD_HEIGHT + 20:
            return "game"  # Three-Body Problem clicked
    return "presets"  # Stay on presets page

def draw_game_screen():
    """Draws a generic game screen with the background and back arrow."""
    screen.fill(BLACK)  # Placeholder for game screen content
    draw_back_arrow()  # Draw the back arrow on this screen
    pygame.display.flip()

def handle_game_screen_click(pos):
    """Handles clicks on the game screen."""
    x, y = pos

    # Check for back arrow click
    if 30 <= x <= 60 and 20 <= y <= 60:
        return "menu"  # Go back to the main menu

    return "game"  # Stay on the game screen

def main():
    """Main loop for the program."""
    running = True
    current_screen = "menu"  # Start in the main menu

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if current_screen == "menu":
                    current_screen = handle_main_menu_click((x, y))
                elif current_screen == "presets":
                    current_screen = handle_presets_click((x, y))
                elif current_screen == "game":
                    current_screen = handle_game_screen_click((x, y))

        # Draw the appropriate screen based on current_screen
        if current_screen == "menu":
            draw_main_menu()
        elif current_screen == "presets":
            draw_presets()
        elif current_screen == "game":
            draw_game_screen()

    pygame.quit()

if __name__ == "__main__":
    main()
