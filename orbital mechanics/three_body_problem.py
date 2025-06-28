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

G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

# Pygame setup
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulator")

clock = pygame.time.Clock()
scale = 1e-7 # Scale for rendering (1 pixel = 1 billion meters)
visual_scale = 1  # Visual scale multiplier for radius
dt = 86400  # Initial time step in seconds
zoom_factor_visual = 1.1  # Zoom multiplier for visual appearance (radius)
zoom_factor_distance = 1.25  # Zoom multiplier for distance (positions)

# Initial trail settings
MAX_TRAIL_LENGTH = 100  # Max number of trail positions to store

class CelestialBody:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.radius = radius  # Radius in pixels
        self.color = color
        self.trail = deque(maxlen=MAX_TRAIL_LENGTH)  # Store past positions for trail

    def draw(self, screen, scale, visual_scale, offset_x, offset_y, trails_enabled):
        # Draw the trail if enabled
        if trails_enabled:
            for i, pos in enumerate(self.trail):
                # Fade the trail with increasing age (lighter color for older positions)
                alpha = max(0, 255 - (i * (255 // MAX_TRAIL_LENGTH)))
                trail_color = (self.color[0], self.color[1], self.color[2], alpha)
                pygame.draw.circle(screen, trail_color, (int(pos[0] * scale + offset_x), int(pos[1] * scale + offset_y)), 2)
        
        # Adjust the radius based on the visual scale only
        scaled_radius = max(2, int(self.radius * visual_scale))  # Apply only visual scale to radius
        scaled_x = int(self.x * scale + offset_x)
        scaled_y = int(self.y * scale + offset_y)
        pygame.draw.circle(screen, self.color, (scaled_x, scaled_y), scaled_radius)

    def update_position(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trail.append((self.x, self.y))  # Store the current position for the trail

    def update_acceleration(self, fx, fy):
        self.ax = fx / self.mass
        self.ay = fy / self.mass

    def is_clicked(self, mouse_x, mouse_y, scale, offset_x, offset_y):
        scaled_x = int(self.x * scale + offset_x)
        scaled_y = int(self.y * scale + offset_y)
        distance = math.sqrt((mouse_x - scaled_x) ** 2 + (mouse_y - scaled_y) ** 2)
        return distance <= max(5, int(self.radius * visual_scale))  # Adjust click radius based on zoom

def calculate_force(body1, body2):
    dx = body2.x - body1.x
    dy = body2.y - body1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return 0, 0  # Avoid division by zero
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
        body.trail.clear()  # Clear the trail


preset_1 =  [# Main simulation setup
    CelestialBody(0, 0, 0, 0, 1.989e30, 30, YELLOW),  # Sun 1, 30 pixels radius

    # Sun 2 (added)
    CelestialBody(1.0e11, 0, 0, 25_000, 1.989e30, 30, (255, 165, 0)),  # Sun-like body 2, orange color, offset to the right

    # Sun 3 (added)
    CelestialBody(-1.0e11, 0, 0, -25_000, 1.989e30, 30, (255, 255, 255))]
     
      # Sun-like body 3, white color, offset to the left


preset_2 = [# Main simulation setup
    CelestialBody(1.0e10, 0, 0, 0, 1.989e30, 30, YELLOW),  # Sun 1, 30 pixels radius

    # Sun 2 (added)
    CelestialBody(1.9e11, 0, 0, 25_000, 3e30, 30, (255, 165, 0)),  # Sun-like body 2, orange color, offset to the right

    # Sun 3 (added)
    CelestialBody(-1.0e11, 0, 0, -25_000, 2.989e30, 30, (255, 255, 255))]

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


if random_preset == 1:
    bodies = preset_1
elif random_preset == 2:
    bodies = preset_2
elif random_preset == 3:
    bodies = preset_3
elif random_preset == 4:
    bodies = preset_binary_system




# Store initial conditions for resetting
initial_conditions_1 = [
    (0, 0, 0, 0),  # Sun 1
    (1.0e11, 0, 0, 25_000),  # Sun 2
    (-1.0e11, 0, 0, -25_000),  # Sun 3
]

initial_conditions_2 = [
    (1.0e10, 0, 0, 0),  # Sun 1
    (1.9e11, 0, 0, 25_000),  # Sun 2
    (-3.0e11, 0, 0, -25_000),  # Sun 3
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


# Center the system on the screen
offset_x = WIDTH // 2
offset_y = HEIGHT // 2

# Track the locked celestial body
locked_body = None
paused = True
font = pygame.font.SysFont("Arial", 50)
simulation_speed = 1
running = True
trails_enabled = False  # Trails are off by default

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Zoom in and out
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                scale *= zoom_factor_distance  # Affect position
                visual_scale *= zoom_factor_visual  # Affect visual size
            elif event.key == pygame.K_MINUS:
                scale /= zoom_factor_distance  # Affect position
                visual_scale /= zoom_factor_visual  # Affect visual size
            # Lock/unlock a body
            elif event.key == pygame.K_ESCAPE:
                locked_body = None
                offset_x = WIDTH // 2
                offset_y = HEIGHT // 2
            # Pause toggle
            if event.key == pygame.K_p:
                paused = not paused
            # Toggle trails visibility
            if event.key == pygame.K_t:
                trails_enabled = not trails_enabled
            # Speed up time step with D, slow down with S, adjust trail length
            if event.key == pygame.K_s and dt <= 86400:  # Speed up the timestep
                dt *= 1.1  # Increase the timestep
                MAX_TRAIL_LENGTH = max(1, int(MAX_TRAIL_LENGTH * 1.1))  # Increase the trail length proportionally
            elif event.key == pygame.K_d and dt >= 600:  # Slow down the timestep
                dt /= 1.1  # Decrease the timestep
                MAX_TRAIL_LENGTH = max(1, int(MAX_TRAIL_LENGTH / 1.1))  # Decrease the trail length proportionally
            # Reset simulation when 'R' is pressed
            elif event.key == pygame.K_r:
                if random_preset == 1:
                    reset_simulation(bodies, initial_conditions_1)
                elif random_preset == 2:
                    reset_simulation(bodies, initial_conditions_2)
                elif random_preset == 3:
                    reset_simulation(bodies, initial_conditions_3)
                elif random_preset == 4:
                    reset_simulation(bodies, initial_conditions_binary_system)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for body in bodies:
                    if body.is_clicked(mouse_x, mouse_y, scale, offset_x, offset_y):
                        locked_body = body
                        print(f"Locked on {body.color} body at ({body.x}, {body.y})")
                        break

    # Reset accelerations
    for body in bodies:
        body.ax = 0
        body.ay = 0

    if not paused:
        # Calculate forces and update accelerations
        for i, body1 in enumerate(bodies):
            for j, body2 in enumerate(bodies):
                if i != j:  # Don't calculate the force for a body against itself
                    fx, fy = calculate_force(body1, body2)
                    body1.ax += fx / body1.mass
                    body1.ay += fy / body1.mass

        # Update positions
        for body in bodies:
            body.update_position(dt)

    # Adjust offset if a body is locked
    if locked_body:
        offset_x = WIDTH // 2 - int(locked_body.x * scale)
        offset_y = HEIGHT // 2 - int(locked_body.y * scale)

    # Drawing
    WIN.fill(BLACK)
    for body in bodies:
        body.draw(WIN, scale, visual_scale, offset_x, offset_y, trails_enabled)

    if paused:
        paused_text = font.render("PAUSED", True, red_text)
        WIN.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()