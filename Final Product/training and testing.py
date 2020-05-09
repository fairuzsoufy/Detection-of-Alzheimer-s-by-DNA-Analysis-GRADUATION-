import _pickle
import hashlib
import numpy as np
import threading
import firebase_admin
import pandas as pd
import sklearn
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QDir
from firebase_admin import credentials, firestore
from joblib import load, dump
from sklearn import svm, preprocessing
from sklearn.model_selection import GridSearchCV

global firstname
global lastname
global username
global password
global type
global found
global filename

cred = credentials.Certificate(r"E:\Users\user\PycharmProjects\untitled1\venv\alzheimer-4a38b-firebase-adminsdk-e29rr-2e0781f010.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 500)
        MainWindow.setObjectName("main_window")
        regex = QtCore.QRegExp("[a-z-A-Z_]+")
        validator = QtGui.QRegExpValidator(regex)
        with open ("design.qss","r")as f:
            stylesheet=f.read()
        MainWindow.setStyleSheet(stylesheet)
        MainWindow.setWindowIcon(QIcon(r"E:\Users\user\PycharmProjects\untitled1\venv\Dna-icon.png"))
        # MainWindow.setStyleSheet("background: '#042c4d'")

   ########################## Home #################################
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.welcomelabel = QtWidgets.QLabel(self.centralwidget)
        self.welcomelabel.setGeometry(QtCore.QRect(130, -70, 350, 270))
        self.welcomelabel.setAutoFillBackground(False)
        self.welcomelabel.setObjectName("welcomelabel")
        self.welcomelabel.setStyleSheet("color: 'white'; font:13pt Arial Rounded MT Bold")
        l2 = QtWidgets.QLabel(self.centralwidget)
        l2.setPixmap(QtGui.QPixmap(r"E:\Users\user\PycharmProjects\untitled1\venv\1.png"))
        l2.setGeometry(0,0,400,400)
        l2.move(30,80)
        self.loginbutton = QtWidgets.QPushButton(self.centralwidget)
        self.loginbutton.setGeometry(QtCore.QRect(360, 210, 93, 28))
        self.loginbutton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.loginbutton.setObjectName("loginbutton")
        # self.loginbutton.setStyleSheet("color: #0d4f91;font:15px;border-radius: 7px;background-color: 'white'")
        self.loginbutton.setStyleSheet(stylesheet)
        self.registerbutton = QtWidgets.QPushButton(self.centralwidget)
        self.registerbutton.setGeometry(QtCore.QRect(360, 280, 93, 28))
        self.registerbutton.setObjectName("registerbutton")
        self.registerbutton.setStyleSheet(stylesheet)
        self.firsttimelabel = QtWidgets.QLabel(self.centralwidget)
        self.firsttimelabel.setGeometry(QtCore.QRect(360, 255, 101, 16))
        self.firsttimelabel.setObjectName("firsttimelabel")
        self.firsttimelabel.setStyleSheet("color: 'white'; font: 10pt Arial Rounded MT Bold")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.loginbutton.clicked.connect(self.Loginclick)
        self.registerbutton.clicked.connect(self.Registerclick)


        #################### Login ####################


        self.QLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.QLineEdit.setGeometry(QtCore.QRect(360, 190, 151, 31))
        self.QLineEdit.setObjectName("textEdit")
        self.QLineEdit.setStyleSheet(stylesheet)
        self.QLineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.QLineEdit_2.setGeometry(QtCore.QRect(360, 240, 151, 31))
        self.QLineEdit_2.setObjectName("textEdit_2")
        self.QLineEdit_2.setEchoMode(QLineEdit.Password)
        self.QLineEdit_2.setStyleSheet(stylesheet)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(275, 195, 80, 20))
        self.label.setStyleSheet(stylesheet)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(275, 245, 80, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(stylesheet)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(250, 50, 111, 30))
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: 'white'; font:13pt Arial Rounded MT Bold")
        self.loginbutton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.loginbutton_2.setGeometry(QtCore.QRect(380, 290, 93, 28))
        self.loginbutton_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.loginbutton_2.setObjectName("loginbutton_2")
        self.loginbutton_2.setStyleSheet(stylesheet)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 542, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.loginbutton_2.clicked.connect(self.loginonclick)


        ##################### Register ###########################


        self.label7 = QtWidgets.QLabel(self.centralwidget)
        self.label7.setGeometry(QtCore.QRect(270, 225, 81, 20))
        self.label7.setObjectName("label7")
        self.label7.setStyleSheet(stylesheet)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(270, 275, 75, 16))
        self.label_8.setObjectName("label_8")
        self.label_8.setStyleSheet(stylesheet)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(370, 50, 111, 25))
        self.label_9.setObjectName("label_9")
        self.label_9.setStyleSheet("color: 'white'; font:13pt Arial Rounded MT Bold")
        self.loginbutton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.loginbutton_3.setGeometry(QtCore.QRect(370, 390, 93, 28))
        self.loginbutton_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.loginbutton_3.setObjectName("loginbutton_3")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(270, 175, 71, 20))
        self.label_10.setObjectName("label_10")
        self.label_10.setStyleSheet(stylesheet)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(270, 125, 71, 20))
        self.label_11.setObjectName("label_11")
        self.label_11.setStyleSheet(stylesheet)
        self.admin_radiobutton = QtWidgets.QRadioButton(self.centralwidget)
        self.admin_radiobutton.setGeometry(QtCore.QRect(370, 320, 105, 20))
        self.admin_radiobutton.setObjectName("radioButton")
        self.admin_radiobutton.setStyleSheet(stylesheet)
        self.researcher_radiobutton = QtWidgets.QRadioButton(self.centralwidget)
        self.researcher_radiobutton.setGeometry(QtCore.QRect(370, 350, 105, 20))
        self.researcher_radiobutton.setObjectName("radioButton_2")
        self.researcher_radiobutton.setStyleSheet(stylesheet)

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(300, 335, 41, 26))
        self.label_12.setObjectName("label_12")
        self.label_12.setStyleSheet(stylesheet)
        self.firstname_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.firstname_txt.setGeometry(QtCore.QRect(350, 120, 151, 31))
        self.firstname_txt.setObjectName("firstname_txt")
        self.firstname_txt.setValidator(validator)
        self.firstname_txt.setMaxLength(8)
        self.firstname_txt.setFocus(True)
        self.firstname_txt.minimumSizeHint()
        self.firstname_txt.setStyleSheet(stylesheet)
        self.lastname_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.lastname_txt.setGeometry(QtCore.QRect(350, 170, 151, 31))
        self.lastname_txt.setObjectName("lastname_txt")
        self.lastname_txt.setValidator(validator)
        self.lastname_txt.setMaxLength(8)
        self.lastname_txt.setStyleSheet(stylesheet)
        self.username_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.username_txt.setGeometry(QtCore.QRect(350, 220, 151, 31))
        self.username_txt.setObjectName("username_txt")
        self.username_txt.setMaxLength(10)
        self.username_txt.setStyleSheet(stylesheet)
        self.password_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.password_txt.setGeometry(QtCore.QRect(350, 270, 151, 31))
        self.password_txt.setObjectName("password_txt")
        self.password_txt.setEchoMode(QLineEdit.Password)
        self.password_txt.setMaxLength(15)
        self.password_txt.setStyleSheet(stylesheet)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 542, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.loginbutton_3.clicked.connect(self.registeronclick)

        ############# back arrow ##########################3
        self.back_arrow=QtWidgets.QLabel(self.centralwidget)
        self.back_arrow.move(30, 0)
        self.back_arrow.setObjectName("back_arrow")
        self.back_arrow.setStyleSheet("font-size: 35px")
        self.back_arrow.setTextFormat(Qt.RichText)
        self.back_arrow.setText("&#8592;")
        self.back_arrow.setStyleSheet("color: 'white'; font:55px")
        self.back_arrow.mousePressEvent=self.back_pressed

        ############## researcher page ############################

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(220, 200, 93, 28))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setStyleSheet(stylesheet)
        self.Researcher_label = QtWidgets.QLabel(self.centralwidget)
        self.Researcher_label.setGeometry(QtCore.QRect(230, 50, 111, 36))
        self.Researcher_label.setObjectName("Researcher_label")
        self.Researcher_label.setStyleSheet("color: 'white'; font:14pt Arial Rounded MT Bold")

        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(300, 400, 111, 36))
        self.result_label.setObjectName("result_label")
        self.result_label.setStyleSheet("color: 'white'; font:14pt Arial Rounded MT Bold")

        self.classify_result = QtWidgets.QLabel(self.centralwidget)
        self.classify_result.setGeometry(QtCore.QRect(400, 400, 111, 36))
        self.classify_result.setObjectName("classify_result")
        self.classify_result.setStyleSheet("color: 'white'; font:14pt Arial Rounded MT Bold")

        self.label13 = QtWidgets.QLabel(self.centralwidget)
        self.label13.setGeometry(QtCore.QRect(210, 140, 241, 31))
        self.label13.setObjectName("label")
        self.label13.setStyleSheet(stylesheet)
        self.pushButton1.clicked.connect(self.researcher_upload)

