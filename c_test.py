import socketio, time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on('receive')
def receive(data):
  print('receive', data)

sio.connect('http://localhost:5000')

while True:
  sio.emit('send', time.time())
  time.sleep(1)
  
sio.wait()

