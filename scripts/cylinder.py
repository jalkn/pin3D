import numpy as np
import trimesh

# --- Cylinder ---
def create_cylinder():
    """Creates a cylinder mesh."""
    cylinder = trimesh.creation.cylinder(radius=1, height=2)
    cylinder.visual.face_colors = [0, 255, 255, 255]  # Cyan color
    return cylinder

cylinder_mesh = create_cylinder()
cylinder_mesh.export('stls/cylinder.stl')
