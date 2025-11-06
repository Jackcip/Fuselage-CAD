import cadquery as cq
import numpy as np

rad = 10
h_ell = 25
length = 40
angle = float(360.0)
thickness = 1

left_dome_sketch = (cq.Workplane("XZ")
           .ellipseArc(rad, h_ell, 0, 90,startAtCurrent = False)
           .lineTo(0,0)
           .close())
left_dome = left_dome_sketch.revolve(angle).faces("<Z").shell(-thickness, kind = "arc")
body = (cq.Workplane("XY")
      .circle(rad)
      .extrude(-length)
      .faces("|Z")
      .shell(-thickness)
      )

right_dome_sketch = (cq.Workplane("XZ")
           .move(0,-length)
           .lineTo(0,-h_ell-length)          
           .ellipseArc(rad, h_ell, 270,360,startAtCurrent = True)
           .close()
           )
right_dome = (right_dome_sketch
              .revolve(angle)
              .faces("|Z")
              .shell(-thickness)
              )

show_object([right_dome,body,left_dome])

combined = left_dome.union(body).union(right_dome)
cq.exporters.export(combined, 'Fuselage.step')