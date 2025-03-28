import numpy as np
import trimesh

# --- Cylinder ---
def create_cylinder():
    """Creates a cylinder mesh."""
    cylinder = trimesh.creation.cylinder(radius=5, height=2)
    cylinder.visual.face_colors = [0, 255, 255, 255]  # Cyan color
    return cylinder

# --- Sphere ---
def create_sphere():
    """Creates a sphere mesh."""
    sphere = trimesh.creation.icosphere(radius=1.5)  # Use icosphere for a better mesh than uv_sphere
    sphere.visual.face_colors = [255, 0, 255, 255]  # Magenta color
    return sphere

# --- Create and export individual shapes ---
cylinder_mesh = create_cylinder()
sphere_mesh = create_sphere()

#cylinder_mesh.export('stls/cylinder.stl')
#sphere_mesh.export('stls/sphere.stl')

# --- Boolean Union ---
combined_mesh = cylinder_mesh + sphere_mesh  # Or use trimesh.boolean.union([cylinder_mesh, sphere_mesh]) for more complex scenarios

combined_mesh.visual.face_colors = [255, 255, 0, 255]  # Yellow color for the combined mesh
combined_mesh.export('stls/combined.stl')