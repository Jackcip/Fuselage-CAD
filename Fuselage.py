import cadquery as cq
import numpy as np

# PARAMETERS
rad = 10
h_ell = 25
length = 40
thickness = 1

# POINTS FOR ELLIPSE SPLINE
def half_ellipse_points(rx, ry, n=20):
    t = np.linspace(0, np.pi/2, n)   
    return [(rx * np.cos(a), ry * np.sin(a)) for a in t]

outer_pts = half_ellipse_points(rad, h_ell, top=True)
inner_pts = half_ellipse_points(rad - thickness, h_ell - thickness, top=True)

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

# FUSELAGE ASSEMBLY
fuselage = body.union(left_dome).union(right_dome)

# EXPORT FILE
cq.exporters.export(fuselage, "Fuselage.step", cq.exporters.ExportTypes.STEP)