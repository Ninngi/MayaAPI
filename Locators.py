# ===================
# patrvq@interia.pl
# Learning resources
# Maya Python API Course
# ===================

# Locators

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender

nodeName = "LeftFoot"
nodeId = OpenMaya.MTypeId(0x100fff)

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()


class LocatorNode(OpenMayaMPx.MPxLocatorNode):
    def __init__(self):
        OpenMayaMPx.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        return OpenMaya.kUnknownParameter

    def draw(self, view, path, style, status):
        view.beginGL()
        # Pushed current state
        glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
        # Enabled Blend mode (to enable transparency)
        glFT.glEnable(OpenMayaRender.MGL_BLEND)
        # Defined Blend function
        glFT.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)

        # Define colors for different selection modes
        if status == view.kActive:
            glFT.glColor4f(0.2, 0.5, 0.1, 0.3)
        elif status == view.kLead:
            glFT.glColor4f(0.5, 0.2, 0.1, 0.3)
        elif status == view.kDormant:
            glFT.glColor4f(0.1, 0.1, 0.1, 0.3)

        # Draw a shape
        glFT.glBegin(OpenMayaRender.MGL_POLYGON)
        glFT.glVertex3f(-0.031, 0, -2.875)
        glFT.glVertex3f(-0.939, 0.1, -2.370)
        glFT.glVertex3f(-1.175, 0.2, -1.731)
        glFT.glVertex3f(-0.603, 0.3, 1.060)
        glFT.glVertex3f(0.473, 0.3, 1.026)
        glFT.glVertex3f(0.977, 0.2, -1.731)
        glFT.glVertex3f(0.809, 0.1, -2.337)
        glFT.glVertex3f(0.035, 0, -2.807)
        glFT.glEnd()

        # Draw a shape
        glFT.glBegin(OpenMayaRender.MGL_POLYGON)
        glFT.glVertex3f(-0.587, 0.3, 1.33)
        glFT.glVertex3f(0.442, 0.3, 1.33)
        glFT.glVertex3f(0.442, 0.3, 1.92)
        glFT.glVertex3f(0.230, 0.3, 2.24)
        glFT.glVertex3f(-0.442, 0.3, 2.25)
        glFT.glVertex3f(-0.635, 0.3, 1.92)
        glFT.glVertex3f(-0.567, 0.3, 1.35)
        glFT.glEnd()

        # Define colors for different selection modes
        if status == view.kActive:
            glFT.glColor4f(0.2, 0.5, 0.1, 1)
        elif status == view.kLead:
            glFT.glColor4f(0.5, 0.2, 0.1, 1)
        elif status == view.kDormant:
            glFT.glColor4f(0.1, 0.1, 0.1, 1)

        view.drawText("Left Foot", OpenMaya.MPoint(0, 0, 0), view.kLeft)
        # Disable Blend mode
        glFT.glDisable(OpenMayaRender.MGL_BLEND)
        # Restore the state
        glFT.glPopAttrib()
        view.endGL()


def nodeCreator():
    return OpenMayaMPx.asMPxPtr(LocatorNode())


def nodeInitializer():
    pass


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        sys.stderr.write("Failed to register command: %s\n" % nodeName)


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(nodeName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % nodeName)