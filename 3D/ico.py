import numpy as np
import trimesh

def create_icosahedron():
    """Create a regular icosahedron."""
    t = (1.0 + np.sqrt(5.0)) / 2.0
    vertices = np.array([
        [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
        [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
        [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]
    ])
    faces = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

def recursive_fractal_cage(base_mesh, recursion_level=1, scale_factor=0.3, wire_thickness=0.02):
    """Recursively replace each edge with a scaled-down version of the base mesh."""
    all_meshes = []
    
    def process_edges(vertices, edges, current_level):
        if current_level >= recursion_level:
            return
        for edge in edges:
            # Get the two vertices of the edge
            v1, v2 = vertices[edge[0]], vertices[edge[1]]
            # Calculate midpoint and direction
            midpoint = (v1 + v2) / 2
            edge_length = np.linalg.norm(v2 - v1)
            # Scale down the base mesh
            scaled_mesh = base_mesh.copy()
            scaled_mesh.vertices *= scale_factor * edge_length
            # Rotate and position the scaled mesh along the edge
            direction = v2 - v1
            rotation = trimesh.transformations.rotation_matrix(
                np.arctan2(direction[1], direction[0]),
                [0, 0, 1],
                midpoint
            )
            scaled_mesh.apply_transform(rotation)
            # Add to the collection
            all_meshes.append(scaled_mesh)
            # Recurse into the new edges
            process_edges(scaled_mesh.vertices, scaled_mesh.edges, current_level + 1)
    
    # Start recursion
    process_edges(base_mesh.vertices, base_mesh.edges, 0)
    
    # Convert all edges into wireframe cylinders
    wireframe_parts = []
    for mesh in all_meshes:
        for edge in mesh.edges:
            line = mesh.vertices[edge]
            cylinder = trimesh.creation.cylinder(
                radius=wire_thickness,
                segment=line
            )
            wireframe_parts.append(cylinder)
    
    # Combine all wires into a single mesh
    return trimesh.util.concatenate(wireframe_parts)

# Create base icosahedron
base_icosahedron = create_icosahedron()

# Generate fractal cage (1 recursion level for clarity)
fractal_cage = recursive_fractal_cage(base_icosahedron, recursion_level=1, wire_thickness=0.01)

# Export as STL
fractal_cage.export('stls/fractal_cage.stl')

print("Successfully exported recursive fractal cage as STL!")