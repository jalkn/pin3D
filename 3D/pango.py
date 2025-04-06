import numpy as np
import trimesh
from scipy.spatial.transform import Rotation

def hyperbolic_paraboloid(u, v, a=1, b=1):
    """Generate a hyperbolic paraboloid (saddle shape)."""
    return np.column_stack([a * u, b * v, u * v])

def create_hypar_scale(size=0.1, resolution=20):
    """Create a single hyperbolic paraboloid scale."""
    u = np.linspace(-1, 1, resolution) * size
    v = np.linspace(-1, 1, resolution) * size
    u, v = np.meshgrid(u, v)
    vertices = hyperbolic_paraboloid(u.flatten(), v.flatten())
    faces = []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            idx = i * resolution + j
            faces.append([idx, idx + 1, idx + resolution])
            faces.append([idx + 1, idx + resolution + 1, idx + resolution])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

def fibonacci_sphere_points(n=100):
    """Generate points on a sphere using the Fibonacci spiral."""
    indices = np.arange(n, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * indices / n)
    theta = np.pi * (1 + 5**0.5) * indices
    return np.column_stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)])

def create_hyperbolic_pangolin():
    """Construct the pangolin with hypar scales."""
    # Low-poly body (simplified ellipsoid)
    body = trimesh.creation.icosphere(subdivisions=1, radius=1.5)
    body.vertices[:, 2] *= 0.5  # Flatten into a pangolin shape
    
    # Generate scales
    scales = []
    scale_positions = fibonacci_sphere_points(n=200) * 1.6  # Arrange on a larger sphere
    for pos in scale_positions:
        if pos[2] < -0.2:  # Skip underside
            continue
        # Orient scale to point outward from body
        rotation = Rotation.align_vectors([[0, 0, 1]], [pos])[0].as_matrix()
        scale = create_hypar_scale(size=0.15)
        scale.vertices = scale.vertices.dot(rotation) + pos
        scales.append(scale)
    
    # Combine body and scales
    pangolin = trimesh.util.concatenate([body] + scales)
    return pangolin

# Create and export
pangolin = create_hyperbolic_pangolin()
pangolin.export("stls/pangolin.stl")
print("Hyperbolic pangolin exported!")