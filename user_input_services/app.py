import os
import sys
import subprocess

from flask import Flask, request, render_template
from threading import Thread
import user_input


app = Flask(__name__, static_folder='templates')


@app.route('/')
def index():
    app.logger.info('hello')
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
    fn = getattr(sys.modules['__main__'], '__file__')
    root_path = os.path.abspath(os.path.dirname(fn))
    app.logger.info(root_path)
    return render_template("index.html", data=data)


def post_input(subreddit, start, end):
    app.logger.info('jumping to user_input.py')
    app.logger.info(subreddit)
    app.logger.info(start)
    app.logger.info(end)
    return user_input.prompt_input(subreddit, start, end)


@app.before_first_request
def run_subprocess():
    subprocess.call(['sh', 'run.sh'])


if __name__ == '__main__':
    app.run(debug=True)




