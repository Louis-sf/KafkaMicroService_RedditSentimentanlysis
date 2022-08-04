import csv
import json
import sys
from confluent_kafka import Consumer, KafkaError
sys.path.append('../')
import ccloud_lib
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
green = '\x1b[32m'
reset = "\x1b[0m"


def histogram(prefix, value, color):
    bar = "=" * value
    return f"{prefix: >10}: {value: >5} {color}{bar}{reset}"


config_file = "../secrets/python.config"
consumer_topic = "pksqlc-kj9ppAVG_SCORE_PER_REQUESTJSON"
conf = ccloud_lib.read_ccloud_config(config_file)

consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
consumer_conf['group.id'] = 'indefiniteconsumer'
consumer_conf['auto.offset.reset'] = 'latest'
consumer_conf['enable.auto.commit'] = 'false'

display_Consumer = Consumer(conf)
display_Consumer.subscribe([consumer_topic])

r_id_mem = set()
f = open("consumer_data.csv", "w")
writer = csv.writer(f)
fields = ['SUB_REDDIT', 'REQUEST_ID', 'AVG_NEG', 'AVG_POS', 'AVG_NEU', 'AVG_COM']
writer.writerow(fields)
f.close()
while True:
    try:
        msg = display_Consumer.poll(1)
        if msg is None:
            print('waiting for message')
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
            break
        else:
            f = open("consumer_data.csv", "w")
            writer = csv.writer(f)
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
            r_id_mem.add(r_id)
            curr_row = [subR, r_id, AVG_NEG, AVG_POS, AVG_NEU, AVG_COM]
            print("record{} written".format(curr_row))
            writer.writerow(curr_row)
            f.close()
            # space = ' '*10
            # neg_bar = histogram("Negative", int(AVG_NEG), red) + space + '\n'
            # pos_bar = histogram("Positive", int(AVG_POS), yellow) + space + '\n' + space
            # neu_bar = histogram("Neutral", int(AVG_NEU), green) + space + '\n' + space

            # res = 'The {subR} subreddit you requested has average negative score {AVG_NEG}, average postive score ' \
            #       '{AVG_POS}, average neutral score {AVG_NEU} and average compound score {AVG_COM}'.format(
            #     subR=subR, AVG_NEG=round(AVG_NEG, 2), AVG_POS=round(AVG_POS, 2), AVG_NEU=round(AVG_NEU, 2),
            #     AVG_COM=round(AVG_COM, 2)) + space
            # print('\r' + neg_bar + pos_bar + neu_bar + res, end='\r')
            # print('\r'+histogram("Negative", int(AVG_NEG), red)+space+'\n', end='\r')
            # print('\r'+histogram("Neutral", int(AVG_NEU), yellow)+space+'\n', end='\r')
            # print('\r'+histogram("Good", int(AVG_POS), green)+space+'\n', end='\r')
    except KeyError as er:
        print(er)
    except KafkaError as ke:
        print(ke)
    except Exception as e:
        print(e)
