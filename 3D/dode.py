import numpy as np
import trimesh

def create_dodecahedron():
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Dodecahedron vertices (scaled up by 2x)
    vertices = 2 * np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, 1/phi, phi], [0, -1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, -phi],
        [1/phi, phi, 0], [-1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, -phi, 0],
        [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi]
    ])
    
    # Scale down to fit inside icosahedron (remove this line for full size)
    scale_factor = (phi ** 2) / np.sqrt(3)
    vertices /= scale_factor
    
    # Generate edges using convex hull
    mesh = trimesh.convex.convex_hull(vertices)
    edges = mesh.edges_unique
    
    return vertices, edges

# Create dodecahedron
dod_v, dod_e = create_dodecahedron()

# Create wireframe (thin orange edges)
radius = 0.02  # Reduced from 0.04 to make edges thinner
edge_meshes = []

for edge in dod_e:
    cylinder = trimesh.creation.cylinder(
        radius=radius,
        segment=dod_v[edge],
        vertex_colors=[255, 100, 0, 255]  # Orange
    )
    edge_meshes.append(cylinder)

wireframe = trimesh.util.concatenate(edge_meshes)
wireframe.export('stls/dodecahedron.stl')

print("Large thin dodecahedron exported successfully!")