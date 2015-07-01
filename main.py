#main.py

from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None


def background_work():
	while True: 
		time.sleep(1) #One second wait between image change
		
		imageString = getRandomImageString()
		
		socketio.emit('newImage', {'data': imageString}, namespace='/test')
		
		
@app.route('/')
def index():
	global thread
	if thread is None: 
		thread = Thread(target=background_work)
		thread.start()
	return render_template('index.html')
	
	
if __name__ == '__main__':
	socketio.run(app)