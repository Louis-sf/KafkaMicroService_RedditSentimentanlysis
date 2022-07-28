from flask import Flask, request
from threading import Thread
import user_input

app = Flask(__name__)


@app.route('/')
def title():
    subname = request.args.get("subreddit", "")
    startdate = request.args.get("startdate", "")
    enddate = request.args.get("enddate", "")

    result = post_input(subname, startdate, enddate)
    if result == '':
        result = 'Request Failed'
    else:
        result = 'Request Succeed'
    return """<form action="" method="get">
                <input type = "text" name = "subreddit" placeholder = "subreddit">
                <input type = "text" name = "startdate" placeholder = "start date">
                <input type = "text" name = "enddate" placeholder = "end date">
                <input type="submit" value="Search">
              </form>""" + result


@app.route('/')
def post_input(subreddit, start, end):
    return user_input.prompt_input(subreddit, start, end)


if __name__ == '__main__':
    app.run(debug=True)


# @app.before_first_request
# def launch_consumers():
#     # t = Thread(target=user_input.prompt_input())
#     # t.start()
