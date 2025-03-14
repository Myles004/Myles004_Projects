from cmath import e
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Mainapp import TriageInputApp

class Ui_LOGINPAGE(object):
    def setupUi(self, LOGINPAGE):
        LOGINPAGE.setObjectName("LOGINPAGE")
        LOGINPAGE.setWindowModality(QtCore.Qt.NonModal)
        LOGINPAGE.resize(801, 579)
       
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Downloads/first-aid-kit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LOGINPAGE.setWindowIcon(icon)
        LOGINPAGE.setAutoFillBackground(False)
        LOGINPAGE.setIconSize(QtCore.QSize(30, 30))
        LOGINPAGE.setDocumentMode(True)
        self.centralwidget = QtWidgets.QWidget(LOGINPAGE)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(390, 130, 391, 361))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMouseTracking(True)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
       
       #username input
        self.username_input = QtWidgets.QLineEdit(self.frame)
        self.username_input.setGeometry(QtCore.QRect(110, 180, 221, 31))
        font = QtGui.QFont()
        font.setFamily("calibri")
        font.setPointSize(9)
        self.username_input.setFont(font)
        self.username_input.setAutoFillBackground(True)
        self.username_input.setObjectName("username_input")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 240, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 180, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        #Password input
        self.password_input = QtWidgets.QLineEdit(self.frame)
        self.password_input.setGeometry(QtCore.QRect(110, 230, 221, 31))
        font = QtGui.QFont()
        font.setFamily("calibri")
        font.setPointSize(9)
        self.password_input.setFont(font)
        self.password_input.setAutoFillBackground(True)
        self.password_input.setObjectName("password_input")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(110, 130, 71, 21))
        font = QtGui.QFont()
        font.setFamily("calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
       
        #Login Button
        self.LoginButton = QtWidgets.QPushButton(self.frame)
        self.LoginButton.setGeometry(QtCore.QRect(220, 310, 75, 23))
        self.LoginButton.setMouseTracking(True)
        self.LoginButton.setCheckable(True)
        self.LoginButton.setObjectName("LoginButton")
        
        #Cancel button
        self.Cance1 = QtWidgets.QPushButton(self.frame)
        self.Cance1.setGeometry(QtCore.QRect(90, 310, 75, 23))
        self.Cance1.setObjectName("Cance1")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(-10, 0, 391, 631))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../../../Downloads/modern-emergency-word-concept-with-flat-design/448196-PFGU1J-617.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(560, 60, 47, 51))
        self.label_5.setText("")
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_4.raise_()
        self.frame.raise_()
        self.label_5.raise_()
        LOGINPAGE.setCentralWidget(self.centralwidget)

        self.retranslateUi(LOGINPAGE)
        QtCore.QMetaObject.connectSlotsByName(LOGINPAGE)

        # Connect the buttons
        self.LoginButton.clicked.connect(self.authenticate_user)
        self.Cance1.clicked.connect(LOGINPAGE.close)

    def authenticate_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        try:
            # Connect to "erdss_db" database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  
                database="erdss_db" 
            )
            cursor = conn.cursor()

            # Checking if user exists in the database
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                self.Triage_window = TriageInputApp()
                self.Triage_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(None, "Database Error", f"Error: {str(e)}")


    def retranslateUi(self, LOGINPAGE):
        _translate = QtCore.QCoreApplication.translate
        LOGINPAGE.setWindowTitle(_translate("LOGINPAGE", "ERDSS"))
        self.label_3.setText(_translate("LOGINPAGE", "Password"))
        self.label_2.setText(_translate("LOGINPAGE", "UserName"))
        self.label.setText(_translate("LOGINPAGE", "LOGIN"))
        self.LoginButton.setText(_translate("LOGINPAGE", "Login"))
        self.Cance1.setText(_translate("LOGINPAGE", "Cancel"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LOGINPAGE = QtWidgets.QMainWindow()
    ui = Ui_LOGINPAGE()
    ui.setupUi(LOGINPAGE)
    LOGINPAGE.show()
    sys.exit(app.exec_())
