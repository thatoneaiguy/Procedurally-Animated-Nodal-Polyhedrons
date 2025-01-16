import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Nodal Polyhedra")
clock = pygame.time.Clock()

# Colors
BACKGROUND_COLOR = (30, 30, 30)
NODE_COLOR = (255, 255, 255)
LINE_COLOR = (255, 255, 255)
DOT_COLOR = (100, 100, 100)

# Variables
node_count = 1  # Start with a single node
radius = 350  # Radius of the polygon
center = (WIDTH // 2, HEIGHT // 2)  # Center of the screen
transition_duration = 1  # Duration in seconds for transitions
fps = 60  # Frames per second

# Background dots
num_dots = 100
dots = [{"pos": (random.randint(0, WIDTH), random.randint(0, HEIGHT)), "original": None} for _ in range(num_dots)]
for dot in dots:
    dot["original"] = dot["pos"]  # Store the original positions

# Animation state
current_positions = []  # Current positions of nodes
target_positions = []  # Target positions of nodes
elapsed_time = 0  # Timer for transition


def calculate_node_positions(count):
    """Calculate the target positions of nodes based on node_count."""
    if count == 1:
        return [center]

    positions = []
    angle_step = 2 * math.pi / count
    for i in range(count):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        positions.append((x, y))
    return positions


def lerp(a, b, t):
    """Linearly interpolate between a and b by t."""
    return a + (b - a) * t


def interpolate_positions():
    """Interpolate current positions toward target positions."""
    global elapsed_time, current_positions
    t = min(elapsed_time / transition_duration, 1)  # Progress (0 to 1)
    current_positions = [
        (lerp(current[0], target[0], t), lerp(current[1], target[1], t))
        for current, target in zip(current_positions, target_positions)
    ]


def push_away_dots():
    """Move background dots away from white nodes."""
    for dot in dots:
        x, y = dot["pos"]
        ox, oy = dot["original"]
        push_x, push_y = 0, 0

        # Check proximity to all nodes
        for node_x, node_y in current_positions:
            distance = math.sqrt((node_x - x) ** 2 + (node_y - y) ** 2)
            if distance < 100:  # Push threshold
                dx = x - node_x
                dy = y - node_y
                factor = max(1 - distance / 100, 0)  # Strength of the push
                push_x += dx * factor
                push_y += dy * factor

        # Apply the push or return to the original position
        if push_x != 0 or push_y != 0:
            dot["pos"] = (x + push_x * 0.1, y + push_y * 0.1)
        else:
            # Gradually return to original position
            dot["pos"] = (lerp(x, ox, 0.01), lerp(y, oy, 0.01))


def draw_background_dots():
    """Draw the background dots."""
    for dot in dots:
        pygame.draw.circle(screen, DOT_COLOR, (int(dot["pos"][0]), int(dot["pos"][1])), 3)


def draw_polygon():
    """Draw the polygon based on current node positions with gaps and rounded edges."""
    # Gap between the node and the line
    line_gap = 10

    for i in range(len(current_positions)):
        for j in range(i + 1, len(current_positions)):
            # Get node positions
            x1, y1 = current_positions[i]
            x2, y2 = current_positions[j]

            # Calculate the direction vector and its length
            dx, dy = x2 - x1, y2 - y1
            length = math.sqrt(dx**2 + dy**2)

            # Avoid division by zero
            if length == 0:
                continue

            # Normalize the vector and scale it by the gap
            dx /= length
            dy /= length
            start_x = x1 + dx * line_gap
            start_y = y1 + dy * line_gap
            end_x = x2 - dx * line_gap
            end_y = y2 - dy * line_gap

            # Draw the line
            pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 2)

            # Draw rounded edges
            pygame.draw.circle(screen, LINE_COLOR, (int(start_x), int(start_y)), 2)
            pygame.draw.circle(screen, LINE_COLOR, (int(end_x), int(end_y)), 2)

    # Draw nodes
    for node in current_positions:
        pygame.draw.circle(screen, NODE_COLOR, (int(node[0]), int(node[1])), 5)


# Initialize positions
current_positions = calculate_node_positions(node_count)
target_positions = current_positions.copy()

# Main loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    delta_time = clock.tick(fps) / 1000  # Time since last frame in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scrolling up
                node_count += 1

                # Calculate new positions for all nodes
                new_positions = calculate_node_positions(node_count)

                if len(new_positions) > len(current_positions):
                    # Determine the opposite position of the last node
                    if len(current_positions) > 0:
                        last_x, last_y = current_positions[-1]
                        opposite_x = 2 * center[0] - last_x
                        opposite_y = 2 * center[1] - last_y
                    else:
                        opposite_x, opposite_y = center  # Default to center if no nodes exist

                    # Add the new node at the opposite position
                    current_positions.append((opposite_x, opposite_y))

            elif event.y < 0 and node_count > 1:  # Scrolling down
                node_count -= 1
                # Trim current_positions to match the reduced node count
                current_positions = current_positions[:node_count]

                # Update target positions for new node count
            target_positions = calculate_node_positions(node_count)
            elapsed_time = 0  # Reset transition timer

    # Update positions during the transition
    if current_positions != target_positions:
        elapsed_time += delta_time
        interpolate_positions()
    else:
        current_positions = target_positions.copy()

    # Update and draw the background dots
    push_away_dots()
    draw_background_dots()

    # Draw the polygon
    draw_polygon()
    pygame.display.flip()

pygame.quit()
sys.exit()
