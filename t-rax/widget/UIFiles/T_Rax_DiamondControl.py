# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_DiamondControl.ui'
#
# Created: Wed Jul  9 08:08:07 2014
# by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_diamond_control_widget(object):
    def setupUi(self, diamond_control_widget):
        diamond_control_widget.setObjectName(_fromUtf8("diamond_control_widget"))
        diamond_control_widget.resize(263, 523)
        diamond_control_widget.setMaximumSize(QtCore.QSize(263, 16777215))
        diamond_control_widget.setStyleSheet(_fromUtf8(""))
        self.verticalLayout_2 = QtGui.QVBoxLayout(diamond_control_widget)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setMargin(12)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(diamond_control_widget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.load_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_exp_data_btn.setMinimumSize(QtCore.QSize(90, 0))
        self.load_exp_data_btn.setFlat(True)
        self.load_exp_data_btn.setObjectName(_fromUtf8("load_exp_data_btn"))
        self.gridLayout.addWidget(self.load_exp_data_btn, 0, 0, 1, 1)
        self.exp_filename_lbl = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp_filename_lbl.sizePolicy().hasHeightForWidth())
        self.exp_filename_lbl.setSizePolicy(sizePolicy)
        self.exp_filename_lbl.setText(_fromUtf8(""))
        self.exp_filename_lbl.setObjectName(_fromUtf8("exp_filename_lbl"))
        self.gridLayout.addWidget(self.exp_filename_lbl, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.load_previous_exp_data_btn = QtGui.QPushButton(self.groupBox)
        self.load_previous_exp_data_btn.setMaximumSize(QtCore.QSize(40, 24))
        self.load_previous_exp_data_btn.setFlat(True)
        self.load_previous_exp_data_btn.setObjectName(_fromUtf8("load_previous_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_previous_exp_data_btn)
        self.load_next_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_next_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_next_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_next_exp_data_btn.setMaximumSize(QtCore.QSize(40, 24))
        self.load_next_exp_data_btn.setFlat(True)
        self.load_next_exp_data_btn.setObjectName(_fromUtf8("load_next_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_next_exp_data_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.auto_process_cb = QtGui.QCheckBox(self.groupBox)
        self.auto_process_cb.setObjectName(_fromUtf8("auto_process_cb"))
        self.gridLayout.addWidget(self.auto_process_cb, 1, 1, 1, 1)
        self.exp_folder_name_lbl = QtGui.QLabel(self.groupBox)
        self.exp_folder_name_lbl.setText(_fromUtf8(""))
        self.exp_folder_name_lbl.setObjectName(_fromUtf8("exp_folder_name_lbl"))
        self.gridLayout.addWidget(self.exp_folder_name_lbl, 2, 0, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.roi_setup_btn = QtGui.QPushButton(diamond_control_widget)
        self.roi_setup_btn.setAutoDefault(False)
        self.roi_setup_btn.setDefault(False)
        self.roi_setup_btn.setFlat(True)
        self.roi_setup_btn.setObjectName(_fromUtf8("roi_setup_btn"))
        self.verticalLayout_2.addWidget(self.roi_setup_btn)
        spacerItem = QtGui.QSpacerItem(20, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.groupBox_2 = QtGui.QGroupBox(diamond_control_widget)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.reference_pos_txt = QtGui.QLineEdit(self.groupBox_2)
        self.reference_pos_txt.setMaximumSize(QtCore.QSize(80, 16777215))
        self.reference_pos_txt.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.reference_pos_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.reference_pos_txt.setObjectName(_fromUtf8("reference_pos_txt"))
        self.horizontalLayout_4.addWidget(self.reference_pos_txt)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setMinimumSize(QtCore.QSize(30, 0))
        self.label_5.setMaximumSize(QtCore.QSize(30, 18))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.measured_pos_lbl = QtGui.QLabel(self.groupBox_2)
        self.measured_pos_lbl.setMinimumSize(QtCore.QSize(0, 18))
        self.measured_pos_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.measured_pos_lbl.setObjectName(_fromUtf8("measured_pos_lbl"))
        self.horizontalLayout_3.addWidget(self.measured_pos_lbl)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setMinimumSize(QtCore.QSize(30, 0))
        self.label_8.setMaximumSize(QtCore.QSize(30, 18))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_3.addWidget(self.label_8)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(7)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pressure_lbl = QtGui.QLabel(self.groupBox_2)
        self.pressure_lbl.setMinimumSize(QtCore.QSize(0, 18))
        self.pressure_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.pressure_lbl.setObjectName(_fromUtf8("pressure_lbl"))
        self.horizontalLayout_5.addWidget(self.pressure_lbl)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.groupBox_4 = QtGui.QGroupBox(diamond_control_widget)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_14 = QtGui.QLabel(self.groupBox_4)
        self.label_14.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_8.addWidget(self.label_14)
        self.laser_line_txt = QtGui.QLineEdit(self.groupBox_4)
        self.laser_line_txt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.laser_line_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.laser_line_txt.setObjectName(_fromUtf8("laser_line_txt"))
        self.horizontalLayout_8.addWidget(self.laser_line_txt)
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_8.addWidget(self.label_15)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.derivative_show_cb = QtGui.QCheckBox(self.groupBox_4)
        self.derivative_show_cb.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.derivative_show_cb.setTristate(False)
        self.derivative_show_cb.setObjectName(_fromUtf8("derivative_show_cb"))
        self.verticalLayout_5.addWidget(self.derivative_show_cb)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_9 = QtGui.QLabel(self.groupBox_4)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_10.addWidget(self.label_9)
        self.derivative_smoothing_sb = QtGui.QSpinBox(self.groupBox_4)
        self.derivative_smoothing_sb.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.derivative_smoothing_sb.setObjectName(_fromUtf8("derivative_smoothing_sb"))
        self.horizontalLayout_10.addWidget(self.derivative_smoothing_sb)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9.addWidget(self.groupBox_4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        spacerItem3 = QtGui.QSpacerItem(20, 49, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)

        self.retranslateUi(diamond_control_widget)
        QtCore.QMetaObject.connectSlotsByName(diamond_control_widget)

    def retranslateUi(self, diamond_control_widget):
        diamond_control_widget.setWindowTitle(_translate("diamond_control_widget", "Form", None))
        self.groupBox.setTitle(_translate("diamond_control_widget", "Experiment", None))
        self.load_exp_data_btn.setText(_translate("diamond_control_widget", "Load Data", None))
        self.load_previous_exp_data_btn.setText(_translate("diamond_control_widget", "<--", None))
        self.load_next_exp_data_btn.setText(_translate("diamond_control_widget", "-->", None))
        self.auto_process_cb.setText(_translate("diamond_control_widget", "autoprocess", None))
        self.roi_setup_btn.setText(_translate("diamond_control_widget", "ROI Setup", None))
        self.groupBox_2.setTitle(_translate("diamond_control_widget", "Pressure", None))
        self.label.setText(_translate("diamond_control_widget", "Reference:", None))
        self.reference_pos_txt.setText(_translate("diamond_control_widget", "1334", None))
        self.label_5.setText(_translate("diamond_control_widget", "cm<sup>-1</sup>", None))
        self.label_2.setText(_translate("diamond_control_widget", "Measured:", None))
        self.measured_pos_lbl.setText(_translate("diamond_control_widget", "1350", None))
        self.label_8.setText(_translate("diamond_control_widget", "cm<sup>-1</sup>", None))
        self.label_3.setText(_translate("diamond_control_widget", "Pressure:", None))
        self.pressure_lbl.setText(_translate("diamond_control_widget", "10", None))
        self.label_6.setText(_translate("diamond_control_widget", "GPa", None))
        self.groupBox_4.setTitle(_translate("diamond_control_widget", "Options", None))
        self.label_14.setText(_translate("diamond_control_widget", "Laser line:", None))
        self.laser_line_txt.setText(_translate("diamond_control_widget", "532", None))
        self.label_15.setText(_translate("diamond_control_widget", "nm", None))
        self.derivative_show_cb.setText(_translate("diamond_control_widget", "show derivative", None))
        self.label_9.setText(_translate("diamond_control_widget", "Smoothing:", None))
