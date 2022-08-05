import os
import sys

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
    return user_input.prompt_input(subreddit, start, end)


if __name__ == '__main__':
    # app.config.from_object(Config())
    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    app.run(debug=True)




