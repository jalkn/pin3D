#!/bin/bash

$GREEN = "Green"
$YELLOW = "Yellow"
$NC = "White"

function createScripts {
    Write-Host "🏗️ Creating 3D Scripts" -ForegroundColor $YELLOW
    Set-Content -Path "3 D/cube.py" -Value @"
import numpy as np
import trimesh

def create_cube_tetrahedron_combo():
    # Cube vertices (edge length 2 centered at origin)
    cube_vertices = np.array([
        [ 1,  1,  1], [-1,  1,  1], [-1, -1,  1], [ 1, -1,  1],
        [ 1,  1, -1], [-1,  1, -1], [-1, -1, -1], [ 1, -1, -1]
    ])
    
    # Cube edges (12 edges)
    cube_edges = [
        [0,1], [1,2], [2,3], [3,0],  # Top face
        [4,5], [5,6], [6,7], [7,4],  # Bottom face
        [0,4], [1,5], [2,6], [3,7]   # Vertical edges
    ]
    
    # Tetrahedron vertices
    tet_vertices = np.array([
        [ 1,  1,  1],
        [-1, -1,  1],
        [-1,  1, -1],
        [ 1, -1, -1]
    ])
    
    # Tetrahedron edges (6 edges)
    tet_edges = [
        [0,1], [0,2], [0,3],
        [1,2], [1,3], [2,3]
    ]
    
    return cube_vertices, cube_edges, tet_vertices, tet_edges

# Create geometry
cube_v, cube_e, tet_v, tet_e = create_cube_tetrahedron_combo()

# Create thin cylinders for all edges
radius = 0.02  # Adjust thickness as needed
edge_meshes = []

# Add cube edges
for edge in cube_e:
    line = cube_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius, segment=line)
    edge_meshes.append(cylinder)

# Add tetrahedron edges (in a different color if desired)
for edge in tet_e:
    line = tet_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius*1.2, segment=line)  # Slightly thicker
    edge_meshes.append(cylinder)

# Combine all cylinders into a single mesh
wireframe = trimesh.util.concatenate(edge_meshes)

# Export as STL
wireframe.export('S T L/combo.stl')

print("Successfully exported cube-tetrahedron combination as STL")
"@

    Set-Content -Path "3 D/cylinder.py" -Value @"
import numpy as np
import trimesh

# --- Cylinder ---
def create_cylinder():
    """Creates a cylinder mesh."""
    cylinder = trimesh.creation.cylinder(radius=1, height=2)
    cylinder.visual.face_colors = [0, 255, 255, 255]  # Cyan color
    return cylinder

cylinder_mesh = create_cylinder()
cylinder_mesh.export('S T L/cylinder.stl')

"@

    Set-Content -Path "3 D/dode.py" -Value @"
import numpy as np
import trimesh

# --- Cylinder ---
def create_cylinder():
    """Creates a cylinder mesh."""
    cylinder = trimesh.creation.cylinder(radius=1, height=2)
    cylinder.visual.face_colors = [0, 255, 255, 255]  # Cyan color
    return cylinder

cylinder_mesh = create_cylinder()
cylinder_mesh.export('S T L/cylinder.stl')

"@

    Set-Content -Path "3 D/dodeca.py" -Value @"
import numpy as np
import trimesh

def create_dodecahedron_icosahedron_combo():
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Icosahedron vertices (12 vertices)
    icosahedron_vertices = np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])
    
    # Icosahedron edges (30 edges - we'll use convex hull to find them)
    icosahedron = trimesh.convex.convex_hull(icosahedron_vertices)
    icosahedron_edges = np.vstack([icosahedron.edges_unique])
    
    # Dodecahedron vertices (20 vertices)
    dodecahedron_vertices = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, 1/phi, phi], [0, -1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, -phi],
        [1/phi, phi, 0], [-1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, -phi, 0],
        [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi]
    ])
    
    # Scale down the dodecahedron to fit inside
    dodecahedron_vertices *= 0.8
    
    # Dodecahedron edges (30 edges - again using convex hull)
    dodecahedron = trimesh.convex.convex_hull(dodecahedron_vertices)
    dodecahedron_edges = np.vstack([dodecahedron.edges_unique])
    
    return icosahedron_vertices, icosahedron_edges, dodecahedron_vertices, dodecahedron_edges

# Create geometry
ico_v, ico_e, dod_v, dod_e = create_dodecahedron_icosahedron_combo()

# Create thin cylinders for all edges
radius = 0.02
edge_meshes = []

# Add icosahedron edges (outer shape)
for edge in ico_e:
    line = ico_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius, segment=line)
    edge_meshes.append(cylinder)

# Add dodecahedron edges (inner shape, slightly thicker and different color)
for edge in dod_e:
    line = dod_v[edge]
    cylinder = trimesh.creation.cylinder(radius=radius*1.5, segment=line)
    edge_meshes.append(cylinder)

