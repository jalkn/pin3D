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

# Create octahedron
octahedron = create_octahedron()

# Create thin cylinders for each edge
radius = 0.02  # Adjust thickness as needed
edge_meshes = []

for edge in octahedron.edges_unique:
    # Get the two vertices of the edge
    line = octahedron.vertices[edge]
    # Create a cylinder along this edge
    cylinder = trimesh.creation.cylinder(radius=radius, segment=line)
    edge_meshes.append(cylinder)

# Combine all cylinders into a single mesh
wireframe = trimesh.util.concatenate(edge_meshes)

# Export as STL
wireframe.export('stls/octahedron_edges.stl')

print("Successfully exported octahedron edges as STL")