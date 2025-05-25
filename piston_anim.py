"""
Blender Python script to generate a mechanical piston assembly with animation.
This version adds a very simple representation of Freddy Fazbear who grips the
piston and moves with it so the piston appears to be pushed up and down.
Run inside Blender's scripting workspace.
"""
import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Base bracket
# Base bracket for piston mounted to the floor
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, -0.5, 0.6))
base = bpy.context.active_object
base.name = "BaseBracket"

# Mounting bolts on base
for x in (-0.1, 0.1):
    for y in (-0.1, 0.1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.05,
                                            location=(x, -0.5 + y, 0.425))
        bpy.context.active_object.parent = base

# Outer cylinder
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.4,
                                    location=(0, -0.5, 0.85))
outer = bpy.context.active_object
outer.name = "OuterCylinder"
outer.parent = base

# Inner piston shaft
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.4,
                                    location=(0, -0.5, 1.05))
inner = bpy.context.active_object
inner.name = "InnerShaft"
inner.parent = base

# Ball joint at end of piston
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(0, -0.5, 1.25))
ball = bpy.context.active_object
ball.name = "BallJoint"
ball.parent = inner

# Mechanical arm segment
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0, -0.5, 1.45))
arm = bpy.context.active_object
arm.scale = (0.5, 0.1, 1)
arm.name = "MechArm"
arm.parent = ball

# Accordion dust boot
bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.01,
                                 location=(0, -0.5, 0.95))
boot = bpy.context.active_object
boot.rotation_euler.x = math.radians(90)
boot.parent = outer
boot_mod = boot.modifiers.new(name="Array", type='ARRAY')
boot_mod.count = 8
boot_mod.relative_offset_displace = (0, 0, 0.12)

# Material with rusted steel look
rust = bpy.data.materials.new(name="RustyMetal")
rust.use_nodes = True
nodes = rust.node_tree.nodes
links = rust.node_tree.links
nodes.clear()
output = nodes.new('ShaderNodeOutputMaterial')
principled = nodes.new('ShaderNodeBsdfPrincipled')
noise = nodes.new('ShaderNodeTexNoise')
color = nodes.new('ShaderNodeValToRGB')
color.color_ramp.elements[0].color = (0.4, 0.2, 0.1, 1)
color.color_ramp.elements[1].color = (0.1, 0.05, 0.02, 1)
links.new(noise.outputs['Fac'], color.inputs['Fac'])
links.new(color.outputs['Color'], principled.inputs['Base Color'])
principled.inputs['Metallic'].default_value = 1.0
principled.inputs['Roughness'].default_value = 0.7
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

for obj in (outer, inner, base, boot, ball, arm):
    obj.data.materials.append(rust)

# -----------------------------------------------------
# Simple Freddy Fazbear built from primitives
# -----------------------------------------------------
# Torso
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, -0.5, 0.8))
torso = bpy.context.active_object
torso.name = "FreddyTorso"
torso.data.materials.append(rust)

# Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, -0.5, 1.5))
head = bpy.context.active_object
head.name = "FreddyHead"
head.parent = torso
head.data.materials.append(rust)

# Right upper arm
bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.4,
                                    location=(0.25, -0.5, 1.2))
upper_arm = bpy.context.active_object
upper_arm.rotation_euler.x = math.radians(90)
upper_arm.name = "FreddyUpperArm"
upper_arm.parent = torso
upper_arm.data.materials.append(rust)

# Right forearm
bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.35,
                                    location=(0, 0, 0))
forearm = bpy.context.active_object
forearm.rotation_euler.x = math.radians(90)
forearm.name = "FreddyForearm"
forearm.parent = ball  # attach to piston end
forearm.data.materials.append(rust)

# Keep forearm aligned to ball location
forearm.location = ball.location

# Animate piston extension/contraction
scene = bpy.context.scene
inner.keyframe_insert(data_path="location", frame=1)
inner.location.z += 0.2
inner.keyframe_insert(data_path="location", frame=20)
inner.location.z -= 0.05
inner.keyframe_insert(data_path="location", frame=25)
inner.location.z += 0.1
inner.keyframe_insert(data_path="location", frame=35)

# Add noise modifiers for jitter
for fc in inner.animation_data.action.fcurves:
    mod = fc.modifiers.new(type='NOISE')
    mod.scale = 5
    mod.strength = 0.01

# Lighting - warm backstage bulb
bpy.ops.object.light_add(type='POINT', location=(2, 2, 2))
light = bpy.context.active_object
light.data.energy = 1000
light.data.color = (1.0, 0.9, 0.7)
light.data.keyframe_insert(data_path='energy', frame=1)
light.data.energy = 600
light.data.keyframe_insert(data_path='energy', frame=10)
light.data.energy = 1000
light.data.keyframe_insert(data_path='energy', frame=20)

# Camera
bpy.ops.object.camera_add(location=(2, -2, 1),
                          rotation=(math.radians(75), 0, math.radians(45)))
scene.camera = bpy.context.active_object

# Render settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.frame_end = 35

# Optional: load servo sound (supply your own path)
# bpy.ops.sound.open(filepath='servo_noise.wav')
# scene.sequence_editor_create()
# scene.sequence_editor.sequences.new_sound('servo', filepath='servo_noise.wav',
#                                            channel=1, frame_start=1)

print("Freddy piston animation setup complete.")
