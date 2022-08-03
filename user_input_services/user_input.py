import json
from confluent_kafka import Producer
import sys
from datetime import datetime
import uuid
import psaw_helper
sys.path.append('../')
import ccloud_lib

# ###############Kafka Producer Config#################
topic = "user_input"
config_file = "../secrets/python.config"
conf = ccloud_lib.read_ccloud_config(config_file)
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
userProducer = Producer(producer_conf)


def prompt_input(subreddit, start, end):
    try:
        # sub = input("Please choose a subreddit you would like to analyze, don't include /r in the beginning\n")
        sub = subreddit
        if psaw_helper.sub_invalid(sub):
            print("this subreddit does not exist, please enter again")
            return '1'
        # my_string = str(input('Please enter the start date: \nEnter date(yyyy-mm-dd): '))
        start_date = datetime.strptime(start, "%Y-%m-%d").timestamp()
        # my_string = str(input('Please enter the end date: \nEnter date(yyyy-mm-dd): '))
        end_date = datetime.strptime(end, "%Y-%m-%d").timestamp()
        request_id = str(uuid.uuid4())

        schema = {
            "request_id": request_id,
            "sub_reddit": sub,
            "start_date": str(int(start_date)),
            "end_date": str(int(end_date))
        }
        userProducer.produce(topic, value=json.dumps(schema))
        return json.dumps(schema)
    except ValueError:
        print("user_input.py : Please make sure the input format is correct", "The error is, ", ValueError)
        return ''
    except Exception as e:
        print(e)
        return ''
