import numpy as np
import trimesh

def create_dodecahedron_icosahedron_combo():
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Icosahedron vertices (12 vertices)
    icosahedron_vertices = np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])
    
    # Icosahedron edges (30 edges - we'll use convex hull to find them)
    icosahedron = trimesh.convex.convex_hull(icosahedron_vertices)
    icosahedron_edges = np.vstack([icosahedron.edges_unique])
    
    # Dodecahedron vertices (20 vertices)
    dodecahedron_vertices = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, 1/phi, phi], [0, -1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, -phi],
        [1/phi, phi, 0], [-1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, -phi, 0],
        [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi]
    ])
    
    # Scale down the dodecahedron to fit inside
    dodecahedron_vertices *= 0.8
    
    # Dodecahedron edges (30 edges - again using convex hull)
    dodecahedron = trimesh.convex.convex_hull(dodecahedron_vertices)
    dodecahedron_edges = np.vstack([dodecahedron.edges_unique])
    
    return icosahedron_vertices, icosahedron_edges, dodecahedron_vertices, dodecahedron_edges

# Create geometry
ico_v, ico_e, dod_v, dod_e = create_dodecahedron_icosahedron_combo()

# Create thin cylinders for all edges
radius = 0.02
edge_meshes = []

# Add icosahedron edges (outer shape)
for edge in ico_e:
    line = ico_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius, segment=line)
    edge_meshes.append(cylinder)

# Add dodecahedron edges (inner shape, slightly thicker and different color)
for edge in dod_e:
    line = dod_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius*1.5, segment=line)
    edge_meshes.append(cylinder)

# Combine all cylinders
wireframe = trimesh.util.concatenate(edge_meshes)

# Export as STL
wireframe.export('stls/dodeca.stl')

print("Successfully exported dodecahedron-icosahedron combination as STL")