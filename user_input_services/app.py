from flask import Flask, request
from threading import Thread, Event
import user_input
from reddit_api_poller_services import reddit_api_poller
from sentiment_analysis_services import sentiment_analysis
import flask_sock

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    app.logger.info('hello')
    subname = request.args.get("subreddit", "")
    startdate = request.args.get("startdate", "")
    enddate = request.args.get("enddate", "")
    result = post_input(subname, startdate, enddate)
    if result == '':
        result = 'Request Failed'
    elif result == '1':
        result = 'This subreddit does not exist, please try again'
    else:
        app.logger.info('request generated')
        result = 'Request Succeed' + result
        # launch_consumers()
    return app.send_static_file("index.html")
    # return """
    #         <div>
    #             <h1>Welcome to Reddit Sentiment Analysis microservices powered by Apache Kafka and Confluent<h1>
    #         <div>
    #         <form action="" method="get">
    #             <input type = "text" name = "subreddit" placeholder = "subreddit">
    #             <input type = "text" name = "startdate" placeholder = "start date">
    #             <input type = "text" name = "enddate" placeholder = "end date">
    #             <input type="submit" value="Search">
    #           </form>""" + result


def post_input(subreddit, start, end):
    app.logger.info('jumping to user_input.py')
    return user_input.prompt_input(subreddit, start, end)


# @app.before_first_request
def launch_consumers():
    # main_thread = Thread(target=index())
    # app.logger.info('main thread created, and running')
    # main_thread.start()
    app.logger.info("reddit_api_poller_thread creating")
    api_poller_t = Thread(target=reddit_api_poller.consuming_request(), daemon=True)
    app.logger.info("reddit_api_poller_thread created and starting")
    app.logger.info("sentiment_analysis_thread creating")
    sa_t = Thread(target=sentiment_analysis.sentiment_analysis(), daemon=True)
    app.logger.info("sentiment_analysis_thread created and starting")
    api_poller_t.start()
    sa_t.start()


if __name__ == '__main__':
    # app.config.from_object(Config())
    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    app.run(debug=True)




