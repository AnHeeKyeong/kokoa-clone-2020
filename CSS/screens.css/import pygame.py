import pygame
import random
# Handle events

# Initialize pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define block size and grid dimensions
block_size = 30
grid_width = window_width // block_size
grid_height = window_height // block_size

# Define the Tetris grid
grid = [[BLACK] * grid_width for _ in range(grid_height)]

# Define the Tetrimino shapes
tetrimino_shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Define the Tetrimino colors
tetrimino_colors = [RED, GREEN, BLUE]

# Function to get tetrimino coordinates
def get_tetrimino_coordinates(shape):
    coordinates = []
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                coordinates.append((row_index, col_index))
    return coordinates

# Define the current Tetrimino
current_tetrimino = random.choice(tetrimino_shapes)
current_color = random.choice(tetrimino_colors)
current_x = grid_width // 2 - len(current_tetrimino[0]) // 2
current_y = 0

# Game loop
running = True
clock = pygame.time.Clock()
fall_speed = 0.5
fall_time = 0

while running:
    window.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic goes here
    # Move the current Tetrimino down
    fall_time += clock.get_rawtime()
    if fall_time / 1000 >= fall_speed:
        current_y += 1
        fall_time = 0

    # Check for collision with the bottom or other blocks
    collision_detected = False
    for row, col in get_tetrimino_coordinates(current_tetrimino):
        if row + current_y >= grid_height or grid[row + current_y][col + current_x] != BLACK:
            collision_detected = True
            break

    if collision_detected:
        # Collision detected, lock the Tetrimino in place
        for row, col in get_tetrimino_coordinates(current_tetrimino):
            grid[row + current_y - 1][col + current_x] = current_color

        # Check for completed lines
        completed_lines = []
        for row in range(grid_height):
            if all(color != BLACK for color in grid[row]):
                completed_lines.append(row)

        # Remove completed lines and add new ones at the top
        for row in completed_lines:
            del grid[row]
            grid.insert(0, [BLACK] * grid_width)

        # Spawn a new Tetrimino
        current_tetrimino = random.choice(tetrimino_shapes)
        current_color = random.choice(tetrimino_colors)
        current_x = grid_width // 2 - len(current_tetrimino[0]) // 2
        current_y = 0

        # Check for game over
        if any(grid[row + current_y][col + current_x] != BLACK for row, col in get_tetrimino_coordinates(current_tetrimino)):
            running = False

    # Draw the grid
    for row in range(grid_height):
        for col in range(grid_width):
            pygame.draw.rect(window, grid[row][col], (col * block_size, row * block_size, block_size, block_size))

    # Draw the current Tetrimino
    for row, col in get_tetrimino_coordinates(current_tetrimino):
        pygame.draw.rect(window, current_color, ((col + current_x) * block_size, (row + current_y) * block_size, block_size, block_size))

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()