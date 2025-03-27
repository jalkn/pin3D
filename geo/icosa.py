import numpy as np
import trimesh

phi = (1 + np.sqrt(5)) / 2  # Golden ratio

def create_icosahedron():
    """Creates an icosahedron mesh."""
    vertices = np.array([
        [0, 1, phi],
        [0, 1, -phi],
        [0, -1, phi],
        [0, -1, -phi],
        [1, phi, 0],
        [1, -phi, 0],
        [-1, phi, 0],
        [-1, -phi, 0],
        [phi, 0, 1],
        [phi, 0, -1],
        [-phi, 0, 1],
        [-phi, 0, -1]
    ])
    faces = np.array([
        [0, 8, 4],
        [0, 4, 6],
        [0, 6, 10],
        [0, 10, 2],
        [0, 2, 8],
        [1, 4, 8],
        [1, 8, 2],
        [1, 2, 11],
        [1, 11, 5],
        [1, 5, 4],
        [3, 6, 10],
        [3, 10, 11],
        [3, 11, 5],
        [3, 5, 9],
        [3, 9, 6],
        [7, 2, 10],
        [7, 10, 6],
        [7, 6, 9],
        [7, 9, 5],
        [7, 5, 11],
        [7, 11, 2] # Corrected face
    ])
    icosahedron = trimesh.Trimesh(vertices=vertices, faces=faces)
    icosahedron.visual.face_colors = [255, 0, 0, 255]  # Red color
    return icosahedron

icosahedron_mesh = create_icosahedron()
icosahedron_mesh.export('stls/icosahedron.stl')