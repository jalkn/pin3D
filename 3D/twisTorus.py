import numpy as np
import trimesh

def create_twisted_torus_wireframe(major_radius=3, minor_radius=1, twist=1, resolution=30, cylinder_radius=0.05):
    # Generate vertices along a twisted torus
    u = np.linspace(0, 2 * np.pi, resolution)  # Major (toroidal) angle
    v = np.linspace(0, 2 * np.pi, resolution)  # Minor (poloidal) angle
    
    vertices = []
    for i, u_val in enumerate(u):
        # Apply a twist that depends on the toroidal angle
        twist_angle = twist * u_val
        for j, v_val in enumerate(v):
            x = (major_radius + minor_radius * np.cos(v_val + twist_angle)) * np.cos(u_val)
            y = (major_radius + minor_radius * np.cos(v_val + twist_angle)) * np.sin(u_val)
            z = minor_radius * np.sin(v_val + twist_angle)
            vertices.append([x, y, z])
    
    vertices = np.array(vertices)
    
    # Create edges (connect adjacent points in u and v directions)
    edge_meshes = []
    for i in range(resolution):
        for j in range(resolution):
            # Connect to next point in u direction
            next_i = (i + 1) % resolution
            line_u = [vertices[i * resolution + j], vertices[next_i * resolution + j]]
            cylinder_u = trimesh.creation.cylinder(radius=cylinder_radius, segment=line_u)
            edge_meshes.append(cylinder_u)
            
            # Connect to next point in v direction
            next_j = (j + 1) % resolution
            line_v = [vertices[i * resolution + j], vertices[i * resolution + next_j]]
            cylinder_v = trimesh.creation.cylinder(radius=cylinder_radius, segment=line_v)
            edge_meshes.append(cylinder_v)
    
    # Combine all cylinders into a single mesh
    wireframe = trimesh.util.concatenate(edge_meshes)
    return wireframe

# Create and export the twisted torus wireframe
twisted_torus = create_twisted_torus_wireframe(twist=1.5)  # Adjust twist for more/less deformation
twisted_torus.export('stls/twisted_torus_wireframe.stl')

print("Successfully exported twisted torus wireframe as STL!")