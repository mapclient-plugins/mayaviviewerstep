# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mayaviviewerwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mayaviscenewidget import MayaviSceneWidget


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(914, 548)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widgetMain = QWidget(Dialog)
        self.widgetMain.setObjectName(u"widgetMain")
        self.widgetMain.setEnabled(True)
        sizePolicy.setHeightForWidth(self.widgetMain.sizePolicy().hasHeightForWidth())
        self.widgetMain.setSizePolicy(sizePolicy)
        self.widgetMain.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.widgetMain)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(self.widgetMain)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.tableWidget = QTableWidget(self.widget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)

        self.verticalLayout.addWidget(self.tableWidget)

        self.sliceplanegroup = QGroupBox(self.widget)
        self.sliceplanegroup.setObjectName(u"sliceplanegroup")
        self.sliceplanegroup.setEnabled(False)
        self.horizontalLayout = QHBoxLayout(self.sliceplanegroup)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.slicePlaneRadioX = QRadioButton(self.sliceplanegroup)
        self.slicePlaneRadioX.setObjectName(u"slicePlaneRadioX")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.slicePlaneRadioX.sizePolicy().hasHeightForWidth())
        self.slicePlaneRadioX.setSizePolicy(sizePolicy2)
        self.slicePlaneRadioX.setChecked(False)

        self.horizontalLayout.addWidget(self.slicePlaneRadioX)

        self.slicePlaneRadioY = QRadioButton(self.sliceplanegroup)
        self.slicePlaneRadioY.setObjectName(u"slicePlaneRadioY")
        sizePolicy2.setHeightForWidth(self.slicePlaneRadioY.sizePolicy().hasHeightForWidth())
        self.slicePlaneRadioY.setSizePolicy(sizePolicy2)
        self.slicePlaneRadioY.setChecked(True)

        self.horizontalLayout.addWidget(self.slicePlaneRadioY)

        self.slicePlaneRadioZ = QRadioButton(self.sliceplanegroup)
        self.slicePlaneRadioZ.setObjectName(u"slicePlaneRadioZ")
        sizePolicy2.setHeightForWidth(self.slicePlaneRadioZ.sizePolicy().hasHeightForWidth())
        self.slicePlaneRadioZ.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.slicePlaneRadioZ)


        self.verticalLayout.addWidget(self.sliceplanegroup)

        self.screenshotgroup = QGroupBox(self.widget)
        self.screenshotgroup.setObjectName(u"screenshotgroup")
        self.screenshotgroup.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout = QFormLayout(self.screenshotgroup)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.pixelsXLabel = QLabel(self.screenshotgroup)
        self.pixelsXLabel.setObjectName(u"pixelsXLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pixelsXLabel.sizePolicy().hasHeightForWidth())
        self.pixelsXLabel.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.pixelsXLabel)

        self.screenshotPixelXLineEdit = QLineEdit(self.screenshotgroup)
        self.screenshotPixelXLineEdit.setObjectName(u"screenshotPixelXLineEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.screenshotPixelXLineEdit.sizePolicy().hasHeightForWidth())
        self.screenshotPixelXLineEdit.setSizePolicy(sizePolicy4)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.screenshotPixelXLineEdit)

        self.pixelsYLabel = QLabel(self.screenshotgroup)
        self.pixelsYLabel.setObjectName(u"pixelsYLabel")
        sizePolicy3.setHeightForWidth(self.pixelsYLabel.sizePolicy().hasHeightForWidth())
        self.pixelsYLabel.setSizePolicy(sizePolicy3)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.pixelsYLabel)

        self.screenshotPixelYLineEdit = QLineEdit(self.screenshotgroup)
        self.screenshotPixelYLineEdit.setObjectName(u"screenshotPixelYLineEdit")
        sizePolicy4.setHeightForWidth(self.screenshotPixelYLineEdit.sizePolicy().hasHeightForWidth())
        self.screenshotPixelYLineEdit.setSizePolicy(sizePolicy4)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.screenshotPixelYLineEdit)

        self.screenshotFilenameLabel = QLabel(self.screenshotgroup)
        self.screenshotFilenameLabel.setObjectName(u"screenshotFilenameLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.screenshotFilenameLabel)

        self.screenshotFilenameLineEdit = QLineEdit(self.screenshotgroup)
        self.screenshotFilenameLineEdit.setObjectName(u"screenshotFilenameLineEdit")
        sizePolicy4.setHeightForWidth(self.screenshotFilenameLineEdit.sizePolicy().hasHeightForWidth())
        self.screenshotFilenameLineEdit.setSizePolicy(sizePolicy4)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.screenshotFilenameLineEdit)

        self.screenshotSaveButton = QPushButton(self.screenshotgroup)
        self.screenshotSaveButton.setObjectName(u"screenshotSaveButton")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.screenshotSaveButton.sizePolicy().hasHeightForWidth())
        self.screenshotSaveButton.setSizePolicy(sizePolicy5)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.screenshotSaveButton)


        self.verticalLayout.addWidget(self.screenshotgroup)

        self.closeButton = QPushButton(self.widget)
        self.closeButton.setObjectName(u"closeButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy6)
        self.closeButton.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.MayaviScene = MayaviSceneWidget(self.widgetMain)
        self.MayaviScene.setObjectName(u"MayaviScene")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.MayaviScene.sizePolicy().hasHeightForWidth())
        self.MayaviScene.setSizePolicy(sizePolicy7)

        self.gridLayout.addWidget(self.MayaviScene, 0, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.widgetMain)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Model Viewer", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Visible", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Type", None));
        self.sliceplanegroup.setTitle(QCoreApplication.translate("Dialog", u"Image Slice Plane", None))
        self.slicePlaneRadioX.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.slicePlaneRadioY.setText(QCoreApplication.translate("Dialog", u"Y", None))
        self.slicePlaneRadioZ.setText(QCoreApplication.translate("Dialog", u"Z", None))
        self.screenshotgroup.setTitle(QCoreApplication.translate("Dialog", u"Screenshot", None))
        self.pixelsXLabel.setText(QCoreApplication.translate("Dialog", u"Pixels X:", None))
        self.screenshotPixelXLineEdit.setText(QCoreApplication.translate("Dialog", u"800", None))
        self.pixelsYLabel.setText(QCoreApplication.translate("Dialog", u"Pixels Y:", None))
        self.screenshotPixelYLineEdit.setText(QCoreApplication.translate("Dialog", u"600", None))
        self.screenshotFilenameLabel.setText(QCoreApplication.translate("Dialog", u"Filename:", None))
        self.screenshotFilenameLineEdit.setText(QCoreApplication.translate("Dialog", u"screenshot.png", None))
        self.screenshotSaveButton.setText(QCoreApplication.translate("Dialog", u"Save Screenshot", None))
        self.closeButton.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi

