
"""
Author: yuxiwang
Date: [1023-12-27]
use easyocr,orc
"""
from PIL import Image, ImageTk
import sys
from PyQt6.QtWidgets import QApplication, QDialog, QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PyQt6.QtGui import QPixmap,QColor
from PyQt6.QtCore import Qt,QTimer
from untitled import Ui_Form
import cv2
from PyQt6.QtGui import QImage
import easyocr
import torch
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import numpy as np
import time



# Define a main function, inherit Ui_Form and QDialog
class main(Ui_Form, QDialog):
    # Initialization function
    def __init__(self):
        # Call the initialization function of the parent class
        super(main, self).__init__()
        # Call the setupUi function, passing in self
        self.setupUi(self)
        # Display the window
        #self.show()
        self.min = 0
        self.sec = 0
        self.secondSec = 0
        self.linetext = str(0) + str(self.min) + ':' + str(0) + str(self.sec) + ':' + str(0) + str(self.secondSec)
        self.lcdNumber.display(self.linetext)  # Display the number



        self.timer = QTimer()
        self.timer.setInterval(2)
        self.timer.timeout.connect(self.onTimerOut)

        # Connect the button click event to the corresponding slot function
        self.pushButton.clicked.connect(self.open_image2)
        self.pushButton_2.clicked.connect(self.easyorc)



        #self.pushButton_2.clicked.connect(self.start)
        # self.pushButton_3.clicked.connect(self.stop)
        #
        # self.count = 1
    #
    # def start(self):
    #     self.reset()
    #     self.timer.start()
    #     self.textEdit.append('计次' + str(self.count) + '      ' + self.linetext)
    #     self.count += 1
    #
    #
    # def stop(self):
    #     self.timer.stop()


    def reset(self):
        self.timer.stop()
        self.sec = 0
        self.min = 0
        self.lcdNumber.display(str(0) + str(0) + ':' + str(0) + str(0) + ':' + str(0) + str(0))
        self.textEdit.clear()
        self.count = 1

    # def exit(self):
    #         sys.exit(app.exec())

    #the function is not working when file path contains Chinese characters
    def open_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Image', '',
                                                   'Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif)')

        if file_path:
            self.img = cv2.imread(file_path)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            height, width, channel = self.img.shape
            bytes_per_line = 3 * width
            q_img = QPixmap.fromImage(QImage(self.img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888))
            # Create a QGraphicsScene object
            scene = QGraphicsScene()
            # Create a QGraphicsPixmapItem object and pass q_img as a parameter
            item = QGraphicsPixmapItem(q_img)
            # Add item to the scene
            scene.addItem(item)
            # Set the scene to graphicsView_2
            self.graphicsView_2.setScene(scene)
            # Set the aspect ratio of graphicsView_2 to KeepAspectRatio
            self.graphicsView_2.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)


#######################################################################
    #the function can work when the file path contains the chinese character
    def open_image2(self):

        file_dialog = QFileDialog()

        file_path, _ = file_dialog.getOpenFileName(self, 'Open Image', '',
                                                   'Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif)')
        if file_path:
            # Read the image using the PIL library
            self.img = Image.open(file_path)
            # Convert the image to OpenCV format (if needed)
            self.img = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            height, width, channel = self.img.shape
            bytes_per_line = 3 * width
            q_img = QPixmap.fromImage(QImage(self.img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888))
            # Create a QGraphicsScene object
            scene = QGraphicsScene()
            # Create a QGraphicsPixmapItem object and pass q_img as a parameter
            item = QGraphicsPixmapItem(q_img)
            # Add item to the scene
            scene.addItem(item)
            # Set the scene to graphicsView_2
            self.graphicsView_2.setScene(scene)
            # Set the aspect ratio of graphicsView_2 to KeepAspectRatio
            self.graphicsView_2.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)

    def easyorc(self):
        # self.start()
        time_start=time.time()
        print(torch.__version__)  # Print the current PyTorch version number
        print(torch.version.cuda)  # Print the current CUDA version number
        print(torch.backends.cudnn.version())  # Print the current cuDNN version number
        print(torch.cuda.get_device_name(0))  # Print the name of the first GPU device
        # Create a reader object
        modelPath = os.getcwd() + "/model"
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=True, model_storage_directory=modelPath)
        result = reader.readtext(self.img)
        print(result)
        print(len(result))

        text_out= ""
        # Draw bounding boxes and text on the image
        for i,detection in enumerate(result):
            print(i)
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            print('top_left',top_left)
            print("bottom_right",bottom_right)
            text = detection[1]
            self.img = cv2.rectangle(self.img, top_left, bottom_right, (0, 0, 255), 2)
            self.progressBar.setValue(int((i+1)/len(result)*100))
            # self.lcdNumber.display(i+1)  # Display the number
            # self.lcdNumber.setDigitCount(10)  # Set the number of digits
            text_out+=text
            print(text)
        image = self.img
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        q_img = QPixmap.fromImage(QImage(image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888))
        # Create a QGraphicsScene object
        scene = QGraphicsScene()
        # Create a QGraphicsPixmapItem object and pass q_img as a parameter
        item = QGraphicsPixmapItem(q_img)
        # Add item to the scene
        scene.addItem(item)
        # Set the scene to graphicsView_2
        self.graphicsView.setScene(scene)
        # Set the aspect ratio of graphicsView_2 to KeepAspectRatio
        self.graphicsView.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)

        print(text_out)
        # Draw a red box around the recognized text
        self.textEdit.setPlainText(text_out)

        print("step001")
        print("time",time.time()-time_start)

        # self.stop()
        # self.textEdit.append('计次' + str(self.count) + '      ' + self.linetext)


    def onTimerOut(self):
        self.secondSec+=1
        if self.secondSec!=100:
            if self.secondSec<10 and self.sec<10 :
                self.linetext=str(0) + str(self.min) + ':' + str(0) + str(self.sec) + ':' + str(0) + str(self.secondSec)
                self.lcdNumber.display(self.linetext)
            elif self.secondSec>=10 and self.sec<10 :
                self.linetext=str(0) + str(self.min) + ':'+str(0) + str(self.sec) + ':' + str(self.secondSec)
                self.lcdNumber.display(self.linetext)
            elif self.secondSec <10 and self.sec >=10:
                self.linetext=str(0) + str(self.min) + ':'+str(self.sec) + ':' + str(0)+str(self.secondSec)
                self.lcdNumber.display(self.linetext)
            elif self.secondSec >= 10 and self.sec >=10:
                self.linetext=str(0) + str(self.min) + ':' +str(self.sec) + ':' + str(self.secondSec)
                self.lcdNumber.display(self.linetext)

        if self.secondSec==100:
            self.secondSec=0
            self.sec+=1

        if self.sec==60:
            self.sec=0
            self.min+=1




# Define a main function, call QApplication, main function, myHellWorld, sys.exit, app.exec
if __name__ == '__main__':
    # Create a QApplication object
    app = QApplication(sys.argv)
    # Create a main function
    MainWindow = main()
    MainWindow.show()
    sys.exit(app.exec())