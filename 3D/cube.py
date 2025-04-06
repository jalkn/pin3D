import numpy as np
import trimesh

def create_cube_tetrahedron_combo():
    # Cube vertices (edge length 2 centered at origin)
    cube_vertices = np.array([
        [ 1,  1,  1], [-1,  1,  1], [-1, -1,  1], [ 1, -1,  1],
        [ 1,  1, -1], [-1,  1, -1], [-1, -1, -1], [ 1, -1, -1]
    ])
    
    # Cube edges (12 edges)
    cube_edges = [
        [0,1], [1,2], [2,3], [3,0],  # Top face
        [4,5], [5,6], [6,7], [7,4],  # Bottom face
        [0,4], [1,5], [2,6], [3,7]   # Vertical edges
    ]
    
    # Tetrahedron vertices
    tet_vertices = np.array([
        [ 1,  1,  1],
        [-1, -1,  1],
        [-1,  1, -1],
        [ 1, -1, -1]
    ])
    
    # Tetrahedron edges (6 edges)
    tet_edges = [
        [0,1], [0,2], [0,3],
        [1,2], [1,3], [2,3]
    ]
    
    return cube_vertices, cube_edges, tet_vertices, tet_edges

# Create geometry
cube_v, cube_e, tet_v, tet_e = create_cube_tetrahedron_combo()

# Create thin cylinders for all edges
radius = 0.02  # Adjust thickness as needed
edge_meshes = []

# Add cube edges
for edge in cube_e:
    line = cube_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius, segment=line)
    edge_meshes.append(cylinder)

# Add tetrahedron edges (in a different color if desired)
for edge in tet_e:
    line = tet_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius*1.2, segment=line)  # Slightly thicker
    edge_meshes.append(cylinder)

# Combine all cylinders into a single mesh
wireframe = trimesh.util.concatenate(edge_meshes)

# Export as STL
wireframe.export('stls/combo.stl')

print("Successfully exported cube-tetrahedron combination as STL")