import numpy as np
import trimesh

# --- Hexahedron (Cuboid) ---
def create_hexahedron(width=3, length=3, height=3):
    """Creates a hexahedron (cuboid) mesh."""
    hexahedron = trimesh.creation.box(extents=[width, length, height])  # extents = [x, y, z] dimensions
    hexahedron.visual.face_colors = [255, 0, 0, 255]  # Red color
    return hexahedron

hexahedron_mesh = create_hexahedron()
hexahedron_mesh.export('stls/hexahedron.stl')