#Imports
import time
import os.path
import PyQt5.uic
from krita import *
from krita import DockWidget
from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QDialog

#Docker code
DOCKER_TITLE = 'Shading Helper'

class EsinsShadingDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.UIElements()
    
    def UIElements(self):
        #Thanks to EyeOdin for this
        self.directory_plugin = str(os.path.dirname(os.path.realpath(__file__)))
        self.layout = uic.loadUi(os.path.normpath(self.directory_plugin + "/ShadingHelper.ui"), QWidget())
        self.setWidget(self.layout)
        self.layout.StartChanging.clicked.connect(self.ChangingColors)

    def ChangingColors(self):
        #Thanks to Grum999 for most parts of the script
        document=Krita.instance().activeDocument()
        node=document.activeNode()
        activeView = Krita.instance().activeWindow().activeView()
        w=document.width()
        h=document.height()

        hueRangeStartOne=self.layout.Hue1.value()
        hueRangeEndOne=self.layout.Hue2.value()

        

        selection = Selection()
        selection.select(0, 0, w, h, 0)
        selPixelData=bytearray(selection.pixelData(0, 0, w, h))

        pixelData=bytearray(node.pixelData(0, 0, w, h))

        offset=0
        color=QColor()
        selOffset=0
        for offset in range(0,len(pixelData),4):
            # note: pixel data are returned as BGRA order and not RGBA order
            color.setRgb(pixelData[offset+2], pixelData[offset+1], pixelData[offset], pixelData[offset+3])
            if color.hue()>=hueRangeStartOne and color.hue()<=hueRangeEndOne:
                selPixelData[selOffset]=255
            selOffset+=1            
                
        selection.setPixelData(QByteArray(selPixelData),0,0,w,h)
        document.setSelection(selection)
        #selection.

        HexChangeRaw1 = self.layout.NewColorHex1.text()
        HexChangeLO1 = HexChangeRaw1.replace("#","")
        HexChangeLO1 = HexChangeLO1.strip()
        print(HexChangeLO1)

        """HexChangeRaw2 = self.layout.NewColorHex2.text()
        HexChangeLO2 = HexChangeRaw2.replace("#","")
        HexChangeLO2 = HexChangeLO2.strip()
        print(HexChangeLO2)"""

        #Thanks to 30secondsofcode.org. They really saved my ass in this one!
        def HextoBGR(hex):
            amogus = list(int(hex[i:i+2], 16) for i in (0, 2, 4))
            amogus.reverse()
            return amogus

        print(HextoBGR(HexChangeLO1))
        #print(HextoBGR(HexChangeLO2))

        NewColor1 = ManagedColor("RGBA", "U8", "")
        Color1Components = NewColor1.components()
        Color1Components[0] = (float(str((HextoBGR(HexChangeLO1)[0] / 255))[:5])) #Blue
        Color1Components[1] = (float(str((HextoBGR(HexChangeLO1)[1] / 255))[:5])) #Green
        Color1Components[2] = (float(str((HextoBGR(HexChangeLO1)[2] / 255))[:5])) #Red
        Color1Components[3] = 1.0 #Alpha (Currently fixed value)
        print(Color1Components)
        NewColor1.setComponents(Color1Components)

        activeView.setForeGroundColor(NewColor1)
        document.setActiveNode(document.nodeByName("Shading"))
        Krita.instance().action("fill_selection_foreground_color").trigger()
        Krita.instance().action("deselect").trigger()
        document.refreshProjection()


        ChangedDialog = QDialog() # create dialog and assign it to a variable
        ChangedDialog.setWindowTitle("Esin's shading helper")
        ChangedDialog.layout = QVBoxLayout()
        message = QLabel("The colors have been changed.")
        ChangedDialog.layout.addWidget(message)
        ChangedDialog.setLayout(ChangedDialog.layout)
        ChangedDialog.exec_() # show the dialog


    def canvasChanged(self, canvas):
        pass
