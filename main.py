#создай тут фоторедактор Easy Editor!
from PIL import Image, ImageFilter
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout,
QVBoxLayout, QButtonGroup, QFileDialog, QListWidget)

from PyQt5.QtGui import QPixmap

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle("Easy Editor")

lb_image = QLabel('Картинка')
lw_files = QListWidget()
btn_dir = QPushButton('Папка')

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркально')
btn_sharp = QPushButton('Резкость')
btn_gray = QPushButton('Ч/б')
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton('Сбросить фильтры')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
brr = QHBoxLayout()
col2.addWidget(lb_image)
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
brr.addWidget(btn_left)
brr.addWidget(btn_right)
brr.addWidget(btn_mirror)
brr.addWidget(btn_sharp)
brr.addWidget(btn_gray)
brr.addWidget(btn_save)
brr.addWidget(btn_reset)
col2.addLayout(brr)

row.addLayout(col1,20)
row.addLayout(col2, 80)

win.setLayout(row)

win.show()



workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg','.png','.bmp','.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),
    extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcesseor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Имя папки/"
        self.original_image = None

    def saveImage(self):
        '''сохраняет копию файла в подпапке'''
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height,
        Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path) 

    def do_left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)   

    def do_right(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)   

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)   

    def do_resetImage(self):
        self.image = self.original_image.copy()
        image_path = os.path.join(workdir, self.filename)
        self.showImage(image_path)   

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcesseor()
lw_files.currentRowChanged.connect(showChosenImage)

btn_gray.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_reset.clicked.connect(workimage.do_resetImage)

app.exec()