# Combine all cylinders
wireframe = trimesh.util.concatenate(edge_meshes)

# Export as STL
wireframe.export('S T L/dodeca.stl')

print("Successfully exported dodecahedron-icosahedron combination as STL")
"@

    Set-Content -Path "3 D/hexa.py" -Value @"
import numpy as np
import trimesh

# --- Hexahedron (Cuboid) ---
def create_hexahedron(width=3, length=3, height=3):
    """Creates a hexahedron (cuboid) mesh."""
    hexahedron = trimesh.creation.box(extents=[width, length, height])  # extents = [x, y, z] dimensions
    hexahedron.visual.face_colors = [255, 0, 0, 255]  # Red color
    return hexahedron

hexahedron_mesh = create_hexahedron()
hexahedron_mesh.export('S T L/hexahedron.stl')
"@

    Set-Content -Path "3 D/ico.py" -Value @"
import numpy as np
import trimesh

def create_icosahedron():
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Icosahedron vertices (scaled up by 2x)
    vertices = 2 * np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])
    
    # Normalize to unit sphere (optional, comment out if you want exact scaling)
    vertices /= np.linalg.norm(vertices, axis=1)[:, np.newaxis]
    
    # Generate edges using convex hull
    mesh = trimesh.convex.convex_hull(vertices)
    edges = mesh.edges_unique
    
    return vertices, edges

# Create icosahedron
ico_v, ico_e = create_icosahedron()

# Create wireframe (thin silver edges)
radius = 0.015  # Reduced from 0.03 to make edges thinner
edge_meshes = []

for edge in ico_e:
    cylinder = trimesh.creation.cylinder(
        radius=radius,
        segment=ico_v[edge],
        vertex_colors=[200, 200, 200, 255]  # Silver
    )
    edge_meshes.append(cylinder)

wireframe = trimesh.util.concatenate(edge_meshes)
wireframe.export('S T L/icosahedron.stl')

print("Large thin icosahedron exported successfully!")

def make_print_ready(vertices, edges, radius=0.4):  # Minimum radius for FDM printing
    # Create thickened edges with spherical joints
    meshes = []
    for edge in edges:
        line = vertices[edge]
        # Cylinder for edge
        cyl = trimesh.creation.cylinder(radius=radius, segment=line)
        # Spheres at vertices for stronger joints
        for vertex in line:
            sphere = trimesh.creation.icosphere(radius=radius*1.2, subdivisions=2)
            sphere.apply_translation(vertex)
            meshes.append(sphere)
        meshes.append(cyl)
    
    # Merge and fix potential issues
    merged = trimesh.util.concatenate(meshes)
    merged.fill_holes()  # Close any gaps
    merged = merged.process(validate=True)  # Repair mesh
    
    return merged

# Usage (replace the wireframe export code in both scripts):
ico_mesh = make_print_ready(ico_v, ico_e, radius=0.4)
ico_mesh.export('S T L/icosahedron_printable.stl')
"@

    Set-Content -Path "3 D/octa.py" -Value @"
import numpy as np
import trimesh

def create_octahedron():
    vertices = np.array([
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1]
    ])
    faces = np.array([
        [0, 2, 4],
        [0, 4, 3],
        [0, 3, 5],
        [0, 5, 2],
        [1, 2, 5],
        [1, 5, 3],
        [1, 3, 4],
        [1, 4, 2]
    ])
    octahedron = trimesh.Trimesh(vertices=vertices, faces=faces)
    octahedron.visual.face_colors = [0, 0, 255, 255]  # Blue color
    return octahedron

octahedron_mesh = create_octahedron()
octahedron_mesh.export('S T L/octahedron.stl')
"@
    Set-Content -Path "3 D/octadge.py" -Value @"
import numpy as np
import trimesh

def create_octahedron():
    vertices = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ])
    faces = np.array([
        [0, 2, 4], [0, 4, 3],
        [0, 3, 5], [0, 5, 2],
        [1, 2, 5], [1, 5, 3],
        [1, 3, 4], [1, 4, 2]
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

# Create octahedron
octahedron = create_octahedron()

# Create thin cylinders for each edge
radius = 0.02  # Adjust thickness as needed
edge_meshes = []

for edge in octahedron.edges_unique:
    # Get the two vertices of the edge
    line = octahedron.vertices[edge]
    # Create a cylinder along this edge
    cylinder = trimesh.creation.cylinder(radius=radius, segment=line)
    edge_meshes.append(cylinder)

# Combine all cylinders into a single mesh
wireframe = trimesh.util.concatenate(edge_meshes)

# Export as STL
wireframe.export('S T L/octahedron_edges.stl')

print("Successfully exported octahedron edges as STL")
"@
    Set-Content -Path "3 D/octedge.py" -Value @"
import numpy as np
import trimesh

def create_octahedron():
    vertices = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ])
    faces = np.array([
        [0, 2, 4], [0, 4, 3],
        [0, 3, 5], [0, 5, 2],
        [1, 2, 5], [1, 5, 3],
        [1, 3, 4], [1, 4, 2]
    ])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

