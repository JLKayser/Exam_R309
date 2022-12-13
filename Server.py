from socket import AF_INET, SOCK_STREAM
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QDialog, QMessageBox, QTabWidget, QVBoxLayout, QPlainTextEdit, QTextEdit, QTableWidget,QTableWidgetItem
import sys
from threading import Thread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.resize(300,300)
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Le serveur de tchat")

        self.__serveur = QLabel("Serveur")
        self.__serveurEdit = QLineEdit("localhost")
        self.__port = QLabel("Port")
        self.__portEdit = QLineEdit("10000")
        self.__nbrClient = QLabel("Nombre de client maximum")
        self.__clientEdit = QLineEdit("5")
        self.__start = QPushButton("Demarrage du serveur")
        self.__recv = QTextEdit("")
        self.__recv.setReadOnly(True)
        self.__exit = QPushButton("Quitter")

        grid.addWidget(self.__serveur,0,0)
        grid.addWidget(self.__serveurEdit,0,1)
        grid.addWidget(self.__port,1,0)
        grid.addWidget(self.__portEdit,1,1)
        grid.addWidget(self.__nbrClient,2,0)
        grid.addWidget(self.__clientEdit,2,1)
        grid.addWidget(self.__start,3,0,1,2)
        grid.addWidget(self.__recv,4,0,1,2)
        grid.addWidget(self.__exit,5,0,1,2)

        self.__start.clicked.connect(self.__demarrage)
        self.__exit.clicked.connect(self.__quitter)

        thread_recu = Thread(target=self.__demarrage)
        thread_recu.start()



    def __demarrage(self):
        try:
            server = socket.socket()
            HOST = self.__serveurEdit.text()
            PORT = int(self.__portEdit.text())
            ecoute = int(self.__clientEdit.text())

            print(f"HOST = {HOST} PORT = {PORT} ECOUTE = {ecoute}")

            server.bind((HOST, PORT))
            server.listen(ecoute)
            conn, address = server.accept()
            print("Connection from: " + str(address))
            self.__start.setText("Arret du server")
            while self.__recv:
                data = conn.recv(1024).decode()
                if not data:
                    server.close()
                    self.__demarrage()
                    break
                self.__recv.append(data + '\n')
                print("from connected user: " + str(data))
                conn.send(data.encode())

            conn.close()
        except Exception as err:
            print(f'non {err}')
            self.__InValid()

    def __quitter(self):
        self.close()


    def __InValid(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not valid")
        msg.resize(500, 500)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Connexion refuser -> Entrez une bonne IP ou port")
        msg.exec()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
