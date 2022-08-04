import json
from confluent_kafka import Producer
from confluent_kafka import Consumer
import ccloud_lib
from nltk.sentiment import SentimentIntensityAnalyzer

# ############### Consumer Config #####################
config_file = "secrets/python.config"
consumer_topic = "reddit_raw_data"
conf = ccloud_lib.read_ccloud_config(config_file)

consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
consumer_conf['group.id'] = 'indefiniteconsumer'
consumer_conf['auto.offset.reset'] = 'latest'
consumer_conf['enable.auto.commit'] = 'false'

sentiment_consumer = Consumer(conf)
sentiment_consumer.subscribe([consumer_topic])

# ############# Producer Config #####################
producer_topic = "scored_thread"
config_file = "secrets/python.config"
conf = ccloud_lib.read_ccloud_config(config_file)
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
raw_producer = Producer(producer_conf)

# ############# Polling Raw Thread #####################
sia = SentimentIntensityAnalyzer()
try:
    while True:
        msg = sentiment_consumer.poll(1.0)
        if msg is None:
            print("sa waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
            break
        else:
            # Check for Kafka message
            record_value = msg.value()
            data = json.loads(record_value)
            id = data['id']
            title_text = data['title_text']
            sub_reddit = data['sub_reddit']
            request_id = data['request_id']
            url = data['url']
            score = sia.polarity_scores(title_text)
            Schema = {
                'id': id,
                'request_id': request_id,
                'title_text': title_text,
                'sub_reddit': sub_reddit,
                'url': url,
                'score_negative': score['neg'],
                'score_neutral': score['neu'],
                'score_positive': score['pos'],
                'score_compound': score['compound']
            }
            to_be_recorded = json.dumps(Schema)
            raw_producer.produce(topic=producer_topic, key=id, value=to_be_recorded)
        raw_producer.flush()
except KeyboardInterrupt:
    pass
