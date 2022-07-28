from flask import Flask, request
from threading import Thread
import user_input
from reddit_api_poller_services import reddit_api_poller
app = Flask(__name__)


@app.route('/')
def index():
    app.logger.info('hello')
    subname = request.args.get("subreddit", "")
    startdate = request.args.get("startdate", "")
    enddate = request.args.get("enddate", "")
    result = post_input(subname, startdate, enddate)
    if result == '':
        result = 'Request Failed'
    else:
        result = 'Request Succeed' + result
    return """
            <div>
                <h1>Welcome to Reddit Sentiment Analysis microservices powered by Apache Kafka and Confluent<h1>
            <div>
            <form action="" method="get">
                <input type = "text" name = "subreddit" placeholder = "subreddit">
                <input type = "text" name = "startdate" placeholder = "start date">
                <input type = "text" name = "enddate" placeholder = "end date">
                <input type="submit" value="Search">
              </form>""" + result


def post_input(subreddit, start, end):
    app.logger.info('jumping to user_input.py')
    return user_input.prompt_input(subreddit, start, end)


if __name__ == '__main__':
    app.run(debug=True)


@app.before_first_request
def launch_consumers():
    app.logger.info("thread creating")
    api_poller_t = Thread(target=reddit_api_poller.consuming_request())
    app.logger.info("thread created and starting")
    api_poller_t.start()

#@app.before_first_request
