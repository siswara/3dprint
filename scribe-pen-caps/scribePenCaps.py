import cadquery as cq
from cadquery import exporters

# in mm
penDiameter = 8.8
penRadius = penDiameter/2
penFlat = 5 #maybe not use this
penFlattenDiameter = 8.1

penSmallerDiameter = 6
penSmallerRadius = penSmallerDiameter/2
penTopHeight = 12
baseHeight = 25

capThickness = 1
tighteningDepth = 0.2
tighteningHeight = 5

capBase = cq.Workplane("front")
capBase = capBase.circle(penRadius + capThickness) #outer circle
capBase = capBase.circle(penRadius)
capBase = capBase.extrude(baseHeight)

capTop = cq.Workplane("front")
capTop = capTop.circle(penRadius + capThickness) #outer circle
capTop = capTop.circle(penSmallerRadius)
capTop = capTop.extrude(penTopHeight)
capTop = capTop.translate((0, 0, baseHeight))

capCover = cq.Workplane("front")\
    .circle(penRadius + capThickness)\
    .extrude(capThickness)\
    .translate((0, 0, baseHeight + penTopHeight))

tighter = cq.Workplane("front")\
    .moveTo(penRadius, 0)\
    .rect(tighteningDepth, 2*tighteningDepth)\
    .extrude(tighteningHeight)\
    .translate((0, 0, tighteningHeight))

tighter = tighter\
    .moveTo(-penRadius, 0)\
    .rect(tighteningDepth, 2*tighteningDepth)\
    .extrude(tighteningHeight)\
    .translate((0, 0, tighteningHeight))

tighter = tighter\
    .moveTo(0, -penRadius)\
    .rect(2*tighteningDepth, tighteningDepth)\
    .extrude(tighteningHeight)\
    .translate((0, 0, tighteningHeight))

cap = capBase.union(capTop).union(capCover).union(tighter)

pts = [
    (0,0), 
    (penDiameter, 0),
    (penDiameter, 2*penDiameter),
    (-penDiameter, 2*penDiameter),
    (-penDiameter, 0),
    (0,0)
]

cap = cap\
    .center(0, (penDiameter/2)- (penDiameter - penFlattenDiameter))\
    .polyline(pts).close()\
    .cutThruAll()

show_object(cap)
exporters.export(cap, 'scribePenCaps.stl')




