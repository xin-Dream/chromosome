import sys

import PyQt5.QtNetwork
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QColorDialog, QAbstractItemView, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QColor
from window import *

import cv2 as cv
import numpy as np


class chromosome(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(chromosome, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("价值百万的软件")

        # default params
        self.total_length = 8000
        self.total_height = 500
        self.img_label = "label"
        self.draw_thickness = 2
        # resize the real shape
        self.narrow_param = 0.1

        self.label_length = 100

        # default background color
        self.longcolor = [211, 215, 207]
        # default line color
        self.drawcolor = [239, 41, 41]

        # a list for line class
        self.line = []

        # set line postion
        self.next_pos.clicked.connect(self.addpos)

        # set default params
        self.image_label.setText(self.img_label)

        # resize image length and height
        self.image_length = int(self.total_length * self.narrow_param)
        self.image_height = int(self.total_height * self.narrow_param)

        # get color
        # line color
        self.color_choose.clicked.connect(self.showColorChoice)
        # background color
        self.color_choose_2.clicked.connect(self.showColorChoice2)
        self.setFocus()

        self.image = np.zeros([self.image_height + 20, self.image_length + self.label_length, 3], np.uint8)
        self.preview.clicked.connect(lambda: self.draw())

        # set callback
        self.background_length.valueChanged.connect(self.change_background_len)
        self.background_height.valueChanged.connect(self.change_background_height)
        self.label_len.valueChanged.connect(self.change_label_len)

        # set table
        self.info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # clear buffer
        self.clear_button.clicked.connect(self.clear_buffer)

    def change_label_len(self):
        self.label_length = self.label_len.value()
        self.image = np.zeros([self.image_height + 20, self.image_length + self.label_length, 3], np.uint8)

    def clear_buffer(self):
        self.line = []
        self.info_table.clearContents()
        self.info_table.setRowCount(0)

    def change_background_len(self):
        self.total_length = self.background_length.value()
        # resize image length and height
        self.image_length = int(self.total_length * self.narrow_param)
        self.image_height = int(self.total_height * self.narrow_param)

    def change_background_height(self):
        self.total_height = self.background_height.value()
        # resize image length and height
        self.image_length = int(self.total_length * self.narrow_param)
        self.image_height = int(self.total_height * self.narrow_param)

    def showColorChoice(self):
        col = QColorDialog.getColor()
        self.drawcolor = self.Hex_to_RGB(col.name())
        print(col.name(), "\n")
        if col.isValid():
            self.color_widget.setStyleSheet('QWidget {background-color:%s}' % col.name())

    def showColorChoice2(self):
        col = QColorDialog.getColor()
        self.longcolor = self.Hex_to_RGB(col.name())
        print(col.name())
        if col.isValid():
            self.color_widget_2.setStyleSheet('QWidget {background-color:%s}' % col.name())

    def addpos(self):
        line = line_info(thickness=self.thickness.value(), label=self.image_label.text(),
                         postion=self.color_pos.value(),
                         R_color=self.drawcolor[0], G_color=self.drawcolor[1], B_color=self.drawcolor[2])
        self.line.append(line)

        # add line info to table
        row = self.info_table.rowCount()
        self.info_table.insertRow(row)
        self.info_table.setItem(row, 0, QTableWidgetItem(str(line.label)))
        self.info_table.setItem(row, 1, QTableWidgetItem(str(line.postion)))
        self.info_table.setItem(row, 2, QTableWidgetItem(str(line.color)))
        self.info_table.setItem(row, 3, QTableWidgetItem(str(line.thickness)))

    def Hex_to_RGB(self, hex):
        r = int(hex[1:3], 16)
        g = int(hex[3:5], 16)
        b = int(hex[5:7], 16)
        # rgb = str(r) + ',' + str(g) + ',' + str(b)

        rgb = [r, g, b]
        print(rgb)
        return rgb

    def draw(self):
        cv.destroyAllWindows()
        self.image.fill(255)

        # 畫背景
        # 注意BGR，注意-1爲實心
        tangle = cv.rectangle(self.image, (self.label_length, 10),
                              (self.image_length + self.label_length, self.image_height + 10),
                              (self.longcolor[2], self.longcolor[1], self.longcolor[0]), -1)

        for i in self.line:
            i.draw(self.image, self.image_height, self.image_label.text(), self.narrow_param, self.label_length)

        cv.imshow("DNA", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows()


class line_info():
    def __init__(self, thickness, label, postion, R_color, G_color, B_color):
        self.thickness = thickness
        self.label = label
        self.postion = postion
        self.R_color = R_color
        self.G_color = G_color
        self.B_color = B_color
        self.color = [self.R_color, self.G_color, self.B_color]

    def draw(self, image, image_height, label, narrow_param, label_length):
        # add label
        cv.putText(image, str(label), (0, image_height), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # draw line
        if self.postion != 0:
            cv.line(image, (int(narrow_param * self.postion + label_length), 10),
                    (int(narrow_param * self.postion + label_length), image_height + 10),
                    (self.B_color, self.G_color, self.R_color), self.thickness,
                    cv.LINE_4)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    appwindow = chromosome()
    appwindow.show()

    sys.exit(app.exec_())
