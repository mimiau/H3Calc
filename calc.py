import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QComboBox,QDialog, QVBoxLayout,QGroupBox, QGridLayout, QTextEdit
from PyQt5.QtCore import *

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery,self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.createPandoraWidget()
        #self.createGuardWidget()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.PandoraWidget)
        self.setLayout(mainLayout)
        self.objects_stack=[]



    def createPandoraWidget(self):
        self.PandoraWidget = QGroupBox("Pandora calculator")
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM units')
        units_names = cursor.fetchall()
        cursor.execute('SELECT name FROM objects')
        object_names = cursor.fetchall()

        self.units = QComboBox()
        self.units.addItems([name[0] for name in units_names])
        #units.setContentsMargins(50,50,50,50)
        
        quantities = QComboBox()
        quantities.addItems(['Few 1-5','Several 5-9','Pack 10-19','Lots 20-49','Horde 50-99','Throng 100-249','Swarm 250-499','Zounds 500-999','Legion 1000-4000'])        
        
        self.objects = QComboBox()
        self.objects.addItems([name[0] for name in object_names])
        
        self.object_list = QTextEdit()
        self.object_list.setWindowTitle("Objects behind guard")
        self.object_list.setDisabled(True)
        #self.object_list.setPlainText('TEST')
        
        add_object_button = QPushButton("Add object")
        add_object_button.clicked.connect(self.addObjectToList)

        remove_last_object_button = QPushButton("Remove last object")
        remove_last_object_button.clicked.connect(self.removeLastObject)
        
        layout = QGridLayout()
        layout.addWidget(self.units,0,0)
        layout.addWidget(quantities,0,1)
        layout.addWidget(self.object_list,0,3,2,2)
        layout.addWidget(self.objects,1,0)
        layout.addWidget(add_object_button,1,1)
        layout.addWidget(remove_last_object_button,2,3)

        self.PandoraWidget.setLayout(layout)

    def createGuardWidget(self):
        pass

    def addObjectToList(self):
        #QTextEdit.setPlainText(self.PandoraWidget.object_list,'Stesa')
        #self.PandoraWidget.children.object_list.setPlainText('Button clicked')
        self.objects_stack.append(self.objects.currentText())
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