import os
import sys
import subprocess

from flask import Flask, request, render_template
from threading import Thread
import user_input


app = Flask(__name__, static_folder='templates')


@app.route('/')
def index():
    subname = request.args.get("subreddit", "")
    startdate = request.args.get("startdate", "")
    enddate = request.args.get("enddate", "")
    result = post_input(subname, startdate, enddate)
    if result == '':
        result = 'Enter your request'
    elif result == '1':
        result = 'This subreddit does not exist, please try again'
        return result
    else:
        app.logger.info('request generated')
        result = 'Request Succeed' + result
    data = {'result': result}
    return render_template("index.html", data=data)


def post_input(subreddit, start, end):
    return user_input.prompt_input(subreddit, start, end)


@app.before_first_request
def run_subprocess():
    subprocess.call(['sh', 'run.sh'])


if __name__ == '__main__':
    app.run(debug=True)




