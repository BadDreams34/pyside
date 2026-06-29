'''Encrypted Notes Taking App
Program to secretly take notes and store them with no clues left behind'''

import sys
from encodings import utf_8
import datetime
import encryption
import PySide6
from PySide6 import QtCore , QtGui , QtWidgets

# after encrypting IF THE PASSWORD IS RIGHT HOW DO I KNOW
# just check if the previous decryption is passing on with the current password !


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.password = ''

        self.setWindowTitle("Unsevered")
        layout = QtWidgets.QVBoxLayout()
        self.box = QtWidgets.QComboBox()
        self.box.addItems(["Access used"])
        self.box.setCurrentIndex(-1)
        layout.addWidget(self.box)
        self.box.hide()

        self.lineedit = QtWidgets.QTextEdit()
        self.lineedit.setFixedHeight(40)
        self.lineedit.setPlaceholderText("Use Me !")
        self.used = QtWidgets.QPushButton("save it !!!")


        self.lineedit.textChanged.connect(self.expand_height)

        layout.addWidget(self.lineedit)
        layout.addWidget(self.used)


        #the top text
        label = QtWidgets.QLabel("Its not a guarentee that you are gonna never forget this program ! ")
        font = label.font()
        font.setPointSize(30)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label)

        #lets make it super ugly
        g_search = QtWidgets.QLabel()
        g_search.setPixmap(QtGui.QPixmap("img_1.png"))
        g_search.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        #checkbox
        self.checkbox = QtWidgets.QCheckBox("You gotta check it !")

        layout.addWidget(self.checkbox, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.checkbox.clicked.connect(self.checkbox_state)
        self.used.clicked.connect(self.on_save_data)

        layout.addWidget(g_search)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.box.currentTextChanged.connect(self.opt_selected)
    def expand_height(self):
        self.lineedit.setFixedHeight(self.lineedit.document().lineCount() * 40)

    def checkbox_state(self,state):
        self.checkbox.setEnabled(False)
        self.box.show()
    def on_save_data(self):
        text = self.lineedit.toPlainText() #pass password before ,
        if text:
            dt = datetime.datetime.now()
            line = f"{dt.strftime("%d %b, %Y %H:%M:%S")} {text}"
            password = text.split(',')[0]

            with open("enc.txt", "rb") as file:
                text = file.read()
            if len(text) != 0:
                prev_pass = encryption.decrypt_file("enc.txt", password)
                if prev_pass == 0:
                    wrong_pas = QtWidgets.QDialog(self)
                    pas_layout = QtWidgets.QVBoxLayout(wrong_pas)
                    label = QtWidgets.QLabel("Please Check Your Password")
                    ok_but = QtWidgets.QPushButton("Ok")
                    pas_layout.addWidget(label)
                    pas_layout.addWidget(ok_but)
                    ok_but.clicked.connect(wrong_pas.accept)
                    wrong_pas.exec()
                else:
                    with open("enc.txt", 'wb') as file:
                        file.write(prev_pass + b'\n')
                        file.write((line + '\n').encode('utf-8'))
            else:
                with open("enc.txt", 'ab') as file:
                    file.write((line + '\n').encode('utf-8'))

            encryption.encrypt_file("enc.txt",password)

        self.lineedit.clear()

    def opt_selected(self,text):
        if text == "Access used":
            pass_dialog.show()


class PassDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        self.edit = QtWidgets.QLineEdit()
        self.ok_but = QtWidgets.QPushButton("OK")
        layout.addWidget(self.edit)
        layout.addWidget(self.ok_but)
        self.setLayout(layout)
        self.ok_but.clicked.connect(self.on_click_ok)

    def on_click_ok(self):
       passwords = encryption.decrypt_file("enc.txt", self.edit.text())
       if not passwords:
           self.edit.clear()
           wrong_pass = QtWidgets.QDialog(self)
           pas_layout = QtWidgets.QVBoxLayout(wrong_pass)
           label = QtWidgets.QLabel("Please Check Your Password")
           ok_but = QtWidgets.QPushButton("Ok")
           pas_layout.addWidget(label)
           pas_layout.addWidget(ok_but)
           ok_but.clicked.connect(wrong_pass.accept)
           wrong_pass.exec()
       else: # when entered password is correct
           self.edit.clear()
           pas_dialog = QtWidgets.QDialog(self)
           pas_layout = QtWidgets.QVBoxLayout(pas_dialog)
           print(passwords.decode())
           password = QtWidgets.QLabel(passwords.decode())
           pas_layout.addWidget(password)
           pas_dialog.exec()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
pass_dialog = PassDialog()
pass_dialog.hide()
app.exec()


