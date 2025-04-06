import numpy as np
import trimesh

def create_snake_segment(start, end, radius):
    """Create a smooth cylinder segment for the snake body."""
    return trimesh.creation.cylinder(radius=radius, segment=[start, end])

def create_spiral_serpent(start_pos, direction, length, radius, depth=0, max_depth=3, coils=2):
    """Generate a snake that recursively coils into smaller spirals."""
    if depth > max_depth:
        return []
    
    segments = []
    coil_radius = length * 0.2  # Radius of the spiral
    coil_length = length * 0.8  # Length of each coil
    
    # Generate points along a spiral
    theta = np.linspace(0, 2 * np.pi * coils, int(coils * 20))  # More points = smoother
    spiral_points = []
    for t in theta:
        # Spiral offset (circular motion perpendicular to direction)
        perpendicular = np.array([-direction[1], direction[0], 0])  # 90° rotation in XY
        spiral_offset = coil_radius * (np.cos(t) * perpendicular + np.sin(t) * np.array([0, 0, 1]))
        
        # Advance along the main direction
        advance = direction * (t / (2 * np.pi * coils)) * coil_length
        point = start_pos + advance + spiral_offset
        spiral_points.append(point)
    
    # Create segments between spiral points
    for i in range(len(spiral_points) - 1):
        segments.append(create_snake_segment(spiral_points[i], spiral_points[i+1], radius))
    
    # Recursively add smaller spirals at the end
    if depth < max_depth:
        new_direction = direction.copy()
        new_direction = np.array([new_direction[1], -new_direction[0], new_direction[2]])  # Rotate 90°
        segments += create_spiral_serpent(
            spiral_points[-1],  # Start at the end of the current spiral
            new_direction,
            length * 0.6,  # Smaller next spiral
            radius * 0.7,   # Thinner next spiral
            depth + 1,
            max_depth,
            coils
        )
    
    return segments

# Initial parameters (explicitly float64)
start_pos = np.array([0.0, 0.0, 0.0], dtype=np.float64)
direction = np.array([1.0, 0.0, 0.0], dtype=np.float64)  # Initial direction (X-axis)
length = 3.0  # Length of the main spiral
radius = 0.15  # Initial thickness

# Generate the spiral serpent
serpent_segments = create_spiral_serpent(start_pos, direction, length, radius, max_depth=2, coils=2)
spiral_serpent = trimesh.util.concatenate(serpent_segments)

# Export as STL
spiral_serpent.export('stls/spiral_serpent.stl')

print("Successfully exported Spiral Serpent as STL!")