######################### ADMIN PAGE #####################################
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(220, 200, 93, 28))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.setStyleSheet(stylesheet)
        self.admin_label = QtWidgets.QLabel(self.centralwidget)
        self.admin_label.setGeometry(QtCore.QRect(250, 50, 111, 36))
        self.admin_label.setObjectName("Admin_label")
        self.admin_label.setStyleSheet("color: 'white'; font:14pt Arial Rounded MT Bold")
        self.label14 = QtWidgets.QLabel(self.centralwidget)
        self.label14.setGeometry(QtCore.QRect(200, 140, 241, 31))
        self.label14.setObjectName("label")
        self.label14.setStyleSheet(stylesheet)
        self.pushButton2.clicked.connect(self.admin_upload)

        self.result_label2 = QtWidgets.QLabel(self.centralwidget)
        self.result_label2.setGeometry(QtCore.QRect(300, 400, 111, 36))
        self.result_label2.setObjectName("result_label2")
        self.result_label2.setStyleSheet("color: 'white'; font:14pt Arial Rounded MT Bold")

        self.train_result = QtWidgets.QLabel(self.centralwidget)
        self.train_result.setGeometry(QtCore.QRect(400, 400, 111, 36))
        self.train_result.setObjectName("train_result")
        self.train_result.setStyleSheet("color: 'white'; font:14pt Arial Rounded MT Bold")


        self.retranslateUi(MainWindow)


        self.hide_login()
        self.hide_register()
        self.hide_researcher_upload()

        self.hide_admin_upload()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alzheimer's Analysis System"))
        self.welcomelabel.setText(_translate("MainWindow", "Alzheimer's Analysis System"))
        self.loginbutton.setText(_translate("MainWindow", "Login"))
        self.registerbutton.setText(_translate("MainWindow", "Register"))
        self.firsttimelabel.setText(_translate("MainWindow", "First Time ?"))
        self.label.setText(_translate("Login", "Username"))
        self.label_2.setText(_translate("Login", "Password"))
        self.label_3.setText(_translate("Login", "Login"))
        self.loginbutton_2.setText(_translate("Login", "Login"))
        self.label7.setText(_translate("Register", "Username"))
        self.label_8.setText(_translate("Register", "Password"))
        self.label_9.setText(_translate("Register", "Welcome "))
        self.loginbutton_3.setText(_translate("Register", "Register"))
        self.label_10.setText(_translate("Register", "Last Name"))
        self.label_11.setText(_translate("Register", "First Name"))
        self.admin_radiobutton.setText(_translate("Register", "Admin"))
        self.researcher_radiobutton.setText(_translate("Register", "Researcher"))
        self.label_12.setText(_translate("Register", "Type"))
        self.pushButton1.setText(_translate("Researcher", "Choose"))
        self.Researcher_label.setText(_translate("Researcher", "Researcher"))
        self.result_label.setText(_translate("Researcher", "Result:"))
        self.classify_result.setText(_translate("Researcher", " "))
        self.label13.setText(_translate("Researcher", "Please select the file"))

        self.pushButton2.setText(_translate("Admin", "Choose"))
        self.admin_label.setText(_translate("Admin", "Admin"))
        self.result_label2.setText(_translate("Admin", "Result:"))
        self.train_result.setText(_translate("Admin", " "))
        self.label14.setText(_translate("Admin", "Please select the dataset file"))

    def admin_upload(self):


        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', r"C:\Users\user\Desktop", '*.csv')

        print(filename)
        self.train(filename)

    def researcher_upload(self):

        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', r"C:\Users\user\Desktop", '*.csv')

        print(filename)

        self.classify(filename)

    def back_pressed(self,event):
        self.hide_register()
        self.hide_login()
        self.hide_researcher_upload()
        self.hide_admin_upload()
        self.show_home()

    def show_home(self):
        self.centralwidget.show()
        self.welcomelabel.show()
        self.loginbutton.show()
        self.registerbutton.show()
        self.firsttimelabel.show()
        self.menubar.show()
        self.menubar.show()
        self.statusbar.show()

    def hide_home(self):
        self.centralwidget.hide()
        self.welcomelabel.hide()
        self.loginbutton.hide()
        self.registerbutton.hide()
        self.firsttimelabel.hide()
        self.menubar.hide()
        self.menubar.hide()
        self.statusbar.hide()

    def show_login(self):

        self.centralwidget.show()
        self.QLineEdit.setText("")
        self.QLineEdit_2.setText("")
        self.QLineEdit.show()
        self.QLineEdit_2.show()
        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.loginbutton_2.show()
        self.menubar.show()
        self.statusbar.show()
        self.loginbutton_2.show()
        self.back_arrow.show()

    def hide_login(self):
        self.QLineEdit.hide()
        self.QLineEdit_2.hide()
        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.loginbutton_2.hide()
        self.menubar.hide()
        self.statusbar.hide()
        self.loginbutton_2.hide()
        self.back_arrow.hide()

    def show_register(self):
        self.centralwidget.show()
        self.label7.show()
        self.label_8.show()
        self.label_9.show()
        self.loginbutton_3.show()
        self.label_10.show()
        self.label_11.show()
        self.admin_radiobutton.show()
        self.researcher_radiobutton.show()
        self.label_12.show()

        self.firstname_txt.setText("")
        self.lastname_txt.setText("")
        self.username_txt.setText("")
        self.password_txt.setText("")

        self.firstname_txt.show()
        self.lastname_txt.show()
        self.username_txt.show()
        self.password_txt.show()
        self.menubar.show()
        self.statusbar.show()
        self.back_arrow.show()

    def hide_register(self):

        self.label7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.loginbutton_3.hide()
        self.label_10.hide()
        self.label_11.hide()
        self.admin_radiobutton.hide()
        self.researcher_radiobutton.hide()
        self.label_12.hide()
        self.firstname_txt.hide()
        self.lastname_txt.hide()
        self.username_txt.hide()
        self.password_txt.hide()
        self.menubar.hide()
        self.statusbar.hide()
        self.back_arrow.hide()

    def show_researcher_upload(self):
        self.centralwidget.show()
        self.pushButton1.show()
        self.Researcher_label.show()
        self.label13.show()
        self.back_arrow.show()
        self.result_label.show()
        self.classify_result.show()

    def hide_researcher_upload(self):
        # self.centralwidget.hide()
        self.pushButton1.hide()
        self.Researcher_label.hide()
        self.label13.hide()
        self.back_arrow.hide()
        self.result_label.hide()
        self.classify_result.hide()

    def show_admin_upload(self):
        self.centralwidget.show()
        self.pushButton2.show()
        self.admin_label.show()
        self.label14.show()
        self.back_arrow.show()
        self.result_label2.show()
        self.train_result.show()

    def hide_admin_upload(self):
        self.pushButton2.hide()
        self.admin_label.hide()
        self.label14.hide()
        self.back_arrow.hide()
        self.result_label2.hide()
        self.train_result.hide()

    def Loginclick(self):
        self.hide_home()
        self.show_login()

        # self.window=QtWidgets.QMainWindow()
        # self.ui=Ui_Login()
        # self.ui.setupUi(self.window)
        # self.window.show()

    def Registerclick(self):
        self.hide_home()
        self.show_register()
        # self.window=QtWidgets.QMainWindow()
        # self.ui=Ui_Register()
        # self.ui.setupUi(self.window)
        # self.window.show()

    def loginonclick(self):
        username = self.QLineEdit.text()
        password = self.QLineEdit_2.text()
        if username=="" or password=="":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Fill in All Fields")
            msg.setWindowTitle("Data Missing")
            msg.exec_()
        else:
            self.check(username, password)

    def registeronclick(self):
        rfirstname = self.firstname_txt.text()
        rlastname = self.lastname_txt.text()
        rusername = self.username_txt.text()
        rpassword = self.password_txt.text()

        if self.admin_radiobutton.isChecked():
            type = 1
        elif self.researcher_radiobutton.isChecked():
            type = 2

        if rfirstname == "" or rlastname == "" or rusername == "" or rpassword == "" or (
                self.admin_radiobutton.isChecked() == False and self.researcher_radiobutton.isChecked() == False):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Fill in All Fields")
            msg.setWindowTitle("Data Missing")
            msg.exec_()
        else:
            self.insert(rfirstname, rlastname, rusername, rpassword, type)

    def adminlogin(self):

        self.hide_login()
        self.hide_register()
        self.hide_home()
        self.show_admin_upload()

    def researcherlogin(self):
        self.hide_login()
        self.hide_register()
        self.hide_home()
        self.hide_admin_upload()
        self.show_researcher_upload()

    def insert(self, fname, lname, uname, realpassword, type):
        password=self.sha(realpassword)
        found = False
        docs = db.collection(u'users').where(u'username', u'==', uname).stream()

        for doc in docs:
            found=True
            # print(u'{} => {}'.format(doc.id, doc.to_dict()))

        if(found == False):
            doc_ref = db.collection(u'users').document()
            doc_ref.set({
                u'firstname': fname,
                u'lastname': lname,
                u'username': uname,
                u'password': password,
                u'type': type
            })
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Registered Successfully')
            msg.setWindowTitle("Done")
            msg.exec_()
            self.hide_register()
            self.show_login()
        else:
            self.username_txt.setFocus()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("That User name is already taken")
            msg.setWindowTitle("Already exists")
            msg.exec_()

    def check(self,uname,realpassword):
        found=False
        type=0
        password = self.sha(realpassword)
        docs = db.collection(u'users').where(u'username', u'==', uname).where(u'password', u'==', password).stream()

        for doc in docs:
            found=True
            type=doc.get('type')
        if found == True:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Logged in Successfully')
            msg.setWindowTitle("Done")
            msg.exec_()
            if(type==1):
               self.adminlogin()
            elif(type==2):
                self.researcherlogin()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong username or password")
            msg.setWindowTitle("Login Failed")
            msg.exec_()

    def sha(self,word):
        enc = hashlib.sha384(word.encode())
        result=enc.hexdigest()
        return result

    def handle_non_numerical_data(self,df):
        columns = df.columns.values
        for column in columns:
            x = 0
            text_digit_vals = {}

            def convert_to_int(val):
                return text_digit_vals[val]

            if df[column].dtype != np.int64 and df[column].dtype != np.float64:
                column_contents = df[column].values.tolist()
                unique_elements = set(column_contents)
                # x = 0
                for unique in unique_elements:
                    if unique not in text_digit_vals:
                        text_digit_vals[unique] = x
                        x += 1
                df[column] = list(map(convert_to_int, df[column]))
        return df

    def classify(self,path):
        df = pd.read_csv(path)

        clf3 = load('SVR_93.joblib')
        df = self.handle_non_numerical_data(df)

        df = df.dropna(axis='rows')

        arr = clf3.predict(df)

        for i in range(len(arr)):

            if arr[i] < 0.5:

                print("diseased")
                self.classify_result.setText("Diseased")

            else:

                print("Normal")
                self.classify_result.setText("Normal")


    def train(self,path):

        df = pd.read_csv(path)  # csv da no3 el dataset -- df stands for data frame

        df = df.dropna(axis='columns')

        diag_dict = {"Diseased": 0, "Normal": 1}

        df['Status'] = df['Status'].map(diag_dict)

        parameters = {'kernel': ('linear', 'rbf'), 'C': [1.5, 10], 'gamma': [1e-7, 1e-4]}

        svc = svm.SVC(gamma="scale")

        # clf2 = GridSearchCV(svc, parameters, cv=5)

        svr = svm.SVR()

        df = self.handle_non_numerical_data(df)

        clf2 = GridSearchCV(svr, parameters)

        #     clf = RandomizedSearchCV(svc, parameters)

        clf = svm.SVR()

        df = sklearn.utils.shuffle(df)

        X = df.drop("Status", axis=1).values

        y = df['Status'].values

        X = preprocessing.scale(X)

        X = preprocessing.scale(X)

        test_size = np.math.ceil(len(df) * 0.3)

        X_train = X[:-test_size]

        y_train = y[:-test_size]

        X_test = X[-test_size:]

        y_test = y[-test_size:]

        clf.fit(X_train, y_train)
        accuracy=int(clf.score(X_test, y_test)*100)
        self.train_result.setText(str(accuracy)+"%")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

