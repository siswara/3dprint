import cadquery as cq
from cadquery import exporters

#in mm
strapWitdh = 15
witdh = 20
extension = 3
height = 10
length = 30
barRadius = 5

baseCut = cq.Workplane("XZ").circle(0.5*barRadius).extrude(witdh, both=True)
baseCut = baseCut.union(
    cq.Workplane("XZ").rect(height, height).extrude(strapWitdh, both=True)
)

base = cq.Workplane("XZ").moveTo(0.5*length+0.5*height+0.5*extension,0).rect(length+height+extension, height).extrude(witdh, both=True)
baseEnd = cq.Workplane("XZ").moveTo(0,0).circle(0.5*height).extrude(witdh, both=True)
base = base.union(baseEnd)
base = base.cut(baseCut)
del baseEnd
del baseCut

#experiment, cut top half
topCut = cq.Workplane("XZ").moveTo(0.5*length+0.5*extension+0.5*height, 1/2*height).rect(0.5*length, height).extrude(witdh, both=True)
base = base.cut(topCut)
bottomCut = cq.Workplane("XZ").moveTo(length+0.5*extension+0.5*height, -1/2*height).rect(0.5*length, height).extrude(witdh, both=True)
base = base.cut(bottomCut)
del topCut, bottomCut

midAdd = cq.Workplane("XZ").moveTo(0.5*length+0.5*extension+0.5*height, 0).rect(1/4*length, 0.5*height, False).extrude(witdh)
midCut = cq.Workplane("XZ").moveTo(0.5*length+0.5*extension+0.5*height, 0).rect(1/4*length, -0.5*height, False).extrude(-witdh)
base = base.cut(midCut)

base = base.union(midAdd)
del midAdd

lastCut = cq.Workplane("XZ").moveTo(length+0.5*extension+0.5*height, 0).rect(1/4*length, 0.5*height, False).extrude(witdh, both=True)
base = base.cut(lastCut)
del lastCut

base = base.edges().chamfer(1)
exporters.export(base, 'latch.stl')