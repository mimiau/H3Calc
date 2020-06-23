import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout,\
    QComboBox,QDialog, QVBoxLayout,QGroupBox, QGridLayout, QTextEdit, QLabel,\
    QRadioButton,QSpinBox, QListWidget, QTabWidget, QSizePolicy, QListWidgetItem
from PyQt5.Qt import QMimeData
from PyQt5.QtCore import *

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery,self).__init__(parent)
        self.originalPalette = QApplication.palette()
        
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()
        
        
        #self.createGuardWidget()
        self.createGuardiansStrengthWidget()
        self.createZonesOnMapWidget()
        self.createPandoraWidget()

        bottomTabs = QTabWidget()
        #bottomTabs.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Ignored)
        bottomTabs.addTab(self.PandoraWidget, "Pandora Calculator")
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.guardiansStrengthWidget,0,0)
        mainLayout.addWidget(self.zonesOnMapWidget,0,1)
        mainLayout.addWidget(bottomTabs,1,0,2,2)
        mainLayout.setRowStretch(2,2)
        self.setLayout(mainLayout)
        self.totalValue = 0

    def createGuardiansStrengthWidget(self):
        self.guardiansStrengthWidget = QGroupBox("Guardians strength:")

        self.globalMonstersStrength = {'Weak':2,'Normal':3,'Strong':4}
        globalLabel = QLabel('Global monster strength:')
        self.globalGuardiansStrength = QComboBox()
        
        self.globalGuardiansStrength.addItems(self.globalMonstersStrength)
        #self.globalGuardiansStrength.setCurrentIndex(1)

        self.zoneMonstersStrength = {'Weak':-1,'Average':0,'Strong':1}
        zoneLabel = QLabel('Zone monster strength:')
        self.zoneGuardianStrength = QComboBox()
        self.zoneGuardianStrength.addItems(self.zoneMonstersStrength)
        
        self.globalGuardiansStrength.currentTextChanged.connect(self.calculateValue)
        self.zoneGuardianStrength.currentTextChanged.connect(self.calculateValue)
        


        layout = QGridLayout()
        layout.addWidget(globalLabel,0,0)
        layout.addWidget(self.globalGuardiansStrength,0,1)
        layout.addWidget(zoneLabel,1,0)
        layout.addWidget(self.zoneGuardianStrength,1,1)
        self.guardiansStrengthWidget.setLayout(layout)
    
    def createZonesOnMapWidget(self):
        self.zonesOnMapWidget = QGroupBox("Zones on map:")

        zoneTypeLabel = QLabel("Zone type: ")
        self.ZoneType = QComboBox()
        self.ZoneType.addItems(['Castle','Rampart','Tower','Inferno','Necropolis','Dungeon','Stronghold','Fortress','Conflux','Cove','Neutral'])
        self.ZoneType.currentTextChanged.connect(self.chooseDwellings)

        currentZonesLabel = QLabel("Same type zones: ")
        self.currentZones = QSpinBox()
        self.currentZones.setValue(1)
        self.currentZones.setMinimum(1)
       
        allZonesLabel = QLabel("All zones:")
        self.allZones = QSpinBox()
        self.allZones.setMinimum(1)
        self.allZones.setValue(1)

        self.currentZones.valueChanged.connect(self.checkValues)
        self.allZones.valueChanged.connect(self.checkValues)
        self.currentZones.valueChanged.connect(self.calculateValue)
        self.allZones.valueChanged.connect(self.calculateValue)

        layout = QGridLayout()
        layout.addWidget(zoneTypeLabel,0,0)
        layout.addWidget(self.ZoneType,0,1)
        layout.addWidget(currentZonesLabel,1,0)
        layout.addWidget(self.currentZones,1,1)
        layout.addWidget(allZonesLabel,2,0)
        layout.addWidget(self.allZones,2,1)
        self.zonesOnMapWidget.setLayout(layout)

    def createPandoraWidget(self):
        self.PandoraWidget = QGroupBox()

        self.cursor.execute('SELECT name, value, growth FROM units')
        self.units_names = dict()
        for name, value, growth in self.cursor.fetchall():
            self.units_names[name] = [value,growth]
        self.cursor.execute('SELECT name, value FROM objects')
        self.object_names = dict(self.cursor.fetchall())
        self.cursor.execute('SELECT name,value FROM artifacts')
        self.artifacts_names = dict(self.cursor.fetchall())
        
        self.cursor.execute('SELECT name,value FROM objects WHERE name LIKE ? or name LIKE ? or name LIKE ?',['Pandora%','Spell%','Prison%'])
        self.unknown_objects = dict(self.cursor.fetchall())

        #print(self.objects_to_calculate)

        self.units = QComboBox()
        #self.units_names = [name[0] for name in self.units_names]
        self.units.addItems(sorted(self.units_names.keys()))
        #units.setContentsMargins(50,50,50,50)
        unitLabel = QLabel("&Guard:")
        unitLabel.setBuddy(self.units)
        self.units.currentTextChanged.connect(self.calculateValue)

        self.quantities = QComboBox()
        self.quantities.addItems(['Few 1-5','Several 5-9','Pack 10-19','Lots 20-49','Horde 50-99','Throng 100-249','Swarm 250-499','Zounds 500-999','Legion 1000-4000'])        
        
        
        self.objects = QComboBox()
        #self.object_names = [name[0] for name in self.object_names]
        self.objects.addItems(sorted(self.object_names.keys()))
        objectLabel = QLabel("&Objects:")
        objectLabel.setBuddy(self.objects)


        self.artifacts = QComboBox()
        #self.artifacts_names = [name[0] for name in self.artifacts_names]
        self.artifacts.addItems(sorted(self.artifacts_names.keys()))
        artifactLabel = QLabel("&Artifacts:")
        artifactLabel.setBuddy(self.artifacts)

        self.object_list = QListWidget()
        self.object_list.itemDoubleClicked.connect(lambda: self.object_list.takeItem(self.object_list.currentRow()))
        self.object_list.itemDoubleClicked.connect(self.calculateValue)
        
        add_object_button = QPushButton("Add object")
        add_object_button.clicked.connect(self.addObjectToList)

        add_artifact_button = QPushButton("Add artifact")
        add_artifact_button.clicked.connect(self.addArtifactToList)

        self.dwellings = QComboBox()
        #self.dwellings_names = [name[0] for name in self.dwellings_names]
        #self.dwellings.addItems(sorted(self.dwellings_names.keys()))
        self.chooseDwellings()
        dwellingsLabel = QLabel("&Dwellings:")
        dwellingsLabel.setBuddy(self.dwellings)

        add_dwelling_button = QPushButton("Add dwelling")
        add_dwelling_button.clicked.connect(self.addDwellingToList)
        #remove_last_object_button = QPushButton("Remove last")
        #remove_last_object_button.clicked.connect(self.removeLastObject)
        
        self.calculatedOutcome = QLabel()
        layout = QGridLayout()
        layout.addWidget(self.units,0,1)
        layout.addWidget(unitLabel,0,0)
        layout.addWidget(self.quantities,0,2)
        layout.addWidget(objectLabel,1,0)
        layout.addWidget(self.object_list,0,3,4,1)
        layout.addWidget(self.objects,1,1)
        layout.addWidget(add_object_button,1,2)
        layout.addWidget(artifactLabel,2,0)
        layout.addWidget(self.artifacts,2,1)
        layout.addWidget(add_artifact_button,2,2)
        layout.addWidget(dwellingsLabel,3,0)
        layout.addWidget(self.dwellings,3,1)
        layout.addWidget(add_dwelling_button,3,2)
        layout.addWidget(self.calculatedOutcome,0,7,2,2)
        #layout.addWidget(remove_last_object_button,2,3,1,2)

        self.PandoraWidget.setLayout(layout)

    def createGuardWidget(self):
        pass

    def checkValues(self):
            curr_value = self.currentZones.value()
            all_value = self.allZones.value()
            if all_value < curr_value:
                self.allZones.setValue(curr_value)

    def addObjectToList(self):
        #QTextEdit.setPlainText(self.PandoraWidget.object_list,'Stesa')
        #self.PandoraWidget.children.object_list.setPlainText('Button clicked')
        obj = self.objects.currentText()
        #self.objects_stack.append(obj)
        #self.cursor.execute('SELECT value FROM objects WHERE name = ?',[obj])
        #value = self.cursor.fetchall()[0][0]
        #self.totalValue += value
        self.object_list.addItem(obj)
        self.calculateValue()

    def addArtifactToList(self):
        art = self.artifacts.currentText()
        #self.artifacts_stack.append(art)
        #self.cursor.execute('SELECT value FROM artifacts WHERE name = ?',[art])
        #value = self.cursor.fetchall()[0][0]
        #self.totalValue += value
        self.object_list.addItem(art)
        self.calculateValue()
        #self.printAll()

    def addDwellingToList(self):
        dwelling = self.dwellings.currentText()
        self.object_list.addItem(dwelling)
        self.calculateValue()

    def calculateValue(self):
        self.totalValue=0
        items = []
        n = self.currentZones.value()
        N = self.allZones.value()
        for x in range(self.object_list.count()):
            items.append(self.object_list.item(x).text())

        objects_and_artifacts = {**self.object_names,**self.artifacts_names}
        for item in items:
            try:
                self.totalValue += objects_and_artifacts[item]
            except KeyError:
                unit = self.dwellings_names[item]
                unit_value = self.units_names[unit][0]
                unit_growth = self.units_names[unit][1]
                value = unit_value*((unit_growth)*(1+n/N)+n/2)
                self.totalValue += value
        #print('Total value: ' + str(self.totalValue))
        self.calculateGuard()

    def calculateGuard(self):
        object_value = self.totalValue
        global_text = self.globalGuardiansStrength.currentText()
        global_coeff = self.globalMonstersStrength[global_text]
        zone_text = self.zoneGuardianStrength.currentText()
        zone_coeff = self.zoneMonstersStrength[zone_text]
        protection_index = global_coeff + zone_coeff 
        minimal_value_1 = {1:2500,2:1500,3:1000,4:500,5:0}
        coefficient_1 = {1:0.5,2:0.75,3:1,4:1.5,5:1.5}
        minimal_value_2 = {1:7500,2:7500,3:7500,4:5000,5:5000}
        coefficient_2 = {1:0.5,2:0.75,3:1,4:1,5:1.5}
        #print('zone: '+ zone_text + ' ' + str(zone_coeff))
        #print('global: ' + global_text + ' '+ str(global_coeff))
        #print('prot index:' + str(protection_index))
        part_1 = object_value - minimal_value_1[protection_index]
        if part_1 < 0:
            part_1 = 0
        #print('min val 1:' + str(minimal_value_1[protection_index]))
        
        part_2 = object_value - minimal_value_2[protection_index]
        if part_2 < 0:
            part_2 = 0
        #print('min val 2:' + str(minimal_value_2[protection_index]))    
        
        total_AI_Value = part_1 * coefficient_1[protection_index] + part_2 * coefficient_2[protection_index]
        #print('total ai val:' +str(total_AI_Value))
        
        guardValue = self.units_names[self.units.currentText()][0]
        if total_AI_Value < 2000:
            #pass
            self.calculatedOutcome.setText('No protection')
        else:
            quantity = float(total_AI_Value/guardValue)
            self.calculateGuardRange(quantity)
            #self.calculatedOutcome.setText(str(quantity))

    def chooseDwellings(self):
        type = self.ZoneType.currentText()
        self.cursor.execute('SELECT name, creature FROM dwellings WHERE type =?',[type])
        self.dwellings_names = dict(self.cursor.fetchall())
        self.dwellings.clear()
        self.dwellings.addItems(self.dwellings_names.keys())

    def calculateGuardRange(self, quantity):
        quantity = round(quantity)
        #text = self.calculatedOutcome.text()
        text = '\nGuard range: '
        if quantity > 4:
            modifier = int(quantity/4)
            low = quantity - modifier
            high = quantity + modifier
            text = text + str(low)
            text = text + ' - '
            text = text + str(high)
            text = text + ' (' + str(quantity) + ')'
        else:
            text = text + str(quantity)
        self.calculatedOutcome.setText(text)
        #self.calcuateUnknownObject()
    
    def calcuateUnknownObject(self):
        guardRange = self.quantities.currentText().split(' ')[1]
        guardRange = guardRange.split('-')
        guardBottom = int(guardRange[0])
        guardTop = int(guardRange[1])
        value_of_the_list = self.totalValue
        for o, v in self.unknown_objects:
            self.totalValue += int(v)
            self.calculateGuard()
            self.totalValue = value_of_the_list

app = QApplication([])
window = WidgetGallery()
window.show()
app.exec_()