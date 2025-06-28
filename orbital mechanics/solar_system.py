import pygame
import sys
import math
from collections import deque

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
scale = 1e-6  # Scale for rendering (1 pixel = 1 billion meters)
visual_scale = 1  # Visual scale multiplier for radius
dt = 1500  # Initial time step in seconds
zoom_factor_visual = 1.1  # Zoom multiplier for visual appearance (radius)
zoom_factor_distance = 1.25  # Zoom multiplier for distance (positions)

# Initial trail settings
MAX_TRAIL_LENGTH = 500  # Max number of trail positions to store

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

bodies = [
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
    # Mars' moons with corrected velocities
    CelestialBody(2.279e11 + 6e6, 0, 0, 24_077 + 2138, 1.08e16, 1, GRAY),  # Phobos
    CelestialBody(2.279e11 + 2.346e7, 0, 0, 24_077 + 1351.3 , 1.51e15, 1, BLUE),  # Deimos
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
            if event.key == pygame.K_s and dt <= 360:  # Speed up the timestep
                dt *= 1.1  # Increase the timestep
                MAX_TRAIL_LENGTH = max(1, int(MAX_TRAIL_LENGTH * 1.1))  # Increase the trail length proportionally
            elif event.key == pygame.K_d and dt >= 60:  # Slow down the timestep
                dt /= 1.1  # Decrease the timestep
                MAX_TRAIL_LENGTH = max(1, int(MAX_TRAIL_LENGTH / 1.1))  # Decrease the trail length proportionally
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

