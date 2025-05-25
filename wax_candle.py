import bpy

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# -----------------
# Candle Mesh Setup
# -----------------

# Base cylinder for candle
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.5, depth=2, location=(0, 0, 1))
candle = bpy.context.active_object
candle.name = "Candle"

# Simple taper toward the top using Simple Deform
simple_def = candle.modifiers.new(name="Taper", type='SIMPLE_DEFORM')
simple_def.deform_method = 'TAPER'
simple_def.deform_axis = 'Z'
simple_def.factor = -0.2

# Subdivision surface for smoothness
subd = candle.modifiers.new(name="Subdivision", type='SUBSURF')
subd.levels = 3
subd.render_levels = 3

# Displace modifier for melted irregularities
cloud_tex = bpy.data.textures.new("CandleCloudTex", type='CLOUDS')
disp_mod = candle.modifiers.new(name="Displace", type='DISPLACE')
disp_mod.texture = cloud_tex
disp_mod.strength = 0.08

# Optional solidify for hollow candle
solid = candle.modifiers.new(name="Solidify", type='SOLIDIFY')
solid.thickness = 0.03

# Multires for manual sculpting (optional)
candle.modifiers.new(name="Multires", type='MULTIRES')

# -----------------
# Wick Setup
# -----------------

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.05, depth=0.25, location=(0, 0, 2.1))
wick = bpy.context.active_object
wick.name = "Wick"

wick_tex = bpy.data.textures.new("WickNoise", type='NOISE')
wick_disp = wick.modifiers.new(name="Displace", type='DISPLACE')
wick_disp.texture = wick_tex
wick_disp.strength = 0.02

# -----------------
# Material for Candle
# -----------------

wax_mat = bpy.data.materials.new(name="WaxMaterial")
wax_mat.use_nodes = True
nodes = wax_mat.node_tree.nodes
links = wax_mat.node_tree.links

# Remove default nodes
for n in nodes:
    nodes.remove(n)

out = nodes.new('ShaderNodeOutputMaterial')
principled = nodes.new('ShaderNodeBsdfPrincipled')
links.new(principled.outputs['BSDF'], out.inputs['Surface'])

# Mix in a small amount of glossy
glossy = nodes.new('ShaderNodeBsdfGlossy')
mix_shader = nodes.new('ShaderNodeMixShader')
mix_shader.inputs['Fac'].default_value = 0.05
links.new(principled.outputs['BSDF'], mix_shader.inputs[1])
links.new(glossy.outputs['BSDF'], mix_shader.inputs[2])
links.new(mix_shader.outputs['Shader'], out.inputs['Surface'])

# Noise texture for color variation
noise = nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 15
noise.inputs['Detail'].default_value = 2
noise.inputs['Distortion'].default_value = 0.1
color_mix = nodes.new('ShaderNodeMixRGB')
color_mix.inputs['Fac'].default_value = 0.5
color_mix.inputs['Color1'].default_value = (0.964, 0.878, 0.709, 1)  # Base
color_mix.inputs['Color2'].default_value = (0.918, 0.796, 0.619, 1)  # Accent
links.new(noise.outputs['Fac'], color_mix.inputs['Fac'])
links.new(color_mix.outputs['Color'], principled.inputs['Base Color'])

# Wax properties
principled.inputs['Subsurface'].default_value = 0.3
principled.inputs['Subsurface Radius'].default_value = (1.0, 0.25, 0.1)
principled.inputs['Subsurface Color'].default_value = (1.0, 0.89, 0.76, 1)
principled.inputs['Roughness'].default_value = 0.5
principled.inputs['Specular'].default_value = 0.3
principled.inputs['Transmission'].default_value = 0.1
principled.inputs['Sheen'].default_value = 0.1

# Bump and displacement
bump = nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = 0.05
links.new(noise.outputs['Fac'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], principled.inputs['Normal'])

musgrave = nodes.new('ShaderNodeTexMusgrave')
musgrave.inputs['Scale'].default_value = 10
musgrave.inputs['Detail'].default_value = 5
musgrave.inputs['Dimension'].default_value = 0.7
disp = nodes.new('ShaderNodeDisplacement')
links.new(musgrave.outputs['Height'], disp.inputs['Height'])
links.new(disp.outputs['Displacement'], out.inputs['Displacement'])

wax_mat.cycles.displacement_method = 'BOTH'

# Assign candle material
candle.data.materials.append(wax_mat)

# -----------------
# Material for Wick
# -----------------

wick_mat = bpy.data.materials.new(name="WickMaterial")
wick_mat.use_nodes = True
wick_nodes = wick_mat.node_tree.nodes
wick_principled = wick_nodes.get('Principled BSDF')
wick_principled.inputs['Base Color'].default_value = (0.05, 0.03, 0.02, 1)
wick_principled.inputs['Roughness'].default_value = 0.6
wick.data.materials.append(wick_mat)
