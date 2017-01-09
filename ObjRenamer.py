from maya import cmds

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

SUFFIXES = {
	"mesh": "geo",
	"joint": "jnt",
	"camera": None,
	"ambientLight": "lgt"
}

DEFAULT_SUFFIX = "grp"

def rename(selection=False):
	'''
	This function will rename any objects to have the correct suffix
	Args:
	    selection: Whether or not we use the current selection

	Returns:
	    A list of all the objects we opereted on

	'''

	objects = cmds.ls(selection=selection, dag=True, long=True)


	# This function cannot run if there is no selection and no objects
	if selection and not objects:
		raise RuntimeError("You dont have anything selected!!! How it come?")

	objects.sort(key=len, reverse=True)

	for obj in objects:
		shortName = obj.split("|")[-1]

		children = cmds.listRelatives(obj, children=True, fullPath=True) or []

		if len(children) == 1:
			child = children[0]
			objType = cmds.objectType(child)
		else:
			objType = cmds.objectType(obj)

		suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

		if not suffix:
			continue

		if obj.endswith('_'+suffix):
			continue

		#newName = shortName + "_" + suffix
		newName = "%s_%s" % (shortName, suffix)
		cmds.rename(obj, newName)

		index = objects.index(obj)
		objects[index] = obj.replace(shortName, newName)

	return objects

