import bpy
import bmesh
from mathutils import Vector

# Nombres de los objetos
objA = bpy.data.objects["ObjetoA"]
objB = bpy.data.objects["ObjetoB"]

# Asegúrate de que ambos objetos tengan la misma topología
meshA = objA.data
meshB = objB.data

# Crear capa de color de vértice si no existe
if "Displacement" not in meshA.vertex_colors:
    meshA.vertex_colors.new(name="Displacement")
color_layer = meshA.vertex_colors["Displacement"]

# Obtener posiciones y normales
vertsA = [v.co for v in meshA.vertices]
normalsA = [v.normal for v in meshA.vertices]
vertsB = [v.co for v in meshB.vertices]

# Calcular desplazamientos proyectados
displacements = []
for i in range(len(vertsA)):
    d = vertsB[i] - vertsA[i]
    proj = d.dot(normalsA[i])
    proj_clamped = max(proj, 0.0)
    displacements.append(proj_clamped)

# Normalizar de 0 a 1
max_disp = max(displacements) if max(displacements) != 0 else 1.0
displacements = [d / max_disp for d in displacements]

# Asignar al color de vértice
# Nota: Cada loop (corner) de la malla toma el color del vértice correspondiente
for poly in meshA.polygons:
    for idx in poly.loop_indices:
        vert_idx = meshA.loops[idx].vertex_index
        val = displacements[vert_idx]
        color_layer.data[idx].color = (val, val, val, 1.0)

print("¡Colores de vértice actualizados con desplazamiento proyectado!")
