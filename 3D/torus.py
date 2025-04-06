import numpy as np
import trimesh

def create_twisted_torus_wireframe(major_radius=3, minor_radius=1, 
                                 twists=5, resolution=100, wire_thickness=0.05):
    """
    Creates a torus where the circular cross-section is replaced with a 
    twisting square wireframe.
    
    Parameters:
    - major_radius: Radius of the entire torus
    - minor_radius: Radius of the twisting square frame
    - twists: Number of full twists in the torus
    - resolution: Number of segments along the torus
    - wire_thickness: Thickness of the wireframe edges
    """
    
    # Create the vertices for a square that will twist around the torus
    theta = np.linspace(0, 2*np.pi, resolution, endpoint=False)
    
    # Initialize list for all wireframe cylinders
    all_wires = []
    
    # We'll create the square at each angle and connect them
    for i in range(len(theta)):
        angle = theta[i]
        next_angle = theta[(i+1)%len(theta)]
        
        # Calculate the position along the torus path
        x0 = major_radius * np.cos(angle)
        y0 = major_radius * np.sin(angle)
        z0 = 0
        
        x1 = major_radius * np.cos(next_angle)
        y1 = major_radius * np.sin(next_angle)
        z1 = 0
        
        # The square will twist as we go around the torus
        twist_factor = angle/max(theta) * twists * 2*np.pi
        
        # Four corners of the square
        square_vertices = []
        for j in range(4):
            corner_angle = j * np.pi/2 + np.pi/4 + twist_factor
            dx = minor_radius * np.cos(corner_angle)
            dy = minor_radius * np.sin(corner_angle)
            
            # Position this square in 3D space
            square_vertices.append([
                x0 + dx * np.cos(angle),
                y0 + dx * np.sin(angle),
                z0 + dy
            ])
        
        # Connect the square vertices with cylinders
        for j in range(4):
            start = square_vertices[j]
            end = square_vertices[(j+1)%4]
            cylinder = trimesh.creation.cylinder(
                radius=wire_thickness,
                segment=np.array([start, end])
            )
            all_wires.append(cylinder)
        
        # Connect this square to the next one
        for j in range(4):
            next_twist_factor = next_angle/max(theta) * twists * 2*np.pi
            next_corner_angle = j * np.pi/2 + np.pi/4 + next_twist_factor
            dx = minor_radius * np.cos(next_corner_angle)
            dy = minor_radius * np.sin(next_corner_angle)
            
            next_vert = [
                x1 + dx * np.cos(next_angle),
                y1 + dx * np.sin(next_angle),
                z1 + dy
            ]
            
            cylinder = trimesh.creation.cylinder(
                radius=wire_thickness,
                segment=np.array([square_vertices[j], next_vert])
            )
            all_wires.append(cylinder)
    
    # Combine all cylinders into a single mesh
    wireframe = trimesh.util.concatenate(all_wires)
    return wireframe

# Create and export the twisted torus
twisted_torus = create_twisted_torus_wireframe(
    major_radius=3, 
    minor_radius=1, 
    twists=5, 
    resolution=100,
    wire_thickness=0.03
)
twisted_torus.export('stls/torus_wireframe.stl')

print("Successfully exported twisted torus wireframe as STL")