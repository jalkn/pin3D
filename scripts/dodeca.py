import numpy as np
import trimesh

phi = (1 + np.sqrt(5)) / 2  # Golden ratio

vertices = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
    [0, -phi, -1/phi], [0, phi, -1/phi], [0, -phi, 1/phi], [0, phi, 1/phi],
    [-phi, -1/phi, 0], [phi, -1/phi, 0], [-phi, 1/phi, 0], [phi, 1/phi, 0],
    [-1/phi, 0, -phi], [1/phi, 0, -phi], [-1/phi, 0, phi], [1/phi, 0, phi]
])

faces = np.array([
    [0, 16, 2, 18, 1], [1, 18, 9, 11, 3], [0, 1, 3, 5, 4],
    [0, 4, 12, 14, 16], [4, 5, 7, 13, 12], [1, 10, 6, 7, 3],
    [2, 17, 8, 10, 1], [2, 16, 14, 15, 17], [5, 3, 11, 19, 7],
    [6, 10, 8, 15, 9], [17, 15, 13, 12, 4], [6, 8, 9, 11, 19],
    [13, 15, 14, 12, 13], [18, 2, 17, 8, 9], [19, 11, 10, 8, 9],
    [19, 7, 6, 9, 11], [13, 7, 5, 4, 12] #removed duplicate [18, 9, 6, 7, 5], [18, 1, 0, 4, 5]
])


def create_dodecahedron():
    # Triangulate the faces because Trimesh expects triangles
    triangulated_faces = []
    for face in faces:
        for i in range(1, len(face) - 1):
            triangulated_faces.append([face[0], face[i], face[i+1]])
    
    dodecahedron = trimesh.Trimesh(vertices=vertices, faces=np.array(triangulated_faces))
    dodecahedron.visual.face_colors = [255, 255, 0, 255] # Yellow
    return dodecahedron


dodecahedron_mesh = create_dodecahedron()
dodecahedron_mesh.export('stls/dodecahedron.stl')