import numpy as np
import trimesh

def create_octahedron():
    vertices = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ])
    faces = np.array([
        [0, 2, 4], [0, 4, 3],
        [0, 3, 5], [0, 5, 2],
        [1, 2, 5], [1, 5, 3],
        [1, 3, 4], [1, 4, 2]
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

# Create octahedron and get edges
octahedron = create_octahedron()
edges = np.sort(octahedron.edges_unique, axis=1)
lines = octahedron.vertices[edges]

# Create and export wireframe
edge_path = trimesh.load_path(lines)
edge_path.export('stls/octahedron_edges.ply')

# Visualize (requires pyglet<2)
edge_path.show()