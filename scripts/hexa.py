import numpy as np
import trimesh

def create_triangular_prism():
    vertices = np.array([
        [0, 0, 0],  # Base triangle
        [1, 0, 0],
        [0.5, np.sqrt(3)/2, 0],
        [0, 0, 1],  # Top triangle
        [1, 0, 1],
        [0.5, np.sqrt(3)/2, 1]
    ])
    faces = np.array([
        [0, 1, 2],  # Bottom face
        [3, 5, 4],  # Top face
        [0, 3, 1],  # Side faces
        [1, 3, 4],
        [1, 4, 2],
        [2, 4, 5],
        [2, 5, 0],
        [0, 5, 3]
    ])
    prism = trimesh.Trimesh(vertices=vertices, faces=faces)
    prism.visual.face_colors = [0, 0, 255, 255]  # Purple color
    return prism

prism_mesh = create_triangular_prism()
prism_mesh.export('stls/prism.stl')