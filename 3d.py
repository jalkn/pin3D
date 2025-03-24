import numpy as np
import trimesh
import pyvista as pv

def create_turtle():
    # Create shell (ellipsoid)
    shell = trimesh.creation.icosphere(subdivisions=2, radius=1.0)
    shell.vertices[:, 2] *= 0.6  # Flatten the sphere into an ellipsoid

    # Create head (sphere)
    head = trimesh.creation.icosphere(radius=0.3)
    head.apply_translation([1.2, 0, 0.3])

    # Create legs (spheres)
    leg_positions = [
        [0.5, 0.7, -0.5],  # Front right
        [0.5, -0.7, -0.5], # Front left
        [-0.7, 0.5, -0.5],  # Back right
        [-0.7, -0.5, -0.5]  # Back left
    ]
    legs = []
    for pos in leg_positions:
        leg = trimesh.creation.icosphere(radius=0.2)
        leg.apply_translation(pos)
        legs.append(leg)

    # Create tail (cone)
    tail = trimesh.creation.cone(radius=0.15, height=0.5)
    tail.apply_translation([-1.2, 0, -0.3])
    tail.apply_transform(trimesh.transformations.rotation_matrix(np.pi/6, [0, 1, 0]))

    # Combine all parts
    turtle = shell + head + sum(legs, trimesh.Trimesh()) + tail
    turtle.visual.face_colors = [100, 200, 100, 255]  # Green color

    return turtle

# Generate and export the turtle
turtle_mesh = create_turtle()
turtle_mesh.export('turtle.stl')  # Save as STL for 3D printing

# Visualize with PyVista
pv_mesh = pv.wrap(turtle_mesh)
pv_mesh.plot(color='green', smooth_shading=True)