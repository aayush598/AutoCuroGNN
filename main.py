import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import networkx as nx
import random

# Define bin dimensions
BIN_WIDTH = 80
BIN_HEIGHT = 40

# Define rectangles with random dimensions (width, height)
rectangles = {
    1: (random.randint(5, 15), random.randint(5, 10)),
    2: (random.randint(5, 15), random.randint(5, 10)),
    3: (random.randint(5, 15), random.randint(5, 10)),
    4: (random.randint(5, 15), random.randint(5, 10)),
    5: (random.randint(5, 15), random.randint(5, 10)),
    6: (random.randint(5, 15), random.randint(5, 10)),
    7: (random.randint(5, 15), random.randint(5, 10)),
    8: (random.randint(5, 15), random.randint(5, 10)),
    9: (random.randint(5, 15), random.randint(5, 10))
}

# Check if two rectangles overlap
def is_overlapping(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1 + w1 + 1 <= x2 or x2 + w2 + 1 <= x1 or
                y1 + h1 + 1 <= y2 or y2 + h2 + 1 <= y1)

# Adjust position to prevent overlap
def adjust_position(placements, rect, x, y, w, h):
    for other_rect, (ox, oy) in placements.items():
        ow, oh = rectangles[other_rect]
        while is_overlapping(x, y, w, h, ox, oy, ow, oh):
            x = random.randint(0, BIN_WIDTH - w)
            y = random.randint(0, BIN_HEIGHT - h)
    return x, y

# Initialize placements with overlap prevention
def initialize_placements():
    placements = {}
    placements[1] = (random.randint(0, BIN_WIDTH - rectangles[1][0]), 0)  # Top
    placements[2] = (random.randint(0, BIN_WIDTH - rectangles[2][0]), BIN_HEIGHT - rectangles[2][1])  # Bottom
    for rect in range(3, 10):
        x, y = random.randint(0, BIN_WIDTH - rectangles[rect][0]), random.randint(0, BIN_HEIGHT - rectangles[rect][1])
        x, y = adjust_position(placements, rect, x, y, rectangles[rect][0], rectangles[rect][1])
        placements[rect] = (x, y)
    return placements

placements = initialize_placements()

# Create a graph to define constraints
G = nx.Graph()
for rect in rectangles.keys():
    G.add_node(rect)

# Add edges based on constraints
constraints = [
    (3, 4), (3, 5), (3, 9),  # Rectangle 3 close to 4, 5, 9
    (7, 6), (7, 2)           # Rectangle 7 close to 6, 2
]
G.add_edges_from(constraints)

# Plot placements
def plot_placements(placements, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, BIN_WIDTH)
    ax.set_ylim(0, BIN_HEIGHT)
    for rect, (x, y) in placements.items():
        w, h = rectangles[rect]
        rect_patch = plt.Rectangle((x, y), w, h, edgecolor='blue', facecolor='lightblue', lw=2)
        ax.add_patch(rect_patch)
        ax.text(x + w / 2, y + h / 2, f"{rect}", ha='center', va='center', color='black')
    ax.set_title(title)
    ax.set_aspect('equal')
    plt.savefig(f"{title}.png")

plot_placements(placements, "initial_placement")

# Reinforcement learning placeholder to refine placements
def reinforcement_learning(G, placements, rectangles):
    for rect, (x, y) in placements.items():
        neighbors = list(G.neighbors(rect))
        for neighbor in neighbors:
            nx, ny = placements[neighbor]
            dist = distance.euclidean((x, y), (nx, ny))
            if dist < 10:  # Minimum distance constraint
                new_x = min(x + random.randint(1, 5), BIN_WIDTH - rectangles[rect][0])
                new_y = min(y + random.randint(1, 5), BIN_HEIGHT - rectangles[rect][1])
                new_x, new_y = adjust_position(placements, rect, new_x, new_y, rectangles[rect][0], rectangles[rect][1])
                placements[rect] = (new_x, new_y)
    return placements

optimized_placements = reinforcement_learning(G, placements, rectangles)
plot_placements(optimized_placements, "optimized_placement")

