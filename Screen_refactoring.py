import sys
import cv2, imutils
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import time
import datetime


class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec = 0, parent= None):
        super().__init__()
        self.running = True #thread start condition

    def run(self):
        while self.running == True :
            self.update.emit()
            time.sleep(0.1)
    
    def stop(self):
        self.running = False

from_class = uic.loadUiType("./screen.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.isCameraOn = False
        self.isRecStart = False

        self.isRedOn = False
        self.isGreenOn = False
        self.isBlueOn = False
        
        self.isBlurOn = False
        self.isHSVOn = False
        self.isBinaryOn = False

        self.threshold_value = 128


        self.btnRecord.hide()
        self.btnSave.hide()

        
        self.x = None
        self.y = None
        self.start_point = None
        self.end_point = None

        self.RGB_MIN = 0
        self.RGB_MAX = 255
    
        self.pixmap = QPixmap()

        self.camera = Camera(self)
        self.camera.daemon = True

        self.record = Camera(self)
        self.record.daemon = True

        self.btnLoad.clicked.connect(self.loadFile)
        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.btnSave.clicked.connect(self.save)

        self.btnRed.clicked.connect(self.changeR)
        self.btnGreen.clicked.connect(self.changeG)
        self.btnBlue.clicked.connect(self.changeB)

        self.btnHSV.clicked.connect(self.changeHSV)

        self.blur.clicked.connect(self.changeBlur)
        
        self.binary.clicked.connect(self.changeBinary)
        self.threshold.returnPressed.connect(self.addValue)
    
    def addValue(self):
        self.threshold_value = int(self.threshold.text())


    def changeBinary(self):
        if self.isBinaryOn == False:
            self.isBinaryOn = True
            self.image_copy = self.image.copy()
            gray_image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            _, self.image = cv2.threshold(gray_image, self.threshold_value, 255, cv2.THRESH_BINARY)
            h,w = self.image.shape
            qimage = QImage(self.image.data, w,h,w, QImage.Format_Grayscale8)

        else:
            self.isBinaryOn = False
            self.image = self.image_copy

            h,w,c = self.image.shape
            qimage = QImage(self.image.data, w,h,w*c, QImage.Format_RGB888)


        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.screen.width(),self.screen.height())
        self.screen.setPixmap(self.pixmap)
        

    def changeHSV(self):
        if self.isHSVOn == False:
            self.isHSVOn = True
            self.image_copy = self.image.copy()
            self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)

        else:
            self.isHSVOn = False
            self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
            self.image = self.image_copy

        h,w,c = self.image.shape
        qimage = QImage(self.image.data, w,h,w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.screen.width(),self.screen.height())
        self.screen.setPixmap(self.pixmap)



    def changeBlur(self):
        if self.isBlurOn == False:
            self.isBlurOn = True
            self.image_copy = self.image.copy()
            self.image = cv2.GaussianBlur(self.image, (75, 75), 0)
        else:
            self.isBlurOn = False
            self.image = self.image_copy

        h,w,c = self.image.shape
        qimage = QImage(self.image.data, w,h,w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.screen.width(),self.screen.height())
        self.screen.setPixmap(self.pixmap)
    

    def changeR(self):
        
        if self.isRedOn == False:
            self.isRedOn = True
            self.image_copy = self.image.copy()
            self.onlyRed()
        else:
            self.isRedOn = False
            self.image = self.image_copy
       
        h, w, c = self.image.shape
        q_image = QImage(self.image.data, w, h, w * c, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.screen.width(),self.screen.height())

        self.screen.setPixmap(pixmap)

    def changeG(self):
        
        if self.isGreenOn == False:
            self.isGreenOn = True
            self.image_copy = self.image.copy()
            self.onlyGreen()
        else:
            self.isGreenOn = False
            self.image = self.image_copy
        h, w, c = self.image.shape
        q_image = QImage(self.image.data, w, h, w * c, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.screen.width(),self.screen.height())

        self.screen.setPixmap(pixmap)

    def changeB(self):
        
        if self.isBlueOn == False:
            self.isBlueOn = True
            self.image_copy = self.image.copy()
            self.onlyBlue()
        else:
            self.isBlueOn = False
            self.image = self.image_copy
       
        h, w, c = self.image.shape
        q_image = QImage(self.image.data, w, h, w * c, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.screen.width(),self.screen.height())

        self.screen.setPixmap(pixmap)

    def onlyRed(self):
        self.image[:,:,1] = 0
        self.image[:,:,2] = 0
        self.isGreenOn = False
        self.isBlueOn = False

    def onlyGreen(self):
        self.image[:,:,0] = 0
        self.image[:,:,2] = 0
        self.isRedOn = False
        self.isBlueOn = False

    def onlyBlue(self):
        self.image[:,:,0] = 0
        self.image[:,:,1] = 0
        self.isRedOn = False
        self.isGreenOn = False
       
    def save(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + ".png"
        
        # QPixmap 저장
        self.screen.pixmap().save(filename)


    def updateRecording(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        self.writer.write(self.image)
        

    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText("Rec stop")
            self.isRecStart = True

            self.recordingStart()


        else:
            self.btnRecord.setText("Rec start")
            self.isRecStart = False

            self.recordingStop()


    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + ".avi"
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w,h))


    def recordingStop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()


    def clickCamera(self):
        if self.isCameraOn == False:
            self.cameraStart()

        else:
            self.cameraStop()


    def cameraStart(self):
        self.btnCamera.setText("Camera off")
        self.isCameraOn = True
        self.btnRecord.show()
        self.btnSave.show()

        self.camera.running =True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)


    def cameraStop(self):
        self.btnCamera.setText("Camera on")
        self.isCameraOn = False
        self.btnRecord.hide()
        self.pixmap.fill(Qt.black)
        self.screen.setPixmap(self.pixmap)
        self.btnSave.hide()

        self.camera.running = False
        self.video.release()
    

    def updateCamera(self):
        
        retval, image = self.video.read()
        if retval:
            
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if self.isRedOn == True:
                self.onlyRed()
            
            if self.isGreenOn == True:
                self.onlyGreen()

            if self.isBlueOn == True:
                self.onlyBlue()

            if self.isBlurOn == True:
                self.image = cv2.GaussianBlur(self.image, (75, 75), 0)

            if self.isHSVOn == True:
                self.image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
                           
            h,w,c = self.image.shape

            qimage = QImage(self.image.data, w,h,w*c,QImage.Format_RGB888)

            if self.isBinaryOn == True:
                gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                h,w = gray_image.shape
                c = 1
                _, self.image = cv2.threshold(gray_image, self.threshold_value, 255, cv2.THRESH_BINARY)

                qimage = QImage(self.image.data, w,h,w,QImage.Format_Grayscale8)


            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.screen.width(),self.screen.height())

            self.screen.setPixmap(self.pixmap)


    def loadFile(self):
        if self.isCameraOn:
            self.cameraStop()

        file,_ = QFileDialog.getOpenFileName(self, "Open File", filter = "Video Files (*.*);;Image (*.*)")

        if file:
            if file.lower().endswith((".png",".jpg",".jpeg")):
                self.display_image(file)
                self.btnSave.show()

            else:
                self.open_video(file)
    
    def get_image(self,file):
        image = cv2.imread(file)
        return image
    
    def get_convert(self,src,cv2_format):
        image = cv2.cvt(src,cv2_format)
        return image
    
    def set_Qimage_format(self,data,w,h,c,Qimage_format):
        qimage = QImage(data, w,h,w*c, Qimage_format)
        return qimage

    def get_WHC(self,image):
        image.shape
        if len(image.shape) == 3:
            w,h,c = image.shape
            return w,h,c
        else:
            w,h = image.shape
            c = 1
            return w,h,c 
  

    def set_pixmap(self):

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.screen.width(),self.screen.height())

        self.screen.setPixmap(self.pixmap)


    def display_image(self,file):
        self.image = cv2.imread(file)
        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
        
        h,w,c = self.image.shape
        qimage = QImage(self.image.data, w,h,w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.screen.width(),self.screen.height())

        self.screen.setPixmap(self.pixmap)


    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.start_point = self.screen.mapFromGlobal(event.globalPos())


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = self.screen.mapFromGlobal(event.globalPos())
            self.draw_line()


    def draw_line(self):
        if self.start_point and self.end_point:
            painter = QPainter(self.screen.pixmap())
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
            painter.drawLine(self.start_point, self.end_point)
            self.update()
            self.start_point = None
            self.end_point = None        

    
    def open_video(self,file):
        if self.isCameraOn:
            self.cameraStop()
        
        self.video = cv2.VideoCapture(file)
        if not self.video.isOpened():
            QMessageBox.warning(self, "Error", "Could not open video file.")
            return
        
        self.isCameraOn = True  
        self.btnCamera.setText("Stop Video")
        self.camera.running = True
        self.camera.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()    
    sys.exit(app.exec_())