import cadquery as cq
import numpy as np

# PARAMETERS
rad = 80    #raggio fusoliera
h_ell = 80  #semiasse maggiore calotta
length = 750    #corpo centrale
thickness = 1   #parete fusoliera
fl_pos = -10    #(mm)
fl_thickness = 1    #(mm)
den_fuselage = 200  
den_floor = 1

# POINTS FOR ELLIPSE SPLINE
def half_ellipse_points(rx, ry, n=20):
    t = np.linspace(0, np.pi/2, n)   
    return [(rx * np.cos(a), ry * np.sin(a)) for a in t]

outer_pts = half_ellipse_points(rad, h_ell)
inner_pts = half_ellipse_points(rad - thickness, h_ell - thickness)

# DOME 
sketch = (
    cq.Workplane("XZ")
    .spline(outer_pts)
     .lineTo(0, 0)
     .lineTo(0, h_ell - thickness)
     .spline(list(reversed(inner_pts)))
     .close()
)

left_dome = sketch.revolve(360)

# CENTRAL BODY
outer_body = (
    cq.Workplane("XY")
    .circle(rad)
    .extrude(-length)
)

inner_body = (
    cq.Workplane("XY")
    .circle(rad - thickness)
    .extrude(-length)
)

body = outer_body.cut(inner_body)

# DOME MIRROR
right_dome = left_dome.mirror(mirrorPlane="XY").translate((0, 0, -length))

# FUSELAGE ASSEMBLY (WITHOUT FLOOR)
asm = body.union(left_dome).union(right_dome)


sketch_cut = (
    cq.Workplane("XZ")
    .spline(inner_pts)
     .lineTo(0, 0)
     .close()
     )

dome_cut = sketch_cut.revolve(360)
dome_mirr_cut = dome_cut.mirror(mirrorPlane="XY").translate((0, 0, -length))

asm_cut= dome_cut.union(dome_mirr_cut).union(inner_body)


#FLOOR
fl_length = length+h_ell+h_ell
fl_width = rad*2

floor = (cq.Workplane("XZ")
         .box(fl_width,fl_length,fl_thickness)
         .translate((0,fl_pos,-length/2))
         .intersect(asm_cut)
    )

#COMPLETE FUSELAGE ASSEMBLY
fuselage = asm.union(floor)

# EXPORT FILE
# Choose "floor" or "fuselage" or "asm"(fuselage w/o floor)
cq.exporters.export(asm, "fuselage_prova.step")

con= 1e-9
vol_fuselage = (asm.val().Volume())*con
vol_floor = (floor.val().Volume())*con


mass_fuselage = vol_fuselage * den_fuselage
mass_floor = vol_floor * den_floor

tot_mass = mass_fuselage

print(tot_mass)
