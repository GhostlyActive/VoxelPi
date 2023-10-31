import pygame
from PIL import Image
import math

# Load the height map and color map PNGs
height_map = Image.open("height_map.png")
color_map = Image.open("color_map.png").convert('RGB') 

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Function to render a vertical line on the screen
def draw_vertical_line(x, ytop, ybottom, color):
    pygame.draw.line(screen, color, (x, ytop), (x, ybottom))

def render(p, phi, height, horizon, scale_height, distance, screen_width, screen_height):
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

        for i in range(screen_width):
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

            pleft[0] += dx
            pleft[1] += dy

        # Go to next line and increase step size when you are far away
        z += dz
        dz += 0.01

# Camera parameters
camera_position = [400, 400]
camera_height = 10
horizon_line = 100
height_scale = 120
max_distance = 400
rotation_angle = 0
movement_speed = 5
rotation_speed = 0.06
height_increment = 10

# Dictionary to keep track of the current movement state
movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
} 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            elif event.key == pygame.K_SPACE:
                camera_height += height_increment
            
            # Rotation keys
            elif event.key == pygame.K_q:
                rotation_angle += rotation_speed
            elif event.key == pygame.K_e:
                rotation_angle -= rotation_speed
        
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

    screen.fill((0, 0, 0))  # Clear the screen

      # Update camera position based on the movement state
    if movement["up"]:
        camera_position[1] -= movement_speed
    if movement["down"]:
        camera_position[1] += movement_speed
    if movement["left"]:
        camera_position[0] -= movement_speed
    if movement["right"]:
        camera_position[0] += movement_speed

    render(camera_position, rotation_angle, camera_height, horizon_line, height_scale, max_distance, screen_width, screen_height)

    pygame.display.update()  # Update the display

pygame.quit()
