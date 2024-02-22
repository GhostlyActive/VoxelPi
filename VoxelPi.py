import pygame
from PIL import Image
import math
import numpy as np

clock = pygame.time.Clock()
# Load the height map and color map PNGs
height_map = Image.open("height_map.png").convert()
color_map = Image.open("color_map.png").convert('RGB') 



# Initialize Pygame
pygame.init()
# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick detected:", joystick.get_name())
else:
    print("No joystick detected")

Quality_High = 0.02
Quality_Low = 0.15
line_step_Distance = 200
graphics_quality = Quality_High



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

        line_step = 1 if z < line_step_Distance else 2  # Change the threshold and step size as needed


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

# Camera parameters
camera_position = [400, 400]
camera_height = 100
horizon_line = 100
height_scale = 120
max_distance = 400
rotation_angle = 0.0
movement_speed = 5
rotation_speed = 0.06
height_increment = 10

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
            if event.button == 0:
                movement["heightUp"] = True 
            # xbox B Button
            if event.button == 1:
                movement["heightDown"] = True 
            #Start
            if event.button == 6:
                #movement[""] = True
                if(graphics_quality == Quality_Low):
                    graphics_quality = Quality_High
                    max_distance = 400
                    line_step_Distance = 200
                elif(graphics_quality == Quality_High):
                    graphics_quality = Quality_Low
                    max_distance = 300
                    line_step_Distance = 150

            # DPadUp
            if event.button == 11:
                movement["up"] = True
            # DPadDown
            if event.button == 12:
                movement["down"] = True
            # DPadLeft
            if event.button == 13:
                movement["left"] = True 
            # DPadRight
            if event.button == 14:
                movement["right"] = True    
            # LB
            if event.button == 9:
                movement["rotateL"] = True
            # LR
            if event.button == 10:
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
            if event.button == 0:
                movement["heightUp"] = False 
            # xbox B Button
            if event.button == 1:
                movement["heightDown"] = False 
             # DPadUp
            if event.button == 11:
                movement["up"] = False
            # DPadDown
            if event.button == 12:
                movement["down"] = False 
            # DPadLeft
            if event.button == 13:
                movement["left"] = False 
            # DPadRight
            if event.button == 14:
                movement["right"] = False 
            # LB
            if event.button == 9:
                movement["rotateL"] = False  
            # LR
            if event.button == 10:
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

       
    render(camera_position, rotation_angle, camera_height, horizon_line, height_scale, max_distance, screen_width, screen_height)

    # Inside your game loop, after pygame.display.update()
    pygame.display.update()  # Update the display

   

    # Calculate and print the FPS
    fps = clock.get_fps()
    print(f"FPS: {fps:.2f}")

# Cap the frame rate (e.g., at 60 frames per second)
    clock.tick(30)


pygame.quit()
