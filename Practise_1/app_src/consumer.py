
from confluent_kafka import Consumer
import json, time

    
def json_deserializer(data):
    """
    Deserialize json data

    Args:
        data: The data to deserialize.
    """
    return json.loads(data)


consumer_conf = {'bootstrap.servers': 'kafka:9092',
                'group.id': '1',
            'auto.offset.reset': "earliest"}
 
consumer = Consumer(consumer_conf)

consumer.subscribe(['exercise_topic'])

while True:
    try:
        # SIGINT can't be handled when polling, limit timeout to 1 second.
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        user = json_deserializer(msg.value())

        if user is not None:
            print(f"User name: {user['name']}, year: {user['year']}")
    except KeyboardInterrupt:
        break

consumer.close()
