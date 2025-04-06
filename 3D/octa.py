import numpy as np
import trimesh

def create_octahedron():
    vertices = np.array([
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1]
    ])
    faces = np.array([
        [0, 2, 4],
        [0, 4, 3],
        [0, 3, 5],
        [0, 5, 2],
        [1, 2, 5],
        [1, 5, 3],
        [1, 3, 4],
        [1, 4, 2]
    ])
    octahedron = trimesh.Trimesh(vertices=vertices, faces=faces)
    octahedron.visual.face_colors = [0, 0, 255, 255]  # Blue color
    return octahedron

octahedron_mesh = create_octahedron()
octahedron_mesh.export('stls/octahedron.stl')