from time import time
from kafka import KafkaProducer
from faker import Faker
import json, time

faker = Faker()

def get_register():
    return {
        'name': faker.name(),
        'year' : faker.year()
    }
    
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'], # server name
    value_serializer = json_serializer # function callable
    )

while True:
    user = get_register()
    producer.send(
        'second_topic',user
    )
    time.sleep(3)
