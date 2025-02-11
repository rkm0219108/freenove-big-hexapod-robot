# -*- coding: utf-8 -*-
import getopt
import os
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow

from Control import *
from Server import *
from ui_server import Ui_server


class MyWindow(QMainWindow, Ui_server):
    def __init__(self):
        self.user_ui = True
        self.start_tcp = False
        self.server = Server()
        self.parseOpt()
        if self.user_ui:
            self.app = QApplication(sys.argv)
            super(MyWindow, self).__init__()
            self.setupUi(self)
            self.pushButton_On_And_Off.clicked.connect(self.on_and_off_server)
            self.on_and_off_server()
        if self.start_tcp:
            self.server.turn_on_server()
            self.server.tcp_enabled = True
            self.video = threading.Thread(
                target=self.server.transmission_video)
            self.video.start()
            self.instruction = threading.Thread(
                target=self.server.receive_instruction)
            self.instruction.start()
            if self.user_ui:
                self.pushButton_On_And_Off.setText('Off')
                self.states.setText('On')

    def parseOpt(self):
        self.opts, self.args = getopt.getopt(sys.argv[1:], "tn")
        for o, a in self.opts:
            if o in ('-t'):
                print("Open TCP")
                self.start_tcp = True
            elif o in ('-n'):
                self.user_ui = False

    def on_and_off_server(self):
        if self.pushButton_On_And_Off.text() == 'On':
            self.pushButton_On_And_Off.setText('Off')
            self.states.setText('On')
            self.server.turn_on_server()
            self.server.tcp_enabled = True
            self.video = threading.Thread(
                target=self.server.transmission_video)
            self.video.start()
            self.instruction = threading.Thread(
                target=self.server.receive_instruction)
            self.instruction.start()
        else:
            self.pushButton_On_And_Off.setText('On')
            self.states.setText('Off')
            self.server.tcp_enabled = False
            try:
                stop_thread(self.video)
                stop_thread(self.instruction)
            except Exception as e:
                print(e)
            self.server.turn_off_server()
            print("close")

    def closeEvent(self, event):
        try:
            stop_thread(self.video)
            stop_thread(self.instruction)
        except:
            pass
        try:
            self.server.video_socket.shutdown(2)
            self.server.instruction_socket.shutdown(2)
            self.server.turn_off_server()
        except:
            pass
        if self.user_ui:
            QCoreApplication.instance().quit()
        os._exit(0)


if __name__ == '__main__':
    myshow = MyWindow()
    if myshow.user_ui == True:
        myshow.show()
        sys.exit(myshow.app.exec_())
    else:
        try:
            pass
        except KeyboardInterrupt:
            myshow.closeEvent(myshow)
