# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(593, 253)
        self.verticalLayout_2 = QVBoxLayout(ConfigureDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(ConfigureDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.renderArgsLineEdit = QLineEdit(self.groupBox)
        self.renderArgsLineEdit.setObjectName(u"renderArgsLineEdit")

        self.gridLayout.addWidget(self.renderArgsLineEdit, 3, 1, 1, 1)

        self.renderArgsLabel = QLabel(self.groupBox)
        self.renderArgsLabel.setObjectName(u"renderArgsLabel")

        self.gridLayout.addWidget(self.renderArgsLabel, 3, 0, 1, 1)

        self.identifierLineEdit = QLineEdit(self.groupBox)
        self.identifierLineEdit.setObjectName(u"identifierLineEdit")

        self.gridLayout.addWidget(self.identifierLineEdit, 0, 1, 1, 1)

        self.discretisationLabel = QLabel(self.groupBox)
        self.discretisationLabel.setObjectName(u"discretisationLabel")
        self.discretisationLabel.setMinimumSize(QSize(71, 0))

        self.gridLayout.addWidget(self.discretisationLabel, 1, 0, 1, 1)

        self.displayNodeLabel = QLabel(self.groupBox)
        self.displayNodeLabel.setObjectName(u"displayNodeLabel")
        self.displayNodeLabel.setMinimumSize(QSize(71, 0))

        self.gridLayout.addWidget(self.displayNodeLabel, 2, 0, 1, 1)

        self.identifierLabel = QLabel(self.groupBox)
        self.identifierLabel.setObjectName(u"identifierLabel")

        self.gridLayout.addWidget(self.identifierLabel, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.displayNodesCheckBox = QCheckBox(self.groupBox)
        self.displayNodesCheckBox.setObjectName(u"displayNodesCheckBox")

        self.gridLayout.addWidget(self.displayNodesCheckBox, 2, 1, 1, 1)

        self.discretisationLineEdit = QLineEdit(self.groupBox)
        self.discretisationLineEdit.setObjectName(u"discretisationLineEdit")

        self.gridLayout.addWidget(self.discretisationLineEdit, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.identifierLabel.setBuddy(self.identifierLineEdit)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure - Mayavi Model Viewer", None))
        self.groupBox.setTitle("")
        self.renderArgsLineEdit.setText(QCoreApplication.translate("ConfigureDialog", u"{'color':'bone'}", None))
        self.renderArgsLabel.setText(QCoreApplication.translate("ConfigureDialog", u"Render Args:", None))
#if QT_CONFIG(tooltip)
        self.discretisationLabel.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.discretisationLabel.setText(QCoreApplication.translate("ConfigureDialog", u"Discretisation:", None))
        self.displayNodeLabel.setText(QCoreApplication.translate("ConfigureDialog", u"Display Nodes:", None))
        self.identifierLabel.setText(QCoreApplication.translate("ConfigureDialog", u"Identifier:", None))
        self.displayNodesCheckBox.setText("")
        self.discretisationLineEdit.setText(QCoreApplication.translate("ConfigureDialog", u"5x5", None))
    # retranslateUi

