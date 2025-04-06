import numpy as np
import trimesh

def create_icosahedron():
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Icosahedron vertices (scaled up by 2x)
    vertices = 2 * np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])
    
    # Normalize to unit sphere (optional, comment out if you want exact scaling)
    vertices /= np.linalg.norm(vertices, axis=1)[:, np.newaxis]
    
    # Generate edges using convex hull
    mesh = trimesh.convex.convex_hull(vertices)
    edges = mesh.edges_unique
    
    return vertices, edges

# Create icosahedron
ico_v, ico_e = create_icosahedron()

# Create wireframe (thin silver edges)
radius = 0.015  # Reduced from 0.03 to make edges thinner
edge_meshes = []

for edge in ico_e:
    cylinder = trimesh.creation.cylinder(
        radius=radius,
        segment=ico_v[edge],
        vertex_colors=[200, 200, 200, 255]  # Silver
    )
    edge_meshes.append(cylinder)

wireframe = trimesh.util.concatenate(edge_meshes)
wireframe.export('stls/icosahedron.stl')

print("Large thin icosahedron exported successfully!")