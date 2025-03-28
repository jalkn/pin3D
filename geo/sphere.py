import numpy as np
import trimesh

# --- Sphere ---
def create_sphere():
    """Creates a sphere mesh."""
    sphere = trimesh.creation.icosphere(radius=1.5)  # Use icosphere for a better mesh than uv_sphere
    sphere.visual.face_colors = [255, 0, 255, 255]  # Magenta color
    return sphere

sphere_mesh = create_sphere()

sphere_mesh.export('stls/sphere.stl')