import cadquery as cq
from cadquery import exporters

#in mm
width = 20
height = 40
length = 102

#sideThickness = 2
bottomThickness = 4

legThickness = 4
legDistance = 20
legHeight = 10

holder = cq.Workplane("front").box(width, length, height).faces("+Z").shell(bottomThickness, kind = 'intersection')
pts = [
    (0,0), 
    (0, legDistance), 
    (legHeight, 0),
    (0,0)
]
#.moveTo(0,0)
leg = cq.Workplane("front").polyline(pts).close().extrude(legThickness)
leg = leg.rotate((0,0,0), (1,0,0), 90)

legRightFront = leg.translate(((width/2)+bottomThickness, (length/2)+bottomThickness, (-height/2)-bottomThickness))
legLeftFront = leg.translate(((width/2)+bottomThickness, -1*((length/2)), (-height/2)-bottomThickness))

leg = leg.rotate((0,0,0), (0,0,1), 180)

legRightBack = leg.translate(( -1*((width/2)+bottomThickness), (length/2), (-height/2)-bottomThickness))
legLeftBack = leg.translate(( -1*((width/2)+bottomThickness), -1*((length/2)+bottomThickness), (-height/2)-bottomThickness))

result = holder.union(legRightFront).union(legLeftFront).union(legRightBack).union(legLeftBack)
show_object(result)
exporters.export(result, 'coasterHolder.stl')