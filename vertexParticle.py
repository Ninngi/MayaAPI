#=========================================================
#Patryk Pawlak
#patrvq@interia.pl
#Chayan Vinayak`s course "Maya Python API"
#========================================================

# still reDoIt issues ;C /// Fixed just remember that doIt undoIt and so on has to be writen with proper lower/upper case !!!!

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
import maya.OpenMayaFX as OpenMayaFX


commandName = 'vertexParticle'

kHelpFlag = '-h'
kHelpLongFlag = '-help'
kSparseFlag = '-s'
kSparseLongFlag = '-sparse'
helpMessage = 'This command is used to attach a particle on each vertex of a poly mesh'

class pluginCommand(OpenMayaMPx.MPxCommand):

    mObj_particle = OpenMaya.MObject()
    sparse = None
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def argumentParser(self, argList):
        syntax = self.syntax()
        try:
            parsedArguments = OpenMaya.MArgDatabase(syntax, argList)
        except:
            print 'Inccorrect Argument'
            return 'unknown'
        if parsedArguments.isFlagSet(kSparseFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseFlag, 0)
            return None
        if parsedArguments.isFlagSet(kSparseLongFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseLongFlag, 0)
            return None

        if parsedArguments.isFlagSet(kHelpFlag):
            self.setResult(helpMessage)
            return None
        if parsedArguments.isFlagSet(kHelpLongFlag):
            self.setResult(helpMessage)
            return None

    def isUndoable(self):
        return True

    def undoIt(self):
        mFnDagNode = OpenMaya.MFnDagNode(self.mObj_particle)
        mDagMod = OpenMaya.MDagModifier()
        if self.mObj_particle.apiTypeStr()!="kInvalid":
            mDagMod.deleteNode(mFnDagNode.parent(0))
            mDagMod.doIt()
            self.mObj_particle = OpenMaya.MObject()
        return None
        '''
          mDagMod.deleteNode(mFnDagNode.parent(0))  # Delete particle system
        mDagMod.doIt()
        return None
        '''

    def redoIt(self):
        mSel = OpenMaya.MSelectionList()
        mDagPath = OpenMaya.MDagPath()
        mFnMesh = OpenMaya.MFnMesh()
        OpenMaya.MGlobal.getActiveSelectionList(mSel)
        if mSel.length() >= 1:
            try:
                mSel.getDagPath(0, mDagPath)
                mFnMesh.setObject(mDagPath)
            except:
                print 'Select a poly mesh'
                return 'unknown'
        else:
            print 'Select a poly mesh'
            return 'unknown'

        mPointArray = OpenMaya.MPointArray()
        mFnMesh.getPoints(mPointArray, OpenMaya.MSpace.kWorld)

        # Create particle system
        mFnParticle = OpenMayaFX.MFnParticleSystem() #it may not work !!!
        self.mObj_particle = mFnParticle.create()

        # To fix bug
        mFnParticle = OpenMayaFX.MFnParticleSystem(self.mObj_particle) # << Optional

        counter = 0
        for i in xrange(mPointArray.length()):
            if i%self.sparse == 0:
                mFnParticle.emit(mPointArray[i])
                counter += 1
        print 'Total points :' + str(counter)
        mFnParticle.saveInitialState()
        return None

    def doIt(self, argList):
        print 'creating Particles ...'
        self.argumentParser(argList)
        print self.sparse
        if self.sparse != None:
            self.redoIt()
        return None

#Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(pluginCommand())

def syntaxCreator():
    #Create MSyntax object
    syntax = OpenMaya.MSyntax()

    #collect/add the flags
    syntax.addFlag(kHelpFlag, kHelpLongFlag)
    syntax.addFlag(kSparseFlag, kSparseLongFlag, OpenMaya.MSyntax.kDouble)

    # return MSyntax
    return syntax

#Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(commandName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command %s\n' + commandName)

#Uninitialize
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(commandName)
    except:
        sys.stderr.write('Failed to de-register command %s\n' + commandName)
# .