# Create octahedron and get edges
octahedron = create_octahedron()
edges = np.sort(octahedron.edges_unique, axis=1)
lines = octahedron.vertices[edges]

# Create and export wireframe
edge_path = trimesh.load_path(lines)
edge_path.export('S T L/octahedron_edges.ply')
"@
    Set-Content -Path "3 D/prism.py" -Value @"
import numpy as np
import trimesh

def create_triangular_prism():
    vertices = np.array([
        [0, 0, 0],  # Base triangle
        [1, 0, 0],
        [0.5, np.sqrt(3)/2, 0],
        [0, 0, 1],  # Top triangle
        [1, 0, 1],
        [0.5, np.sqrt(3)/2, 1]
    ])
    faces = np.array([
        [0, 1, 2],  # Bottom face
        [3, 5, 4],  # Top face
        [0, 3, 1],  # Side faces
        [1, 3, 4],
        [1, 4, 2],
        [2, 4, 5],
        [2, 5, 0],
        [0, 5, 3]
    ])
    prism = trimesh.Trimesh(vertices=vertices, faces=faces)
    prism.visual.face_colors = [255, 0, 255, 255]  # Purple color
    return prism

prism_mesh = create_triangular_prism()
prism_mesh.export('S T L/prism.stl')
"@
    Set-Content -Path "3 D/sphere.py" -Value @"
import numpy as np
import trimesh

# --- Sphere ---
def create_sphere():
    """Creates a sphere mesh."""
    sphere = trimesh.creation.icosphere(radius=1.5)  # Use icosphere for a better mesh than uv_sphere
    sphere.visual.face_colors = [255, 0, 255, 255]  # Magenta color
    return sphere

sphere_mesh = create_sphere()

sphere_mesh.export('S T L/sphere.stl')
"@
    Set-Content -Path "3 D/tetra.py" -Value @"
import numpy as np
import trimesh

def create_tetrahedron():
    vertices = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 1],
        [1, 3, 2]
    ])
    tetrahedron = trimesh.Trimesh(vertices=vertices, faces=faces)
    tetrahedron.visual.face_colors = [0, 255, 0, 255]  # Green color
    return tetrahedron

tetrahedron_mesh = create_tetrahedron()
tetrahedron_mesh.export('S T L/tetrahedron.stl')
"@
    Set-Content -Path "3 D/torus.py" -Value @"
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
twisted_torus.export('S T L/torus_wireframe.stl')

print("Successfully exported twisted torus wireframe as STL")
"@
    Set-Content -Path "3 D/twisTorus.py" -Value @"
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
twisted_torus.export('S T L/twisted_torus_wireframe.stl')

print("Successfully exported twisted torus wireframe as STL!")
"@
}

function generateSTL {
    Write-Host "🏗️ Generating STLS  " -ForegroundColor $GREEN

    # python3 scripts to generate tables
    $scripts = @(
        "3 D/cube.py",
        "3 D/cylinder.py",
        "3 D/dode.py",
        "3 D/dodeca.py",
        "3 D/ico.py",
        "3 D/octa.py",
        "3 D/ico.py",
        "3 D/octa.py",
        "3 D/octadge.py",
        "3 D/octedge.py",
        "3 D/prism.py",
        "3 D/sphere.py",
        "3 D/tetra.py",
        "3 D/torus.py",
        "3 D/twisTorus.py"
    )

    foreach ($script in $scripts) {
        #Execute the script
        python3 $script
    }
}

function createStructure {
    Write-Host "🏗️ Creating Structure" -ForegroundColor $YELLOW

    # Create python3 virtual environment
    python3 -m venv .venv
    #.\.venv\Scripts\Activate.ps1

    # Upgrade pip and install required packages
    pip install --upgrade pip
    pip install scipy pyvista trimesh numpy pybullet panda3d

    # Always create subdirectories
    Write-Host "🏗️ Creating directory structure" -ForegroundColor $YELLOW
    $directories = @(
        "3 D",
        "S T L"
    )
    foreach ($dir in $directories) {
        New-Item -Path $dir -ItemType Directory -Force
    }
}

function main {
    Write-Host "🏗️ P I N 3 D" -ForegroundColor $NC

    # Call functions to create structure and generate scripts
    createStructure
    createScripts

    # Activate virtual environment
    #.\.venv\Scripts\Activate.ps1

    # Generate STLS
    generateSTL

    Write-Host "✅ Process completed." -ForegroundColor $NC
    Write-Host "🏗️ The STLS are generated" -ForegroundColor $YELLOW
}

main