import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Shell (UV Sphere)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
shell = bpy.context.object
shell.scale.z = 0.6  # Flatten the shell

# Head (Sphere)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(1.2, 0, 0.3))
head = bpy.context.object

# Legs (Spheres)
leg_locs = [(0.5, 0.7, -0.5), (0.5, -0.7, -0.5), (-0.7, 0.5, -0.5), (-0.7, -0.5, -0.5)]
for loc in leg_locs:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=loc)

# Tail (Cone)
bpy.ops.mesh.primitive_cone_add(radius1=0.15, depth=0.5, location=(-1.2, 0, -0.3))
tail = bpy.context.object
tail.rotation_euler = (0, math.radians(30), 0)

# Color everything green
mat = bpy.data.materials.new(name="Turtle_Green")
mat.diffuse_color = (0.2, 0.8, 0.3, 1)
for obj in bpy.data.objects:
    obj.data.materials.append(mat)