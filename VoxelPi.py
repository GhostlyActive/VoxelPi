import pygame
from PIL import Image
import math
import numpy as np

# Constants screen and graphics
QUALITY_HIGH = 0.02
QUALITY_LOW = 0.15
MIN_LINE_STEP_DISTANCE = 200
MAX_LINE_STEP_DISTANCE = 250
MAX_VIEW_DISTANCE = 600
MIN_VIEW_DISTANCE = 400
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Constants for initial camera parameters
INITIAL_CAMERA_POSITION = [512, 800]
INITIAL_CAMERA_HEIGHT = 78
INITIAL_HORIZON_LINE = 70
INITIAL_HEIGHT_SCALE = 350
INITIAL_MAX_DISTANCE = 600
INITIAL_ROTATION_ANGLE = 0.0
INITIAL_MOVEMENT_SPEED = 5
INITIAL_ROTATION_SPEED = 0.06
INITIAL_HEIGHT_INCREMENT = 10
MOUSE_SENSITIVITY = 0.005
VERTICAL_SENSITIVITY = 0.2
LINE_STEP_SMALL = 1
LINE_STEP_LARGE = 3

class Game:
    def __init__(self):
        self.graphics_quality = QUALITY_HIGH
        self.max_distance = MAX_VIEW_DISTANCE
        self.line_step_distance = MAX_LINE_STEP_DISTANCE
        self.camera = Camera(INITIAL_CAMERA_POSITION, INITIAL_CAMERA_HEIGHT, INITIAL_ROTATION_ANGLE, INITIAL_MOVEMENT_SPEED, INITIAL_ROTATION_SPEED, INITIAL_HEIGHT_INCREMENT, INITIAL_HORIZON_LINE, INITIAL_HEIGHT_SCALE, INITIAL_MAX_DISTANCE)

    def handle_event(self, event):
        # Mapping of keys/buttons to movement actions
        action_map = {
            pygame.K_w: ("up", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_s: ("down", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_a: ("left", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_d: ("right", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_q: ("rotateL", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_e: ("rotateR", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_y: ("heightUp", pygame.KEYDOWN, pygame.KEYUP),
            pygame.K_x: ("heightDown", pygame.KEYDOWN, pygame.KEYUP),
            XBOX_A_BUTTON: ("heightUp", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            XBOX_B_BUTTON: ("heightDown", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            DPAD_UP: ("up", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            DPAD_DOWN: ("down", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            DPAD_LEFT: ("left", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            DPAD_RIGHT: ("right", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            LB_BUTTON: ("rotateL", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP),
            LR_BUTTON: ("rotateR", pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP)
        }

        # Mouse movement event
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            x, y = event.rel
            self.camera.rotation_angle += x * -MOUSE_SENSITIVITY
            self.camera.height += y * -VERTICAL_SENSITIVITY

        # Mouse button press event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.camera.movement["up"] = True
            elif event.button == 3:  # Right mouse button
                self.camera.movement["down"] = True

        # Mouse button release event
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.camera.movement["up"] = False
            elif event.button == 3:  # Right mouse button
                self.camera.movement["down"] = False

        # Start button toggles graphics quality
        if event.type == pygame.JOYBUTTONDOWN and event.button == XBOX_START_BUTTON:
            if self.graphics_quality == QUALITY_LOW:
                self.graphics_quality = QUALITY_HIGH
                self.max_distance = MAX_VIEW_DISTANCE
                self.line_step_distance = MAX_LINE_STEP_DISTANCE
            elif self.graphics_quality == QUALITY_HIGH:
                self.graphics_quality = QUALITY_LOW
                self.max_distance = MIN_VIEW_DISTANCE
                self.line_step_distance = MIN_LINE_STEP_DISTANCE

        # Handle key/button presses and releases
        for key, (action, press_event, release_event) in action_map.items():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP] and hasattr(event, 'key') and event.key == key:
                self.camera.movement[action] = event.type == pygame.KEYDOWN
            elif event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP] and hasattr(event, 'button') and event.button == key:
                self.camera.movement[action] = event.type == pygame.JOYBUTTONDOWN


class Camera:
    def __init__(self, position, height, rotation_angle, movement_speed, rotation_speed, height_increment, horizon_line, height_scale, max_distance):
        self.position = position
        self.height = height
        self.rotation_angle = rotation_angle
        self.movement_speed = movement_speed
        self.rotation_speed = rotation_speed
        self.height_increment = height_increment
        self.horizon_line = horizon_line
        self.height_scale = height_scale
        self.max_distance = max_distance    
        self.movement = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "rotateL": False,
            "rotateR": False,
            "heightUp": False,
            "heightDown": False
        }

    def update_position(self):
        # Update camera position based on the movement state and rotation angle
        if self.movement["up"]:
            self.position[0] -= math.sin(self.rotation_angle) * self.movement_speed
            self.position[1] -= math.cos(self.rotation_angle) * self.movement_speed
        if movement["down"]:
            self.position[0] += math.sin(self.rotation_angle) * self.movement_speed
            self.position[1] += math.cos(self.rotation_angle) * self.movement_speed
        if movement["left"]:
            self.position[0] -= math.cos(self.rotation_angle) * self.movement_speed
            self.position[1] += math.sin(self.rotation_angle) * self.movement_speed
        if movement["right"]:
            self.position[0] += math.cos(self.rotation_angle) * self.movement_speed
            self.position[1] -= math.sin(self.rotation_angle) * self.movement_speed


        if movement["rotateL"]:
            self.rotation_angle += self.rotation_speed
        if movement["rotateR"]:
            self.rotation_angle -= self.rotation_speed
        if movement["heightUp"]:
            self.height += self.height_increment
        if movement["heightDown"]:
            self.height -= self.height_increment

        if self.rotation_angle < 0:
            self.rotation_angle += 2 * math.pi
        elif self.rotation_angle > 2 * math.pi:
            self.rotation_angle -= 2 * math.pi



# Constants for button codes
XBOX_A_BUTTON = 0
XBOX_B_BUTTON = 1
XBOX_START_BUTTON = 6
DPAD_UP = 11
DPAD_DOWN = 12
DPAD_LEFT = 13
DPAD_RIGHT = 14
LB_BUTTON = 9
LR_BUTTON = 10

# Dictionary to keep track of the current movement state
movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotateL": False,
    "rotateR": False,
    "heightUp": False,
    "heightDown": False
} 

# Initialize Pygame
pygame.init()

game = Game()

# Initialize clock
clock = pygame.time.Clock()

# Load the height map and color map PNGs
try:
    height_map = Image.open("height_map.png").convert()
    color_map = Image.open("color_map.png").convert('RGB')
except FileNotFoundError:
    print("Error: height_map.png or color_map.png not found.")
    exit(1)

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick detected:", joystick.get_name())
else:
    print("No joystick detected")

# Graphics settings
graphics_quality = QUALITY_HIGH
line_step_distance = MAX_LINE_STEP_DISTANCE



# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Function to render a vertical line on the screen
def draw_vertical_line(x, ytop, ybottom, color):
    """
    Draw a vertical line on the screen.

    Parameters:
    x (int): The x-coordinate of the line.
    ytop (int): The y-coordinate of the top of the line.
    ybottom (int): The y-coordinate of the bottom of the line.
    color (tuple): The color of the line.
    """
    pygame.draw.line(screen, color, (x, ytop), (x, ybottom))

# Function for rendering 3D scene
def render(p, phi, height, horizon, scale_height, distance, screen_width, screen_height):
    """
    Render the 3D scene.

    Parameters:
    camera_position (list): The camera position.
    phi (float): The camera rotation angle.
    height (int): The camera height.
    horizon (int): The horizon line.
    scale_height (int): The height scale.
    distance (int): The maximum rendering distance.
    screen_width (int): The screen width.
    screen_height (int): The screen height.
    """
    sinphi = math.sin(phi)
    cosphi = math.cos(phi)

    # Initialize visibility array. Y position for each column on screen
    ybuffer = [screen_height] * screen_width

    # Draw from front to the back (low z coordinate to high z coordinate)
    dz = 1.
    z = 1.
    while z < distance:
        pleft = [
            (-cosphi * z - sinphi * z) + p[0],
            (sinphi * z - cosphi * z) + p[1]
        ]
        pright = [
            (cosphi * z - sinphi * z) + p[0],
            (-sinphi * z - cosphi * z) + p[1]
        ]

        dx = (pright[0] - pleft[0]) / screen_width
        dy = (pright[1] - pleft[1]) / screen_width

        line_step = LINE_STEP_SMALL if z < line_step_distance else LINE_STEP_LARGE  # Change the threshold and step size as needed


        for i in range(0, screen_width, line_step):
            # Check if the current position is within the bounds of the maps
            if 0 <= int(pleft[0]) < height_map.width and 0 <= int(pleft[1]) < height_map.height:
                
                height_pixel = height_map.getpixel((int(pleft[0]), int(pleft[1])))

                color = color_map.getpixel((int(pleft[0]), int(pleft[1])))
                if isinstance(color, int):
                    color = (color, color, color)

                height_on_screen = (height - height_pixel) / z * scale_height + horizon
                if height_on_screen < ybuffer[i]:
                    draw_vertical_line(i, height_on_screen, ybuffer[i], color)
                    ybuffer[i] = height_on_screen

            pleft[0] += dx * line_step
            pleft[1] += dy * line_step

        # Go to next line and increase step size when you are far away
        z += dz
        dz += graphics_quality



def display_fps():
    fps = clock.get_fps()
    print(f"FPS: {fps:.2f}")
    pass


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

   
    screen.fill((0, 0, 0))  # Clear the screen

    game.camera.update_position()

    render(game.camera.position, game.camera.rotation_angle, game.camera.height, game.camera.horizon_line, game.camera.height_scale, game.camera.max_distance, SCREEN_WIDTH, SCREEN_HEIGHT)

    pygame.display.update()  # Update the display

    display_fps()

    clock.tick(30)  # Cap the frame rate (e.g., at 30 frames per second)

pygame.quit()
