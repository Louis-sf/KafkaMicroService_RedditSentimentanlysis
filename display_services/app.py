from flask import Flask

app = Flask(__name__)

if __name__ == 'main':
    app.run()


@app.route('/')
def display():
    return 'display result here'
