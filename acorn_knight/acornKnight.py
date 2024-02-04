import cadquery as cq
from cadquery import exporters

SHOULDER_NUB_DEPTH = 3
(TAG_DISC_RADIUS, TAG_DISC_THICKNESS) = (3,2)

acornRadius = 20.52/2
acornHeight = 28.15
acornSinkHeight = 7.58
armLength = 10
legLength = 10
baseThickness = 3

def makeTorso(torsoHeight, neckOpeningRadius, cuffHeight):

    neckCuffCut = cq.Workplane("YZ").moveTo(0, cuffHeight).circle(cuffHeight).extrude(1.4*neckOpeningRadius)
    neckCuff = cq.Workplane("XY").circle(1.2*neckOpeningRadius).circle(neckOpeningRadius).extrude(cuffHeight).faces(">Z").chamfer(1).cut(neckCuffCut)
    body = cq.Workplane("XY").circle(1.3*neckOpeningRadius).extrude(-torsoHeight).chamfer(1)

    #tagDisc = cq.Workplane("XZ").circle(TAG_DISC_RADIUS).extrude(TAG_DISC_THICKNESS)
    #tagDiscLeft = tagDisc.translate((0, 1.3*neckOpeningRadius+TAG_DISC_THICKNESS, -0.25*torsoHeight))
    #tagDiscRight = tagDisc.translate((0, -1.3*neckOpeningRadius, -0.25*torsoHeight))
    shoulderDisc = (
            cq.Workplane("XZ").circle(TAG_DISC_RADIUS)
                .extrude(1.3*neckOpeningRadius+SHOULDER_NUB_DEPTH, both=True).translate((0, 0, -0.25*torsoHeight))
                .chamfer(1)
        )
    #tagDiscBottom = tagDisc.rotate((0,0,0), (1,0,0), 90)
    tagDiscBottom = cq.Workplane("XY").box(TAG_DISC_RADIUS, TAG_DISC_RADIUS, TAG_DISC_THICKNESS)
    tagDiscBottomLeft = tagDiscBottom.translate((+3, 0.7*neckOpeningRadius, -torsoHeight))
    tagDiscBottomRight = tagDiscBottom.translate((-2, -0.7*neckOpeningRadius, -torsoHeight))
    body.faces(">Z").circle(TAG_DISC_RADIUS).extrude(-10, both=True)
    rv = (
        body.union(neckCuff)
            #.union(tagDiscLeft).union(tagDiscRight)
            .union(shoulderDisc)
            .union(tagDiscBottomLeft).union(tagDiscBottomRight)
    )

    #tag connector
    rv.faces("<Y").tag("rightShoulder")
    rv.faces(">Y").tag("leftShoulder")
    rv.faces("<Z").faces(">Y").tag("leftHip")
    rv.faces("<Z").faces("<Y").tag("rightHip")
    return rv

#TODO
# def makeArm(armLength):
#     return rv

def makeLeg(legLength):
    upperThigh = cq.Workplane("XY").workplane(offset=-2.5).box(9,5,legLength/2).edges('|Z').chamfer(1).edges('|Y and <Z').chamfer(1)
    lowerShin = cq.Workplane("XY").box(7,5,legLength/2).edges('|Z').chamfer(1)
    lowerShin = lowerShin.translate((-1,0,-4))
    cutForAssembly = cq.Workplane("XY").circle(1).extrude(-TAG_DISC_THICKNESS)
    #upperThigh = cq.Workplane("XY").circle(3).workplane(-legLength).moveTo(0,0).circle(1).loft().cut(cutForAssembly)
    upperThigh = upperThigh.cut(cutForAssembly)
    rv = (
        upperThigh.union(lowerShin)
    )
    return rv

def basePlate(acornRadius, baseThickness):
    rv = (
        cq.Workplane("XY").circle(acornRadius)
            .workplane(offset=-baseThickness)
            .circle(acornRadius+SHOULDER_NUB_DEPTH)
            .loft()
    )
    return rv

#TODO
# def makePole():
#     return rv

#TODO
# def makeMace():
#     return rv

knight = (
    cq.Assembly()
    .add(makeTorso(acornHeight, acornRadius, acornSinkHeight), name="torso", color=cq.Color("red"))
    .add(makeLeg(legLength), name="rightLeg", color=cq.Color("blue1"))
    .add(makeLeg(legLength), name="leftLeg", color=cq.Color("purple"))
    #.add(basePlate(1.5*acornRadius, baseThickness), name="basePlate", color=cq.Color("yellow"))
    # .add(makePole(), name="pole")
    # .add(makeMace(), name="mace")
)

# i want to minimize distance between 
#   plane rightLeg >Z vs knight rightHip
#   plane leftLeg >Z vs knight leftHip
(
    knight
    .constrain("torso?rightHip", "rightLeg@faces@<Z[1]", "Plane") 
    .constrain("torso?leftHip", "leftLeg@faces@<Z[1]", "Plane")
    #.constrain("torso?rightHip", "rightLeg@faces@>Z[1]", "Axis") 
    #.constrain("torso?leftHip", "leftLeg@faces@>Z[1]", "Axis")
    
    #.constrain("leftLeg@faces@<Y","rightLeg@faces@>Y", "Plane", param=100)
    .constrain("rightLeg@faces@>X","FixedAxis",(4,-1,0))
    .constrain("leftLeg@faces@>X","FixedAxis",(4,1,0))
    #.constrain("basePlate@faces@>Z", "rightLeg@faces@<Z", "Plane")
    #.constrain("basePlate@faces@>Z", "leftLeg@faces@<Z", "Plane")
)

knight.solve()

knightCompound = knight.toCompound()

#workaround
base = basePlate(1.5*acornRadius, baseThickness)
base = base.translate((0, 0, -acornHeight-6))
knightCompound = knightCompound.fuse(base.val())

show_object([knightCompound])
# exporters.export(knightCompound, 'knight.stl')

# question : how can I center the base plate based on both plane?
# #2nd assembly
# assy = (
#     cq.Assembly()
#         .add(knight.toCompound(), name="knight2")
#         .add(basePlate(1.5*acornRadius, baseThickness), name="basePlate", color=cq.Color("yellow"))
# )

# (
#     assy
#         #.constrain("knight2", "basePlate", "Point")
#         .constrain("knight2@faces@>Z", "basePlate@faces@<Z", "Axis")
#         .constrain("knight2@faces@<<Z", "basePlate@faces@>Z", "Plane")
#         #.constrain("basePlate@faces@>Z", "knight2@faces@<Z", "Point")
# )

# assy.solve()
# show_object(assy, name="knight")
# #knight.toCompound()#.save('knight.stl')