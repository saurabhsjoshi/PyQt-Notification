###############################
#                             #
#  Coded By: Saurabh Joshi    #
#  Original: 12/10/12         #
#  Date Modified: 8/12/12     #
#                             #
#  File: Notification System  #
###############################

import sys
from PyQt4 import QtCore, QtGui
OS = 0

try:
    from ctypes import windll
except:
    global OS
    OS = 1
import time

MSSG = ''

from ui_notification import Ui_Notification

class Notification(QtGui.QMainWindow):
    closed = QtCore.pyqtSignal()
    
    def __init__(self,mssg,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.parent = parent
        global MSSG
        MSSG = mssg
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_Notification()
        self.ui.setupUi(self)
        
        self.createNotification(MSSG)
        
    def closeEvent(self,event):
        self.close.emit()
        
    def createNotification(self,mssg):
        global OS
        if (OS!= 1):
            user32 = windll.user32
            #Get X coordinate of screen
            self.x = user32.GetSystemMetrics(0)
        else:
            cp = QtGui.QDesktopWidget().availableGeometry()
            self.x = cp.width()

        #Set the opacity
        self.f = 1.0

        #Set the message 
        self.ui.lbl_mssg.setText(mssg)

        #Start Worker
        self.workThread = WorkThread()
        self.connect( self.workThread, QtCore.SIGNAL("update(QString)"), self.animate )
        self.connect( self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
        self.connect( self.workThread, QtCore.SIGNAL("finished()"), self.done)
        
        self.workThread.start()
        return

    #Quit when done
    def done(self):
        self.hide()
        return

    #Reduce opacity of the window
    def disappear(self):
        self.f -= 0.02
        self.setWindowOpacity(self.f)
        return
        
        
    #Move in animation
    def animate(self):
        self.move(self.x,0)
        self.x -= 1
        return
        
        

#The Worker
class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        #Bring em in :D
        for i in range(336):
            time.sleep(0.0001)
            self.emit( QtCore.SIGNAL('update(QString)'), "ping" )
        #Hide u bitch :P
        for j in range(50):
            time.sleep(0.1)
            self.emit( QtCore.SIGNAL('vanish(QString)'), "ping" )
        return
def Notify(msg):
    app = QtGui.QApplication(sys.argv)
    myapp = Notification(msg)
    myapp.show()
    sys.exit(app.exec_())

     

        
        
        
