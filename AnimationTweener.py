#===================
#patrvq@interia.pl
#Learning resources
#Maya Python API Course
#===================

#AnimationTweener

from maya import cmds


def tween(percentage, obj=None, attrs=None, selection=True):
    """
    This function will tween the keyed attributes on an object.
    Args:
        percentage (float): This is a mandatory argument and will be the percentage to tween
        obj (str): the name of the object to use. This is optional since it has a default value
        attrs (list): A list of the attributes to tween. This is optional since it has a default value
        selection (bool):
    """

    if not obj and not selection:
        raise ValueError("No object given to tween")

    if not obj:
        obj = cmds.ls(sl=1)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

    currentTime = cmds.currentTime(query=True)

    # Loop through all the attributes
    for attr in attrs:
        attrFull = '%s.%s' % (obj, attr)
        keyframes = cmds.keyframe(attrFull, query=True)
        if not keyframes:
            continue
        previousKeyframes = []
        for k in keyframes:
            if k < currentTime:
                previousKeyframes.append(k)

        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        if previousKeyframes:
            previousFrame = max(previousKeyframes)
        else:
            previousFrame = None

        nextFrame = min(laterKeyframes) if laterKeyframes else None

        if previousFrame is None:
            previousFrame = nextFrame

        nextFrame = previousFrame if nextFrame is None else nextFrame

        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        if nextFrame is None:
            currentValue = previousValue
        elif previousFrame is None:
            currentValue = nextValue
        elif previousValue == nextValue:
            currentValue = previousValue
        else:
            difference = nextValue - previousValue
            biasedDifference = (difference * percentage) / 100.0
            currentValue = previousValue + biasedDifference

        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)


class TweenerWindow(object):
    windowName = "TweenerWindow"

    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")
        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        cmds.button(label="Reset", command=self.reset)
        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)

    def close(self, *args):
        cmds.deleteUI(self.windowName)