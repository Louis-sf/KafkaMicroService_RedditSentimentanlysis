from flask import Flask
import display

import signal
from flask_socketio import SocketIO

import display_services.display

app = Flask(__name__)
# socketio = SocketIO(app)


@app.route('/')
def display():
    return display_services.display.drawing()


if __name__ == '__main__':
    app.run(debug=True, port=8000)
