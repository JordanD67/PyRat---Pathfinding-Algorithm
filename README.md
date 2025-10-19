# PyRat Pathfinding game

<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/aadf7463-677e-42a4-b5b4-368d079797bf" />

## Overview
This repository contains the Python implementation of an AI strategy designed for the **PyRat maze game**. The strategy, referred to as **Hybrid Explorer**, combines **density-based initial movement** with a **Greedy Shortest Path** approach to maximize cheese collection.

This implementation uses several standard graph algorithms (Dijkstra's, BFS-like routing) and a custom density calculation to determine the optimal path.

---

## Strategy Description
The algorithm operates in **two main phases**:

### Phase 1: Density-Based Exploration (Preprocessing & Initial Turns)
- **Goal:** Move the player toward the most dense area of cheese on the map (determined during preprocessing).
- **Density Calculation (`densité` function):** The map is scanned to calculate the concentration of cheese within a square window (size `n=13` in the current configuration).
- **Initial Target:** The center of the square with the highest cheese count (`initial_vertex`) is set as the primary target.
- **Movement:** The player attempts to move to this `initial_vertex`.
- **Proximity Check:** If a piece of cheese is within a short range (distance ≤ 4), the player takes a detour to collect it first (Shortest Path to Closest Cheese).
- **Fallback:** If no cheese is close enough, the player continues moving toward the high-density `initial_vertex` using the shortest path found by Dijkstra's algorithm.

### Phase 2: Greedy Shortest Path (After Reaching High-Density Zone)
- **Switch Condition:** Once `initial_vertex` is in `all_explored_vertices`, the strategy switches to a purely greedy approach.
- **Shortest Path to Nearest Cheese:** In every turn, Dijkstra's algorithm is used to determine the exact shortest path to the nearest uncollected cheese.
- **Movement:** The player moves one step along this shortest path.
- **Meta-Graph Optimization:** A meta-graph is built to calculate distances between all pairs of cheese locations (and the player's current location), ensuring greedy choices are cost-minimized.

---

## Technical Details
The core functionality relies on several modular functions:

- `dijkstra(start_vertex, graph)`: Implements Dijkstra's algorithm to find the shortest distance from a `start_vertex` to all reachable nodes, returning a `routing_table` (for path reconstruction) and `explored_vertices` (for distances).
- `build_meta_graph(maze_map, locations)`: Constructs a complete graph (meta-graph) where nodes are key cheese locations and edge weights are shortest path distances between them, using Dijkstra's output.
- `densité(...)`: Computes the density of cheese within a square window centered at a given vertex to determine the strategic starting point.
- `find_route(...)` / `find_route2(...)`: Reconstructs the actual sequence of coordinates (the route) between two locations based on the routing_table from Dijkstra's.

---

## Installation and Usage
For up-to-date installation and usage details, please refer to the official PyRat website.

To use this specific strategy:
1. Place the provided Python script (`densite.py`) in your PyRat client folder.
2. Configure your player settings to use the **turn function** from this file.

# About

This is the software of the course [PyRat](https://formations.imt-atlantique.fr/pyrat).

Original code by Vincent Gripon. 

# Installation and usage

For up to date installation and usage details, please refer to the PyRat website [here](https://formations.imt-atlantique.fr/pyrat/install/).
