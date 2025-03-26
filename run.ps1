#!/bin/bash

$GREEN = "Green"
$YELLOW = "Yellow"
$NC = "White"

function createScripts {
    Write-Host "🏗️ Creating Scripts" -ForegroundColor $YELLOW
    
    # tetrahedron
    Set-Content -Path "scripts/tetra.py" -Value @"
import numpy as np
import trimesh
import pyvista as pv

def create_tetrahedron():
    """Creates a tetrahedron mesh."""
    tetrahedron = trimesh.creation.box(extents=[1,1,1]) # Use box instead
    tetrahedron = tetrahedron.subdivide() #divide the box for simulating a tetrahedron
    tetrahedron.visual.face_colors = [255, 0, 0, 255]  # Red color
    return tetrahedron

# Generate and export the tetrahedron
tetrahedron_mesh = create_tetrahedron()
tetrahedron_mesh.export('stls/tetrahedron.stl')  # Save as STL
"@

    # hexahedron
    Set-Content -Path "scripts/hexa.py" -Value @"
import numpy as np
import trimesh
import pyvista as pv

# --- Hexahedron (Cube) ---
def create_hexahedron():
    """Creates a hexahedron (cube) mesh."""
    hexahedron = trimesh.creation.box(extents=[1, 1, 1])
    hexahedron.visual.face_colors = [0, 255, 0, 255]  # Green color
    return hexahedron

hexahedron_mesh = create_hexahedron()
hexahedron_mesh.export('stls/hexahedron.stl')
"@

    # octahedron
    Set-Content -Path "scripts/octa.py" -Value @"
import numpy as np
import trimesh
import pyvista as pv

# --- Octahedron ---
def create_octahedron():
    """Creates an octahedron mesh."""
    octahedron = trimesh.creation.octahedron()  # Direct octahedron creation
    octahedron.visual.face_colors = [0, 0, 255, 255]  # Blue color
    return octahedron

octahedron_mesh = create_octahedron()
octahedron_mesh.export('stls/octahedron.stl')
"@

    # octahedron
    Set-Content -Path "scripts/dodeca.py" -Value @"
import numpy as np
import trimesh
import pyvista as pv

# --- Dodecahedron ---
def create_dodecahedron():
    """Creates a dodecahedron mesh."""
    dodecahedron = trimesh.creation.dodecahedron() # Direct dodecahedron creation
    dodecahedron.visual.face_colors = [255, 255, 0, 255]  # Yellow color
    return dodecahedron


dodecahedron_mesh = create_dodecahedron()
dodecahedron_mesh.export('stls/dodecahedron.stl')
"@

    # icosahedron
    Set-Content -Path "scripts/icosa.py" -Value @"
import numpy as np
import trimesh
import pyvista as pv

# --- Icosahedron ---
def create_icosahedron():
    """Creates an icosahedron mesh."""
    icosahedron = trimesh.creation.icosahedron()  # Direct icosahedron creation
    icosahedron.visual.face_colors = [255, 0, 255, 255]  # Magenta color
    return icosahedron


icosahedron_mesh = create_icosahedron()
icosahedron_mesh.export('stls/icosahedron.stl')
"@

    # icosahedron
    Set-Content -Path "scripts/cylinder.py" -Value @"
import numpy as np
import trimesh
import pyvista as pv

# --- Cylinder ---
def create_cylinder():
    """Creates a cylinder mesh."""
    cylinder = trimesh.creation.cylinder(radius=1, height=2)
    cylinder.visual.face_colors = [0, 255, 255, 255]  # Cyan color
    return cylinder

cylinder_mesh = create_cylinder()
cylinder_mesh.export('stls/cylinder.stl')
"@
}

function generateSTLS {
    Write-Host "🏗️ Generating STLS  " -ForegroundColor $GREEN

    # Python scripts to generate tables
    $scripts = @(
        "scripts/tetra.py",
        "scripts/hexa.py",
        "scripts/octa.py",
        "scripts/dodeca.py",
        "scripts/icosa.py",
        "scripts/cylinder.py"
    )

    foreach ($script in $scripts) {
        #Execute the script
        python $script
    }
}

function createStructure {
    Write-Host "🏗️ Creating Structure" -ForegroundColor $YELLOW

    # Create Python virtual environment
    python -m venv .venv
    #.\.venv\Scripts\Activate.ps1

    # Upgrade pip and install required packages
    pip install --upgrade pip
    pip install scipy pyvista trimesh numpy pybullet panda3d

    # Always create subdirectories
    Write-Host "🏗️ Creating directory structure" -ForegroundColor $YELLOW
    $directories = @(
        "scripts",
        "stls"
    )
    foreach ($dir in $directories) {
        New-Item -Path $dir -ItemType Directory -Force
    }

    # Create empty Python files
    $files = @(
        "scripts/tetra.py",
        "scripts/hexa.py",
        "scripts/octa.py",
        "scripts/dodeca.py",
        "scripts/icosa.py",
        "scripts/cylinder.py"
    )
    foreach ($file in $files) {
        New-Item -Path $file -ItemType File -Force
    }
}

function createDMG {
    Write-Host "📦 Creating DMG" -ForegroundColor $GREEN

    # DMG filename
    $dmgName = "PinealGallery.dmg"

    # Temporary directory for DMG creation
    $tempDir = "temp_dmg"
    New-Item -Path $tempDir -ItemType Directory -Force

    # Copy the 'stls' directory into the temporary directory
    Copy-Item -Path "stls" -Destination "$tempDir/stls" -Recurse

    # Create the DMG file
    hdiutil create "$dmgName" -volname "PinealGallery" -srcfolder "$tempDir" -ov

    # Clean up the temporary directory
    Remove-Item -Path $tempDir -Recurse -Force

    Write-Host "✅ DMG created: $dmgName" -ForegroundColor $GREEN
}

function main {
    Write-Host "🏗️ Pineal Gallery" -ForegroundColor $NC

    # Call functions to create structure and generate scripts
    createStructure
    createScripts

    # Activate virtual environment
    #.\.venv\Scripts\Activate.ps1

    # Generate STLS
    generateSTLS

    # Create the DMG
    createDMG

    Write-Host "✅ Process completed." -ForegroundColor $NC
    Write-Host "🏗️ The STLS are generated" -ForegroundColor $YELLOW
}

main