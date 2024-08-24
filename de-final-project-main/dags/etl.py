import tweepy
import json
import re
import time
from bson import json_util
from sqlalchemy import create_engine
import pandas as pd
from kafka import KafkaConsumer, KafkaProducer

counter = 0


def start_etl():

    producer = KafkaProducer(bootstrap_servers=['broker'])

    class IDPrinter(tweepy.StreamingClient):
        def __init__(self, BEARER_TOKEN):
            self.counter = 0
            self.limit = 10
            super(IDPrinter, self).__init__(BEARER_TOKEN)

        def on_connect(self):
            print("Connected")
            return super().on_connect()

        def on_disconnect(self):
            print("Disconnected")
            return super().on_disconnect()

        def on_data(self, tweet):
            try:

                all_data = json.loads(tweet)
                data = {
                    'text': all_data['data']['text'],
                }
                jdata = json.dumps(
                    data, default=json_util.default).encode('utf-8')
                print(jdata)
                producer.send('projek_akhir', jdata)
                self.counter += 1
                if self.counter < self.limit:
                    return True
                else:
                    streaming.disconnect()
                return super().on_tweet(tweet)
            except BaseException as e:
                print('failed on_status,', str(e))
                time.sleep(5)

    consumer = KafkaConsumer('projek_akhir', bootstrap_servers=['broker'],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='consumers',
                             value_deserializer=lambda x: x.decode('utf8'),
                             consumer_timeout_ms=1000,
                             heartbeat_interval_ms=1000,
                             api_version=(3, 0, 0))

    engine = create_engine(
        'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')

    def preprocessing(text):
        text = text.lower()
        text = re.sub(
            '(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', text)
        text = re.sub('\\+n', ' ', text)
        text = re.sub('\n', " ", text)
        text = re.sub('rt', ' ', text)
        text = re.sub('RT', ' ', text)
        text = re.sub('user', ' ', text)
        text = re.sub('USER', ' ', text)
        text = re.sub(
            '((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', ' ', text)
        text = re.sub(':', ' ', text)
        text = re.sub(';', ' ', text)
        text = re.sub('@', ' ', text)
        text = re.sub('\\+n', ' ', text)
        text = re.sub('\n', " ", text)
        text = re.sub('\\+', ' ', text)
        text = re.sub('  +', ' ', text)
        text = re.sub(r'[-+]?[0-9]+', '', text)
        text = text.replace("\\", " ")
        text = re.sub('x..', ' ', text)
        text = re.sub(' n ', ' ', text)
        text = re.sub('\\+', ' ', text)
        text = re.sub('  +', ' ', text)
        return text

    def load(msg):
        engine = create_engine(
            'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')
        temp = json.loads(msg)
        print(temp)
        data = pd.DataFrame([preprocessing(temp['text'])])
        data.columns = ["0"]
        data.to_sql('tweets', con=engine, if_exists='append', index=False)

    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADAfkwEAAAAAroT3heQnRThxsNGhpOChKH6tSvs%3DrQUFlbEwdjup3PxEk1vW96Gsp2Ac5HL2NEwg7jJL4Hmakr03QM"

    streaming = IDPrinter(BEARER_TOKEN)
    streaming.add_rules(tweepy.StreamRule("alice in borderland lang:en"))
    streaming.filter()

    for msg in consumer:
        load(msg.value)

    datasql = pd.read_sql_table('tweets', engine)
    print(datasql.head)
