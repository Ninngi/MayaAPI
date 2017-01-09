# ===================
# patrvq@interia.pl
# Learning resources
# Maya Python API Course
# ===================

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx



nodeName = "WheelNode"
nodeId = OpenMaya.MTypeId(0x100fff) # Temporary =)


class WheelNode(OpenMayaMPx.MPxNode):
    inRadius = OpenMaya.MObject()
    inTranslate = OpenMaya.MObject()
    outRotate = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        '''
        rotate = translate/ (2 * 3.14 * radius ) * (-360)
        '''
        if plug == WheelNode.outRotate:

            dataHandleRadius = dataBlock.inputValue(WheelNode.inRadius)
            dataHandleTranslate = dataBlock.inputValue(WheelNode.inTranslate)

            inRadiusVal = dataHandleRadius.asFloat()
            inTranslateVal = dataHandleTranslate.asFloat()

            outRotate = float(inTranslateVal) / float(2 * 3.14 * inRadiusVal) * (-360)

            dataHandleRotate = dataBlock.outputValue(WheelNode.outRotate)

            dataHandleRotate.setFloat(outRotate)
            dataBlock.setClean(plug)

        else:
            return None




def nodeCreator():
    return OpenMayaMPx.asMPxPtr(WheelNode())


def nodeInitializer():
    # 1. creating a function set for numeric attributes
    mFnAttr = OpenMaya.MFnNumericAttribute()

    # 2. create the attributes
    WheelNode.inRadius = mFnAttr.create("radius", "r", OpenMaya.MFnNumericData.kFloat, 0.0)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    WheelNode.inTranslate = mFnAttr.create("translate", "t", OpenMaya.MFnNumericData.kFloat, 0.0)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)

    WheelNode.outRotate = mFnAttr.create("rotate", "rot", OpenMaya.MFnNumericData.kFloat)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)

    # 3. Attaching the attributes to the Node

    WheelNode.addAttribute(WheelNode.inRadius)
    WheelNode.addAttribute(WheelNode.inTranslate)
    WheelNode.addAttribute(WheelNode.outRotate)

    # 4. Design circuitry
    WheelNode.attributeAffects(WheelNode.inRadius, WheelNode.outRotate)
    WheelNode.attributeAffects(WheelNode.inTranslate, WheelNode.outRotate)


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register command: %s\n" % nodeName)


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(nodeName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % nodeName)







