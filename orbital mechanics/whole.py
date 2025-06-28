import pygame
import sys
import math
from collections import deque
import random

random_preset = random.randint(1, 4)
print(random_preset)


# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
red_text = (255, 0, 0)


# Pygame setup
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Orbital Simulator")

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
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
visual_scale = 1


# Draw the back arrow
def draw_back_arrow():
    """Draws a small white arrow on the top left corner."""
    pygame.draw.line(screen, WHITE, (40, 30), (20, 50), 3)  # Diagonal line
    pygame.draw.line(screen, WHITE, (20, 50), (40, 70), 3)  # Bottom diagonal line
    pygame.draw.line(screen, WHITE, (40, 50), (60, 50), 3)  # Horizontal line

def draw_main_menu():
    """Draws the main menu UI with a background image."""
    screen.blit(background_image, (0, 0))

    title_text = font.render("ORBITAL SIMULATOR", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    buttons = ["Play", "Presets","Tutorial", "Settings"]
    for i, button_text in enumerate(buttons):
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        button_y = 200 + i * (BUTTON_HEIGHT + 20)
        pygame.draw.rect(screen, BLUE, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        text = button_font.render(button_text, True, WHITE)
        text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
        screen.blit(text, text_rect)

    draw_back_arrow()

    pygame.display.flip()

def handle_main_menu_click(pos):
    """Handles clicks in the main menu."""
    x, y = pos

    buttons = ["Play", "Presets", "Tutorial","Settings" ]
    for i, button_text in enumerate(buttons):
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        button_y = 200 + i * (BUTTON_HEIGHT + 20)
        if button_x <= x <= button_x + BUTTON_WIDTH and button_y <= y <= button_y + BUTTON_HEIGHT:
            print(f"Clicked on: {button_text}")  # Add this line for debugging
            if button_text == "Play":
                return "game"
            elif button_text == "Presets":
                return "presets"
            elif button_text == "Tutorial":
                return "tutorial"
    return "menu"

def handle_tutorial_click(pos):
    """Handles clicks on the tutorial page."""
    x, y = pos
    if 30 <= x <= 60 and 20 <= y <= 60:
        print("Back button clicked!")  # Add this line for debugging
        return "menu"
    return "tutorial"


def draw_gradient_rect(surface, x, y, width, height, start_color, end_color):
    """Draws a vertical gradient from start_color to end_color."""
    for i in range(height):
        color = (
            int(start_color[0] + (end_color[0] - start_color[0]) * i / height),
            int(start_color[1] + (end_color[1] - start_color[1]) * i / height),
            int(start_color[2] + (end_color[2] - start_color[2]) * i / height)
        )
        pygame.draw.line(surface, color, (x, y + i), (x + width, y + i))

def draw_presets():
    """Draws the presets page with clickable cards, including a gradient background."""
    screen.blit(background_image, (0, 0))

    title_text = font.render("PRESETS", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    cards = ["Solar System", "Three-Body Problem"]
    for i, card_text in enumerate(cards):
        card_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2
        card_y = 200 + i * (CARD_HEIGHT + 20)

        # Create gradient from dark blue to black for each card
        for j in range(CARD_HEIGHT):
            color = (0, 0, int(255 * (1 - j / CARD_HEIGHT)))
            pygame.draw.line(screen, color, (card_x, card_y + j), (card_x + CARD_WIDTH, card_y + j))

        # Draw the text on the card
        text = button_font.render(card_text, True, WHITE)
        text_rect = text.get_rect(center=(card_x + CARD_WIDTH // 2, card_y + CARD_HEIGHT // 2))
        screen.blit(text, text_rect)

    draw_back_arrow()

    pygame.display.flip()


   
def handle_presets_click(pos):
    """Handles clicks on the presets page."""
    x, y = pos

    if 30 <= x <= 60 and 20 <= y <= 60:
        return "menu"

    if SCREEN_WIDTH // 2 - CARD_WIDTH // 2 <= x <= SCREEN_WIDTH // 2 + CARD_WIDTH // 2:
        if 200 <= y <= 200 + CARD_HEIGHT:
            return "solar_system"
        elif 200 + CARD_HEIGHT + 20 <= y <= 200 + 2 * CARD_HEIGHT + 20:
            return "three_body"
    return "presets"


def draw_tutorial_screen():
    """Draws the tutorial screen UI with key-function pairs in boxes, consistent with the homepage."""
    screen.blit(background_image, (0, 0))  # Use the same background as the homepage

    title_text = font.render("TUTORIAL", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    tutorial_keys = [
        ("Mouse Click", "Lock camera on celestial body"),
        ("+ / -", "Zoom in / out"),
        ("P", "Pause / Unpause"),
        ("T", "Toggle trails of bodies"),
        ("Arrow Keys", "Navigate camera"),
        ("R", "Reset simulation")
    ]

    small_font = pygame.font.Font(None, 24)  # Smaller font size (24)

    # Draw boxes with key-function pairs
    box_width = 400
    box_height = 40  # Smaller height for the boxes to match smaller text
    padding = 15  # Adjust padding to fit the smaller text
    box_color = (50, 50, 50)  # Dark gray background for the boxes
    text_color = WHITE  # White text color

    for i, (key, function) in enumerate(tutorial_keys):
        # Create the box for the key-function pair
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = 150 + i * (box_height + padding)

        # Create gradient for each box
        for j in range(box_height):
            color = (0, 0, int(255 * (1 - j / box_height)))
            pygame.draw.line(screen, color, (box_x, box_y + j), (box_x + box_width, box_y + j))

        # Render the key and function text with the smaller font
        key_text = small_font.render(key, True, text_color)
        function_text = small_font.render(function, True, text_color)
        
        # Place the key text to the left and the function text to the right
        screen.blit(key_text, (box_x + 10, box_y + 10))
        screen.blit(function_text, (box_x + 150, box_y + 10))

    # Draw back arrow to go back to the menu (same as the one in the home screen)
    draw_back_arrow()

    # Update the display to reflect changes
    pygame.display.flip()


def handle_tutorial_click(pos):
    """Handles clicks on the tutorial page."""
    x, y = pos
    if 30 <= x <= 60 and 20 <= y <= 60:  # Back button area
        print("Back button clicked!")  # This will be printed when the back button is clicked
        return "menu"  # Go back to the menu screen

    return "tutorial"













class CelestialBody:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = deque(maxlen=200)

    def draw(self, screen, scale, visual_scale, offset_x, offset_y, trails_enabled):
        if trails_enabled and len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                pos1 = self.trail[i - 1]
                pos2 = self.trail[i]
                alpha = max(0, 255 - (i * (255 // len(self.trail))))
                trail_color = (self.color[0], self.color[1], self.color[2], alpha)
                # Draw a line between consecutive positions in the trail
                pygame.draw.line(screen, trail_color,
                             (int(pos1[0] * scale + offset_x), int(pos1[1] * scale + offset_y)),
                             (int(pos2[0] * scale + offset_x), int(pos2[1] * scale + offset_y)), 2)

        scaled_radius = max(2, int(self.radius * visual_scale))
        scaled_x = int(self.x * scale + offset_x)
        scaled_y = int(self.y * scale + offset_y)
        pygame.draw.circle(screen, self.color, (scaled_x, scaled_y), scaled_radius)




    def update_position(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trail.append((self.x, self.y))

    def update_acceleration(self, fx, fy):
        self.ax = fx / self.mass
        self.ay = fy / self.mass

    def is_clicked(self, mouse_x, mouse_y, scale, offset_x, offset_y):
        scaled_x = int(self.x * scale + offset_x)
        scaled_y = int(self.y * scale + offset_y)
        distance = math.sqrt((mouse_x - scaled_x) ** 2 + (mouse_y - scaled_y) ** 2)
        return distance <= max(5, int(self.radius * visual_scale))

def calculate_force(body1, body2):
    dx = body2.x - body1.x
    dy = body2.y - body1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return 0, 0
    force = G * body1.mass * body2.mass / distance**2
    angle = math.atan2(dy, dx)
    fx = force * math.cos(angle)
    fy = force * math.sin(angle)
    return fx, fy

def reset_simulation(bodies, initial_conditions):
    for i, body in enumerate(bodies):
        body.x, body.y, body.vx, body.vy = initial_conditions[i]
        body.ax = 0
        body.ay = 0
        body.trail.clear()

preset_1 = [
    CelestialBody(0, 0, 0, 0, 1.989e30, 30, YELLOW),
    CelestialBody(1.0e11, 0, 0, 25_000, 1.989e30, 30, (255, 165, 0)),
    CelestialBody(-1.0e11, 0, 0, -25_000, 1.989e30, 30, (255, 255, 255))
]

preset_2 = [
    CelestialBody(1.0e10, 0, 0, 0, 1.989e30, 30, YELLOW),
    CelestialBody(1.9e11, 0, 0, 25_000, 3e30, 30, (255, 165, 0)),
    CelestialBody(-1.0e11, 0, 0, -25_000, 2.989e30, 30, (255, 255, 255))
]

preset_3 = [
    # Body 1: Large central body
    CelestialBody(0, 0, 0, 0, 5.0e30, 35, YELLOW),  # Central body with significant mass

    # Body 2: Medium-sized body
    CelestialBody(1.2e11, 0, 0, 25_000, 3.0e30, 30, (255, 165, 0)),  # Orange body, orbiting central body

    # Body 3: Smaller body
    CelestialBody(-1.0e11, 0, 0, -35_000, 1.5e30, 25, (135, 206, 250)),  # Light blue body with higher velocity
]

preset_binary_system = [
    # Star 1: Binary pair
    CelestialBody(-5.0e10, 0, 0, 15_000, 2.0e30, 25, (255, 215, 0)),  # Yellow star

    # Star 2: Binary pair
    CelestialBody(5.0e10, 0, 0, -15_000, 2.0e30, 25, (255, 165, 0)),  # Orange star

    # Star 3: Orbiting the binary system
    CelestialBody(0, -3.0e11, 8_000, 0, 1.9e30, 20, (135, 206, 250)),  # Light blue star
]



initial_conditions_1 = [
    (0, 0, 0, 0),
    (1.0e11, 0, 0, 25_000),
    (-1.0e11, 0, 0, -25_000)
]

initial_conditions_2 = [
    (1.0e10, 0, 0, 0),
    (1.9e11, 0, 0, 25_000),
    (-1.0e11, 0, 0, -25_000)
]

initial_conditions_3 = [
    (0, 0, 0, 0),  # Central body
    (1.2e11, 0, 0, 25_000),  # Medium-sized body
    (-1.0e11, 0, 0, -35_000),  # Smaller body
]

initial_conditions_binary_system = [
    (-5.0e10, 0, 0, 15_000),  # Yellow star 
    (5.0e10, 0, 0, -15_000),  # Orange star
    (0, -3.0e11, 8_000, 0),  # Light blue star
]


bodies_solar_system = [
    # Main simulation setup
    CelestialBody(0, 0, 0, 0, 1.989e30, 30, YELLOW),  # Sun, 30 pixels radius

    # Mercury: closest to the Sun (no moons)
    CelestialBody(5.791e10, 0, 0, 47_870, 3.301e23, 5, (169, 169, 169)),  # Grayish color

    # Venus: second planet from the Sun (no moons)
    CelestialBody(1.082e11, 0, 0, 35_020, 4.867e24, 12, (255, 215, 0)),  # Yellowish color

    # Earth: third planet from the Sun
    CelestialBody(1.496e11, 0, 0, 29_800, 5.972e24, 10, (0, 0, 255)),  # Blue color
    # Earth's moons
    CelestialBody(1.496e11 + 3.844e8, 0, 0, 29_800 + 1_022, 7.348e22, 2, GRAY),  # Moon

    # Mars: fourth planet from the Sun
    CelestialBody(2.279e11, 0, 0, 24_077, 6.417e23, 8, (255, 0, 0)),  # Red color


]




if random_preset == 1:
    bodies = preset_1
elif random_preset == 2:
    bodies = preset_2
elif random_preset == 3:
    bodies = preset_3

def draw_game_screen(bodies, scale, visual_scale, offset_x, offset_y, trails_enabled, paused):
    screen.fill(BLACK)

    for body in bodies:
        body.draw(screen, scale, visual_scale, offset_x, offset_y, trails_enabled)

    if paused:
        paused_text = font.render("PAUSED", True, red_text)
        screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

def handle_game_screen_click(pos, bodies, scale, offset_x, offset_y, locked_body):
    x, y = pos
    for body in bodies:
        if body.is_clicked(x, y, scale, offset_x, offset_y):
            # Lock the camera view on the clicked body
            return body  # Return the locked body
    return locked_body  # If no body is clicked, return the previous locked body


def main():
    running = True
    current_screen = "menu"
    bodies = []
    dt = 86400
    scale = 1e-7
    visual_scale = 1
    offset_x = SCREEN_WIDTH // 2
    offset_y = SCREEN_HEIGHT // 2
    trails_enabled = False
    locked_body = None  # Initially no body is locked
    paused = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if current_screen == "menu":
                    current_screen = handle_main_menu_click((x, y))
                elif current_screen == "presets":
                    preset = handle_presets_click((x, y))
                    if preset == "solar_system":
                        bodies = bodies_solar_system
                        current_screen = "game"
                        paused = False
                    elif preset == "three_body":
                        if random_preset == 1:
                            bodies = preset_1
                        elif random_preset == 2:
                            bodies = preset_2
                        elif random_preset == 3:
                            bodies = preset_3
                        elif random_preset == 4:
                            bodies = preset_binary_system 
                        current_screen = "game"
                        paused = False
                    elif preset == "menu":
                        current_screen = "menu"
                    elif current_screen == "tutorial":
                        current_screen = handle_tutorial_click((x, y))
                elif current_screen == "game":
                    # Handle body click to lock view
                    locked_body = handle_game_screen_click((x, y), bodies, scale, offset_x, offset_y, locked_body)

            elif event.type == pygame.KEYDOWN:
                if current_screen == "game":
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        scale *= 1.25
                        visual_scale *= 1.1
                    elif event.key == pygame.K_MINUS:
                        scale /= 1.25
                        visual_scale /= 1.1
                    elif event.key == pygame.K_ESCAPE:
                        locked_body = None  # Unlock body when pressing ESC
                        offset_x = SCREEN_WIDTH // 2
                        offset_y = SCREEN_HEIGHT // 2
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_t:
                        trails_enabled = not trails_enabled
                    elif event.key == pygame.K_s and dt <= 86400:
                        dt *= 1.1
                    elif event.key == pygame.K_d and dt >= 600:
                        dt /= 1.1
                    elif event.key == pygame.K_r:
                        if bodies == preset_1:
                            reset_simulation(bodies, initial_conditions_1)
                        elif bodies == preset_2:
                            reset_simulation(bodies, initial_conditions_2)
                        elif bodies == preset_3:
                            reset_simulation(bodies, initial_conditions_3)
                        elif bodies == preset_binary_system:
                            reset_simulation(bodies, initial_conditions_binary_system)

        if current_screen == "menu":
            draw_main_menu()
        elif current_screen == "presets":
            draw_presets()
        elif current_screen == "tutorial":
            draw_tutorial_screen()
        elif current_screen == "game":
            if locked_body:
                # Keep the view locked on the selected body
                offset_x = SCREEN_WIDTH // 2 - locked_body.x * scale
                offset_y = SCREEN_HEIGHT // 2 - locked_body.y * scale
            if not paused:
                # Perform simulation updates
                for body in bodies:
                    body.ax = 0
                    body.ay = 0
                for i, body1 in enumerate(bodies):
                    for j, body2 in enumerate(bodies):
                        if i != j:
                            fx, fy = calculate_force(body1, body2)
                            body1.ax += fx / body1.mass
                            body1.ay += fy / body1.mass
                for body in bodies:
                    body.update_position(dt)

            draw_game_screen(bodies, scale, visual_scale, offset_x, offset_y, trails_enabled, paused)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()