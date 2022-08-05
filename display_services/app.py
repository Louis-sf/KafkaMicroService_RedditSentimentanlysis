from flask import Flask

import display

app = Flask(__name__)
# socketio = SocketIO(app)


@app.route('/')
def display():
    return display.drawing()


if __name__ == '__main__':
    app.run(debug=True, port=8000)
