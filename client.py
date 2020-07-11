import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic

import socketio, time

ui_form = uic.loadUiType("main.ui")[0]

class SocketClient(QThread):
  add_chat = QtCore.pyqtSignal(str)
  sio = socketio.Client()
  
  def __init__(self, parent=None):
    super().__init__()
    self.main = parent
    self.is_run = False
    self.ip = 5000
    self.localhost = 'localhost'

  def set_host(self, ip, port):
    self.ip = ip
    self.port = port

  def run(self):
    host = 'http://%s:%s'%(self.ip, self.port) 
    
    self.connect(host)
    self.is_run = not self.is_run

  def connect(self, host):
    SocketClient.sio.on('receive', self.receive)
    SocketClient.sio.connect(host)
    self.add_chat.emit('채팅 서버와 접속 완료했습니다.')

  def send(self, msg):
    SocketClient.sio.emit('send', msg)
    self.add_chat.emit('[나]:%s'%(msg))

  def receive(self, msg):
    self.add_chat.emit('[상대방] %s'%(msg))

class ChatWindow(QMainWindow, ui_form) :
  def __init__(self):
    super().__init__()
    self.setupUi(self)

    self.btn_send.clicked.connect(self.send_message)
    self.btn_connect.clicked.connect(self.socket_connection)
    self.sc = SocketClient(self)

    self.sc.add_chat.connect(self.add_chat)

  def socket_connection(self):
    ip = self.input_ip.toPlainText()
    port = self.input_port.toPlainText()
    
    if (not ip) or (not port):
      self.add_chat('ip 또는 port 번호가 비었습니다.')  
      return

    self.sc.set_host(ip, port)

    if not self.sc.is_run:
      self.sc.start()

  def send_message(self):
    if not self.sc.is_run:
      self.add_chat('서버와 연결 상태가 끊겨 있어 메시지를 전송할 수 없습니다.')  
      return

    msg = self.input_message.toPlainText()
    self.sc.send(msg)
    self.input_message.setPlainText('')

  @pyqtSlot(str)
  def add_chat(self, msg):
    self.chats.appendPlainText(msg)

if __name__ == "__main__":
  app = QApplication(sys.argv) 
  myWindow = ChatWindow() 
  myWindow.setWindowTitle('멍개의 채팅 프로그램')
  myWindow.show()
  app.exec_()