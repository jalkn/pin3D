#!/bin/bash

$GREEN = "Green"
$YELLOW = "Yellow"
$NC = "White"

function createScripts {
    Write-Host "🏗️ Creating Scripts" -ForegroundColor $YELLOW
    
    # Banks
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
}

function generateSTLS {
    Write-Host "🏗️ Generating STLS  " -ForegroundColor $GREEN

    # Python scripts to generate tables
    $scripts = @(
        "scripts/tetra.py"
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
    .\.venv\Scripts\Activate.ps1

    # Upgrade pip and install required packages
    python -m pip install --upgrade pip
    python -m pip install scipy pyvista trimesh numpy pybullet panda3d

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
        "scripts/tetra.py"
    )
    foreach ($file in $files) {
        New-Item -Path $file -ItemType File -Force
    }
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

    Write-Host "🏗️ The STLS are generated" -ForegroundColor $YELLOW
}

main