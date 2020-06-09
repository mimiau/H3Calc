import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QComboBox,QDialog, QVBoxLayout,QGroupBox, QGridLayout, QTextEdit, QLabel, QRadioButton,QSpinBox
from PyQt5.QtCore import *

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery,self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.createPandoraWidget()
        #self.createGuardWidget()
        self.createGuardiansStrengthWidget()
        self.createZonesOnMapWidget()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.guardiansStrengthWidget,0,0)
        mainLayout.addWidget(self.zonesOnMapWidget,0,1)
        mainLayout.addWidget(self.PandoraWidget,1,0,1,2)
        self.setLayout(mainLayout)
        self.objects_stack=[]

    def createGuardiansStrengthWidget(self):
        self.guardiansStrengthWidget = QGroupBox("Guardians strength:")

        weakRadioButton = QRadioButton("Weak")
        averageRadioButton = QRadioButton("Average")
        strongRadioButton = QRadioButton("Strong")
        weakRadioButton.setChecked(True)
        
        layout = QVBoxLayout()
        layout.addWidget(weakRadioButton)
        layout.addWidget(averageRadioButton)
        layout.addWidget(strongRadioButton)
        self.guardiansStrengthWidget.setLayout(layout)
    
    def createZonesOnMapWidget(self):
        self.zonesOnMapWidget = QGroupBox("Zones on map:")

        currentZonesLabel = QLabel("Same type zones: ")
        currentZones = QSpinBox()
        currentZones.setValue(1)
        currentZones.setMinimum(1)
       
        def checkValues(self):
            curr_value = currentZones.value()
            all_value = allZones.value()
            if all_value < curr_value:
                allZones.setValue(curr_value)
            
            

        allZonesLabel = QLabel("All zones:")
        allZones = QSpinBox()
        allZones.setMinimum(1)
        allZones.setValue(1)
        print(allZones.value())

        currentZones.valueChanged.connect(checkValues)
        allZones.valueChanged.connect(checkValues)

        layout = QGridLayout()
        layout.addWidget(currentZonesLabel,0,0)
        layout.addWidget(currentZones,0,1)
        layout.addWidget(allZonesLabel,1,0)
        layout.addWidget(allZones,1,1)
        self.zonesOnMapWidget.setLayout(layout)

    def createPandoraWidget(self):
        self.PandoraWidget = QGroupBox("Pandora calculator")
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM units')
        units_names = cursor.fetchall()
        cursor.execute('SELECT name FROM objects')
        object_names = cursor.fetchall()
        cursor.execute('SELECT name FROM artifacts')
        artifacts_names = cursor.fetchall()


        self.units = QComboBox()
        self.units.addItems([name[0] for name in units_names])
        #units.setContentsMargins(50,50,50,50)
        unitLabel = QLabel("&Guard:")
        unitLabel.setBuddy(self.units)

        quantities = QComboBox()
        quantities.addItems(['Few 1-5','Several 5-9','Pack 10-19','Lots 20-49','Horde 50-99','Throng 100-249','Swarm 250-499','Zounds 500-999','Legion 1000-4000'])        
        
        
        self.objects = QComboBox()
        self.objects.addItems([name[0] for name in object_names])
        objectLabel = QLabel("&Objects:")
        objectLabel.setBuddy(self.objects)


        self.artifacts = QComboBox()
        self.artifacts.addItems([name[0] for name in artifacts_names])
        artifactLabel = QLabel("&Artifacts:")
        artifactLabel.setBuddy(self.artifacts)

        self.object_list = QTextEdit()
        self.object_list.setWindowTitle("Objects behind guard")
        self.object_list.setReadOnly(True)
        #self.object_list.setPlainText('TEST')
        
        add_object_button = QPushButton("Add object")
        add_object_button.clicked.connect(self.addObjectToList)

        add_artifact_button = QPushButton("Add artifact")
        add_artifact_button.clicked.connect(self.addArtifactToList)

        remove_last_object_button = QPushButton("Remove last")
        remove_last_object_button.clicked.connect(self.removeLastObject)
        
        layout = QGridLayout()
        layout.addWidget(self.units,0,1)
        layout.addWidget(unitLabel,0,0)
        layout.addWidget(quantities,0,2)
        layout.addWidget(objectLabel,1,0)
        layout.addWidget(self.object_list,0,3,2,2)
        layout.addWidget(self.objects,1,1)
        layout.addWidget(add_object_button,1,2)
        layout.addWidget(artifactLabel,2,0)
        layout.addWidget(self.artifacts,2,1)
        layout.addWidget(add_artifact_button,2,2)
        layout.addWidget(remove_last_object_button,2,3,1,2)

        self.PandoraWidget.setLayout(layout)

    def createGuardWidget(self):
        pass

    def addObjectToList(self):
        #QTextEdit.setPlainText(self.PandoraWidget.object_list,'Stesa')
        #self.PandoraWidget.children.object_list.setPlainText('Button clicked')
        self.objects_stack.append(self.objects.currentText())
        self.printObjects()

    def addArtifactToList(self):
        self.objects_stack.append(self.artifacts.currentText())
        self.printObjects()
    
    def printObjects(self):
        text_to_print = ""
        for object in self.objects_stack:
            text_to_print += object
            text_to_print += '\n'
        self.object_list.setPlainText(text_to_print)

    def removeLastObject(self):
        try:
            del self.objects_stack[-1]
        except IndexError:
            pass
        self.printObjects()
#cursor.execute('SELECT name from objects')
#objects_names = cursor.fetchall()

app = QApplication([])
window = WidgetGallery()

#vlayout = QVBoxLayout()
#QHBoxLayout.setContentsMargins(layout,50,50,50,50)

#objects = QComboBox()
#objects.addItems([name[0] for name in objects_names])
#vlayout.addWidget(objects)#

#window.setLayout(layout)
#window.setLayout(vlayout)
window.show()
app.exec_()