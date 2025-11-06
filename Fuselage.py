import cadquery as cq
import numpy as np

rad = 10        
h_ell = 25      
length = 40     
thickness = 1   

def half_ellipse_points(rx, ry, top=True, n=20):
    if top:
        t = np.linspace(0, np.pi/2, n)  
    else:
        t = np.linspace(-np.pi/2, 0, n) 
    return [(rx * np.cos(a), ry * np.sin(a)) for a in t]




outer_pts = half_ellipse_points(rad, h_ell, top=True)

inner_pts = half_ellipse_points(rad - thickness, h_ell - thickness, top=True)

sketch = (
    cq.Workplane("XZ")
    .spline(outer_pts)
     .lineTo(0, 0)
     .moveTo(0, 0)
     .lineTo(0, h_ell - thickness)
     .spline(list(reversed(inner_pts)))
     .close()
)
left_dome = sketch.revolve(360)


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

right_dome = left_dome.mirror(mirrorPlane="XY").translate((0, 0, -length))


fuselage = body.union(left_dome).union(right_dome)

cq.exporters.export(fuselage, "Fuselage.step", cq.exporters.ExportTypes.STEP)