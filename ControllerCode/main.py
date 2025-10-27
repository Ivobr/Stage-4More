import pygame

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick connected!")
    exit()

# Use the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read and print all axis values
    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()

    # to read sensor axis value
    for i in range(axes):
        axis_val = joystick.get_axis(i)
        print(f"Axis {i}: {axis_val:.3f}", end=" | ")
    print()  # Newline after each frame
    for i in range(buttons):
        button_val = joystick.get_button(i)
        if button_val == 1:
            print(f"Button {i}: {button_val:.3f}", end=" | ")
    print()

    pygame.time.wait(100)  # Slight delay for readability

pygame.quit()
