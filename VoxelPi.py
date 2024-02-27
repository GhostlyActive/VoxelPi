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

# Camera parameters
camera_position = INITIAL_CAMERA_POSITION
camera_height = INITIAL_CAMERA_HEIGHT
horizon_line = INITIAL_HORIZON_LINE
height_scale = INITIAL_HEIGHT_SCALE
max_distance = INITIAL_MAX_DISTANCE
rotation_angle = INITIAL_ROTATION_ANGLE
movement_speed = INITIAL_MOVEMENT_SPEED
rotation_speed = INITIAL_ROTATION_SPEED
height_increment = INITIAL_HEIGHT_INCREMENT

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

        line_step = 1 if z < line_step_distance else 3  # Change the threshold and step size as needed


        for i in range(0, screen_width, line_step):
            # Check if the current position is within the bounds of the maps
            if 0 <= int(pleft[0]) < height_map.width and 0 <= int(pleft[1]) < height_map.height:
                
                height_pixel = height_map.getpixel((int(pleft[0]), int(pleft[1])))

                color = color_map.getpixel((int(pleft[0]), int(pleft[1])))
                if isinstance(color, int):
                    color = (color, color, color)

                height_on_screen = (height - height_pixel) / z * height_scale + horizon
                if height_on_screen < ybuffer[i]:
                    draw_vertical_line(i, height_on_screen, ybuffer[i], color)
                    ybuffer[i] = height_on_screen

            pleft[0] += dx * line_step
            pleft[1] += dy * line_step

        # Go to next line and increase step size when you are far away
        z += dz
        dz += graphics_quality


def handle_event(event):
    # Handle the event here...
    pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

         # Mouse movement event
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
            x, y = event.rel  # Get the relative movement of the mouse
            rotation_angle += x * -0.005  # Adjust the rotation angle based on mouse movement
            camera_height += y * -0.2 


        # Mouse button press event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                movement["up"] = True
            elif event.button == 3:  # Right mouse button
                movement["down"] = True

        # Mouse button release event
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                movement["up"] = False
            elif event.button == 3:  # Right mouse button
                movement["down"] = False

        # Check for key presses to move the camera
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                movement["up"] = True
            elif event.key == pygame.K_s:
                movement["down"] = True
            elif event.key == pygame.K_a:
                movement["left"] = True
            elif event.key == pygame.K_d:
                movement["right"] = True
            elif event.key == pygame.K_q:
                movement["rotateL"] = True
            elif event.key == pygame.K_e:
                movement["rotateR"] = True
            elif event.key == pygame.K_y:
                movement["heightUp"] = True
            elif event.key == pygame.K_x:
                movement["heightDown"] = True

        # Controller input down
        if event.type == pygame.JOYBUTTONDOWN:
            # xbox A Button
            if event.button == XBOX_A_BUTTON:
                movement["heightUp"] = True 
            # xbox B Button
            if event.button == XBOX_B_BUTTON:
                movement["heightDown"] = True 
            #Start
            if event.button == XBOX_START_BUTTON:
                #movement[""] = True
                if(graphics_quality == QUALITY_LOW):
                    graphics_quality = QUALITY_HIGH
                    max_distance = MAX_VIEW_DISTANCE
                    line_step_Distance = MAX_LINE_STEP_DISTANCE
                elif(graphics_quality == QUALITY_HIGH):
                    graphics_quality = QUALITY_LOW
                    max_distance = MAX_VIEW_DISTANCE
                    line_step_Distance = MIN_LINE_STEP_DISTANCE

            # DPadUp
            if event.button == DPAD_UP:
                movement["up"] = True
            # DPadDown
            if event.button == DPAD_DOWN:
                movement["down"] = True
            # DPadLeft
            if event.button == DPAD_LEFT:
                movement["left"] = True 
            # DPadRight
            if event.button == DPAD_RIGHT:
                movement["right"] = True    
            # LB
            if event.button == LB_BUTTON:
                movement["rotateL"] = True
            # LR
            if event.button == LR_BUTTON:
                movement["rotateR"] = True
   


        # Check for key releases to stop camera movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                movement["up"] = False
            elif event.key == pygame.K_s:
                movement["down"] = False
            elif event.key == pygame.K_a:
                movement["left"] = False
            elif event.key == pygame.K_d:
                movement["right"] = False
            elif event.key == pygame.K_q:
                movement["rotateL"] = False
            elif event.key == pygame.K_e:
                movement["rotateR"] = False
            elif event.key == pygame.K_y:
                movement["heightUp"] = False
            elif event.key == pygame.K_x:
                movement["heightDown"] = False

        # Controller input up
        if event.type == pygame.JOYBUTTONUP:
            # xbox A Button
            if event.button == XBOX_A_BUTTON:
                movement["heightUp"] = False 
            # xbox B Button
            if event.button == XBOX_B_BUTTON:
                movement["heightDown"] = False 
             # DPadUp
            if event.button == DPAD_UP:
                movement["up"] = False
            # DPadDown
            if event.button == DPAD_DOWN:
                movement["down"] = False 
            # DPadLeft
            if event.button == DPAD_LEFT:
                movement["left"] = False 
            # DPadRight
            if event.button == DPAD_RIGHT:
                movement["right"] = False 
            # LB
            if event.button == LB_BUTTON:
                movement["rotateL"] = False  
            # LR
            if event.button == LR_BUTTON:
                movement["rotateR"] = False      

    screen.fill((0, 0, 0))  # Clear the screen

    # Update camera position based on the movement state and rotation angle
    if movement["up"]:
        camera_position[0] -= math.sin(rotation_angle) * movement_speed
        camera_position[1] -= math.cos(rotation_angle) * movement_speed
    if movement["down"]:
        camera_position[0] += math.sin(rotation_angle) * movement_speed
        camera_position[1] += math.cos(rotation_angle) * movement_speed
    if movement["left"]:
        camera_position[0] -= math.cos(rotation_angle) * movement_speed
        camera_position[1] += math.sin(rotation_angle) * movement_speed
    if movement["right"]:
        camera_position[0] += math.cos(rotation_angle) * movement_speed
        camera_position[1] -= math.sin(rotation_angle) * movement_speed


    if movement["rotateL"]:
        rotation_angle += rotation_speed
    if movement["rotateR"]:
        rotation_angle -= rotation_speed
    if movement["heightUp"]:
       camera_height += height_increment
    if movement["heightDown"]:
        camera_height -= height_increment

    if rotation_angle < 0:
        rotation_angle += 2 * math.pi
    elif rotation_angle > 2 * math.pi:
        rotation_angle -= 2 * math.pi

       
    render(camera_position, rotation_angle, camera_height, horizon_line, height_scale, max_distance, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Inside your game loop, after pygame.display.update()
    pygame.display.update()  # Update the display

   

    # Calculate and print the FPS
    fps = clock.get_fps()
    print(f"FPS: {fps:.2f}")

    # Cap the frame rate (e.g., at 30 frames per second)
    clock.tick(30)


pygame.quit()
