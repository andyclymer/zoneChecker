# -*- coding: utf-8 -*-

from AppKit import NSColor, NSFont, NSFontAttributeName, NSForegroundColorAttributeName, NSCursor
from mojo.events import installTool, EditingTool, BaseEventTool, setActiveEventTool
from mojo.drawingTools import *
from mojo.UI import UpdateCurrentGlyphView
from defconAppKit.windows.baseWindow import BaseWindowController

import vanilla

from mojo.extensions import ExtensionBundle
shapeBundle = ExtensionBundle("ZoneChecker")
toolbarIcon = shapeBundle.get("ZoneCheckerButton")

"""


    Zonechecker
    
    Check for points near the alignment zones.


"""


class ZoneCheckerTool(EditingTool):

    zoneCheckerToolPrefsLibKey = "com.letterror.zoneChecker.prefs"
    textAttributes = {
        NSFontAttributeName : NSFont.systemFontOfSize_(10),
        NSForegroundColorAttributeName : NSColor.whiteColor(),
    }
    
    margin = 3    # how far off are points?
    def setup(self):
        self.markColor = (    255/255.0,    0/255.0,    0/255.0,     0.8)
        self.okColor = (      0/255.0,      0/255.0,    255/255.0,   0.8)
        self.outside = []
        self.inside = []
    
    def _p(self, items):
        if len(items)%2!=0:
            return []
        return [(items[i], items[i+1]) for i in range(0, len(items)-1, 2)]
        
    def findMisalignedPoints(self):
        g = CurrentGlyph()
        f = CurrentFont()
        if f is None:
            return
        if not g: 
            return

        self.outside = []
        self.inside = []
        zones = []
        
        for a, b in self._p(f.info.postscriptBlueValues):
            zones.append((a,b))
        for a, b in self._p(f.info.postscriptOtherBlues):
            zones.append((a,b))
        for a, b in self._p(f.info.postscriptFamilyBlues):
            zones.append((a,b))
        for c in g.contours:
            for p in c.points:
                if p.type == "offCurve":
                    continue
                y = p.y
                for a, b in zones:
                    if (a-self.margin < y < b+self.margin):
                        if not (a <= y <= b):
                            self.outside.append((p.x, p.y))
                        else:
                            self.inside.append((p.x, p.y))
        
    def draw(self, scale):
        self.findMisalignedPoints()
        if scale == 0:
            return
        save()
        fill(None)
        for x, y in self.outside:
            d = scale * 25
            d2 = 2*d
            strokeWidth(20*scale)
            stroke(self.markColor[0],self.markColor[1],self.markColor[2],self.markColor[3])
            oval(x-d, y-d, d2, d2)
        for x, y in self.inside:
            d = scale * 9
            d2 = 2*d
            strokeWidth(2*scale)
            stroke(self.okColor[0],self.okColor[1],self.okColor[2],self.okColor[3])
            oval(x-d, y-d, d2, d2)
        restore()

        # self.getNSView()._drawTextAtPoint(
        #     "%3.2f"%(100-100*level),
        #     self.textAttributes,
        #     tp,
        #     yOffset=-30,
        #     drawBackground=True,
        #     backgroundColor=NSColor.blueColor())

    def mouseDown(self, point, event):
        pass
        # mods = self.getModifiers()
        # cmd = mods['commandDown'] > 0
        # self.isResizing = False
        # if cmd:
        #     self.clear()
            
    def clear(self):
        self.marked = None
        pass
        # self.pts = []
        # self.dupes = set()
        # self.samples = {}
    
    def keyDown(self, event):
        pass
        # letter = event.characters()
        # if letter == "i":
        #     # invert the paint color on drawing
        #     self.prefs['invert'] = not self.prefs['invert']
        #     self.storePrefs()
        # UpdateCurrentGlyphView()
        
    def mouseDragged(self, point, delta):
        """ Calculate the blurred gray level for this point. """
        pass

    def getToolbarTip(self):
        return 'ZoneChecker'

    def getToolbarIcon(self):
        ## return the toolbar icon
        return toolbarIcon

    
p = ZoneCheckerTool()
installTool(p)
