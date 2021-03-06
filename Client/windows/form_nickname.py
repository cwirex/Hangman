from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_formNickname(object):
    """
    Window class for entering a nickname
    """

    def __init__(self, windows=None):
        """
        Initialize object

        :param windows: Windows (parent)
        """
        self.windows = windows

    def bind(self):
        """
        Bind function to window

        """
        self.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        """
        Read nickname and serve it. If nickname is in database fetch details of an account

        """
        nick = self.lineEdit.text()
        if nick:
            if self.windows.game.playerExists(nick):
                self.windows.game.playerLogin(nick)
                self.windows.show_mainWindow()
            else:
                self.windows.formPlayer.set_player_name(nick)
                self.windows.show_formPlayer()
            self.lineEdit.setText("")

    def setupUi(self, formNickname):
        """
        Setup the UI

        :param formNickname: formNickname
        """
        formNickname.setObjectName("QformNickname")
        formNickname.resize(401, 230)
        self.lineEdit = QtWidgets.QLineEdit(formNickname)
        self.lineEdit.setGeometry(QtCore.QRect(60, 90, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(32)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(formNickname)
        self.pushButton.setGeometry(QtCore.QRect(120, 170, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(formNickname)
        self.label.setGeometry(QtCore.QRect(0, 20, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(formNickname)
        QtCore.QMetaObject.connectSlotsByName(formNickname)

    def retranslateUi(self, formNickname):
        """
        Retranslate the UI

        :param formNickname: formNickname
        """
        _translate = QtCore.QCoreApplication.translate
        formNickname.setWindowTitle(_translate("QformNickname", "Form"))
        self.lineEdit.setPlaceholderText(_translate("QformNickname", "Enter new or existing name"))
        self.pushButton.setText(_translate("QformNickname", "Confirm"))
        self.label.setText(_translate("QformNickname", "Choose your nickname"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    formNickname = QtWidgets.QWidget()
    ui = Ui_formNickname()
    ui.setupUi(formNickname)
    formNickname.show()
    sys.exit(app.exec_())
