import maya.OpenMaya as OpenMaya

# 1. Create a Selection List
mSel = OpenMaya.MSelectionList()
mSel.add("pPlane1")

# 2. Create MObject and MDagPath
mObj = OpenMaya.MObject()
mDagPath = OpenMaya.MDagPath()

# 3. Request Dependecy Node and Dag Path of the object
mSel.getDependNode(0,mObj)
mSel.getDagPath(0,mDagPath)

# 4. Mesh function set
mFnMesh = OpenMaya.MFnMesh(mDagPath)
mFnMesh.fullPathName()

# 5. Dependecy Node function set
mFnDependNode = OpenMaya.MFnDependencyNode(mObj)

# 6. get all the connections of a Shape Node
mPlugArray = OpenMaya.MPlugArray()
mFnMesh.getConnections(mPlugArray)

mPlugArray.length()
print mPlugArray[0].name()
print mPlugArray[1].name()

mPlugArray_connections = OpenMaya.MPlugArray()
mPlugArray[1].connectedTo(mPlugArray_connections, True, False)

mPlugArray_connections.length()
# Can not be used: len(mPlugArray_connections)

print mPlugArray_connections[0].name()

mObj2 = mPlugArray_connections[0].node()

mFnDependNode2 = OpenMaya.MFnDependencyNode(mObj2)
print mFnDependNode2.name()

mPlug_width = mFnDependNode2.findPlug("width")
mPlug_height = mFnDependNode2.findPlug("height")

print mPlug_width.asInt()
print mPlug_height.asInt()

mPlug_subWidth = mFnDependNode2.findPlug("subdivisionsWidth")
mPlug_subHeight = mFnDependNode2.findPlug("subdivisionsHeight")

mPlug_subWidth.setInt(10)
mPlug_height.setInt(10)

 

