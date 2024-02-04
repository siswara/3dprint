import cadquery as cq
from cadquery import exporters

shoulderPegRadius = 6.8/2
shoulderPegDepth = (33.67-26.67)/2
upperArmLength = 10
lowerArmLength = 15


pegCut = cq.Workplane("XZ").circle(shoulderPegRadius).extrude(shoulderPegDepth)
shoulder = cq.Workplane("XZ").circle(1.5*shoulderPegRadius).extrude(2*shoulderPegDepth).chamfer(2)
upperArm = (
    #upperArm
    cq.Workplane("XY").center(0, -2.4*shoulderPegDepth/2).rect(2*shoulderPegRadius, 1.8*shoulderPegRadius)
    .workplane(-upperArmLength).rect(2*shoulderPegRadius, 1.8*shoulderPegRadius).loft()
    .faces("|Y").chamfer(2)
)


elbow = (
    upperArm.faces(">Y").workplane().move(0, 1).circle(4.5).extrude(-2.65*shoulderPegDepth).faces(">Y").chamfer(1)
    .faces("<Y").chamfer(2)
)

lowerArm = (
    cq.Workplane("XY").center(0, -2*shoulderPegDepth/2).rect(2*shoulderPegRadius, 2*shoulderPegRadius)
        .workplane(-lowerArmLength).rect(2*shoulderPegRadius, 2*shoulderPegRadius).loft()
        .faces("|Y").chamfer(2)
        .faces("|Z").hole(3)
)

lowerArm = lowerArm.rotate((0,0,0),(0,1,0),-60).translate(cq.Vector(0, -shoulderPegDepth, -7.6)).translate((-2,0,-1))
arm = upperArm.union(lowerArm)
arm = arm.union(shoulder).union(elbow).cut(pegCut)

del pegCut, upperArm, shoulder, elbow

armMirror = arm.mirror(mirrorPlane="XZ", basePointVector=(0,0,0))

exporters.export(arm, 'knightArm.stl')
exporters.export(armMirror, 'knightArmMirror.stl')