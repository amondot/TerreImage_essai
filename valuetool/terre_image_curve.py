# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGIS_Edu
                                 A QGIS plugin
 Segmentation using OTB application
                              -------------------
        begin                : 2014-05-06
        copyright            : (C) 2014 by CNES
        email                : alexia.mondot@c-s.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 """

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QColor, QWidget, QPixmap, QIcon, QInputDialog

from ui_terre_image_curve import Ui_Form

import random

#import loggin for debug messages
import logging
logging.basicConfig()
# create logger
logger = logging.getLogger( 'TerreImage_Curve' )
logger.setLevel(logging.INFO)


class TerreImageCurve(QWidget, Ui_Form):

    __pyqtSignals__ = ("curveTitleChanged(str)", "hideCurve(int)", "colorChanged()", "deleteCurve()")

    def __init__(self, name, x, y, points, abs = None, color = None):
        QWidget.__init__(self)
        self.setupUi(self)

        self.name = name
        self.lineEdit_curve_name.setText(name)

        logger.debug("from curve: " + str(x) + " " + str(y))
        self.coordinates = "[x=" + str(x) + ", y=" + str(y) + "]"
        self.label_coordinates.setText(self.coordinates)

        self.lettersToQColor = {"bleu": QColor(0, 132, 255), "vert": QColor(148, 255, 69),
                                "rouge": QColor(255, 30, 0), "cyan": QColor(0, 255, 204),
                                "magenta": QColor(255, 0, 255), "jaune": QColor(255, 255, 0),
                                "noir": QColor(0, 0, 0)}

        self.frenchToLetter = {"bleu": 'b', "vert": 'g',
                               "rouge": 'r', "cyan": 'c',
                               "magenta": 'm', "jaune": 'y',
                               "noir": 'k'}

        self.lettersToNameColor = {"b": "blue", "g": "green", "r": "red",
                                   "c": "cyan", "m": "magenta",
                                   "y": "yellow", "k": "black"}

        self.nameColorsToLetters = dict((v, k) for k, v in self.lettersToNameColor.iteritems())

        if color is None:
            colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
            logger.debug("len(colors): " + str(len(colors)))
            color = colors[ random.randint(0, len(colors) - 1) ]
            logger.debug('color from creation courbe: ' + str(color))
        self.color = color

        if abs:
            self.abs = abs
        else:
            self.abs = None

        pixmap = QPixmap(self.pushButton_color.size())
        pixmap.fill(QColor(self.lettersToNameColor[self.color]))
        icon = QIcon(pixmap)
        self.pushButton_color.setIcon(icon)

        self.points = points

        # self.connect(self.lineEdit_curve_name, SIGNAL("textChanged(str)"), self, SIGNAL("curveTitleChanged(str)"))
        self.connect(self.lineEdit_curve_name, SIGNAL("editingFinished()"), self.set_name)
        self.connect(self.pushButton_color, SIGNAL("clicked()"), self.set_color)
        self.connect(self.pushButton_delete_curve, SIGNAL("clicked()"), self, SIGNAL("deleteCurve()"))

    def display_points(self):
        return self.checkBox_curve_visible.checkState() == Qt.Checked

    def set_color(self):
        # couleur = QtGui.QColorDialog.getColor(QtCore.Qt.white)

        testqt, ok = QInputDialog.getItem(None, "Couleur", "Selection d'une couleur", self.lettersToQColor.keys(), False)
        if ok:
            # couleur = self.nameColorsToLetters[testqt]
            couleur = self.lettersToQColor[testqt]
            logger.debug(couleur)
            self.color = self.frenchToLetter[testqt]
        else:
            couleur = self.lettersToQColor['noir']
            self.color = 'b'

        # self.color = str(couleur.name())
        # logger.debug( couleur.name())

        # self.color = self.lettersToNameColor[testqt]

        pixmap = QPixmap(self.pushButton_color.size())
        # pixmap.fill(QColor(self.color))
        pixmap.fill(couleur)
        icon = QIcon(pixmap)
        self.pushButton_color.setIcon(icon)
        # logger.debug(  QColor(self.color) )

        # self.pushButton_color.setStyleSheet("background-color: " + self.color )

        # palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.ButtonText, self.lettersToQColor[testqt])
        # palette.setColor(10, couleur)
        # self.pushButton_color.setPalette(palette)
        self.emit(SIGNAL("colorChanged"))

    def set_name(self, text = None):
        self.name = self.lineEdit_curve_name.text()

    def __str__(self):
        return self.name + " " + str(self.coordinates) + " " + str(self.color) + " " + str(self.points)

    def has_abs(self):
        return self.abs is not None
