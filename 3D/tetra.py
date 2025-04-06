import numpy as np
import trimesh

def create_tetrahedron():
    vertices = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 1],
        [1, 3, 2]
    ])
    tetrahedron = trimesh.Trimesh(vertices=vertices, faces=faces)
    tetrahedron.visual.face_colors = [0, 255, 0, 255]  # Green color
    return tetrahedron

tetrahedron_mesh = create_tetrahedron()
tetrahedron_mesh.export('stls/tetrahedron.stl')