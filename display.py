import csv
import json
import sys
from confluent_kafka import Consumer, KafkaError
sys.path.append('/')
import ccloud_lib
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
green = '\x1b[32m'
reset = "\x1b[0m"


def histogram(prefix, value, color):
    bar = "=" * value
    return f"{prefix: >10}: {value: >5} {color}{bar}{reset}"


config_file = "secrets/python.config"
consumer_topic = "display_result"
conf = ccloud_lib.read_ccloud_config(config_file)

consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
consumer_conf['group.id'] = 'indefiniteconsumer'
consumer_conf['auto.offset.reset'] = 'latest'
consumer_conf['enable.auto.commit'] = 'false'

display_Consumer = Consumer(conf)
display_Consumer.subscribe([consumer_topic])

r_id_mem = set()
f = open("user_input_services/templates/consumer_data.csv", "w")
writer = csv.writer(f)
fields = ['SCORE', 'VALUE']
f.close()
ft = open("user_input_services/templates/hi.txt", "w")
print('header written')
while True:
    try:
        msg = display_Consumer.poll(1)
        if msg is None:
            print('csvwriter waiting for message')
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
            break
        else:
            print("open file in the loop")
            f = open("user_input_services/templates/consumer_data.csv", "w")
            writer = csv.writer(f)
            writer.writerow(fields)
            record_value = msg.value()
            record_key = msg.key()
            key = json.loads(record_key)
            data = json.loads(record_value)
            subR = key['SUB_REDDIT']
            r_id = key['REQUEST_ID']
            AVG_NEG = data['AVG_NEG']
            AVG_POS = data['AVG_POS']
            AVG_NEU = data['AVG_NEU']
            AVG_COM = data['AVG_COM']
            if r_id not in r_id_mem:
                f.truncate(0)
                writer.writerow(fields)
                r_id_mem = set()
                print("new r_id, rewrite csv..")
            r_id_mem.add(r_id)
            neg = ['AVG_NEG', str(AVG_NEG)]
            print("record{} written".format(neg))
            writer.writerow(neg)
            pos = ['AVG_POS', str(AVG_POS)]
            print("record{} written".format(pos))
            writer.writerow(pos)
            neu = ['AVG_NEU', str(AVG_NEU)]
            print("record{} written".format(neu))
            writer.writerow(neu)
            com = ['AVG_COM', str(AVG_COM)]
            print("record{} written".format(com))
            writer.writerow(com)
            f.close()
    except KeyError as er:
        print(er)
    except KafkaError as ke:
        print(ke)
    except Exception as e:
        print(e)
