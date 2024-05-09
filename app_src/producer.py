from time import time
from confluent_kafka import Producer
from faker import Faker
import json, time

faker = Faker()

def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))
    
    
def get_register():
    """
    Generate data for testing
    """
    return {
        'name': faker.name(),
        'year' : faker.year()
    }
    
def json_serializer(data):
    """
    Serialize json data

    Args:
        data: The data to serialize.
    """
    return json.dumps(data).encode('utf-8')

producer = Producer({
    "bootstrap.servers" : "kafka:9092" # server name
  }  )

while True:
    # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
    
    # Generate data
    user = get_register()
    
    try:
        producer.produce(
            topic="exercise_topic",
            value=json_serializer(user),
            on_delivery = delivery_report
        )
    except KeyboardInterrupt:
        break 
    except ValueError:
        print("Invalid input, discarding record...")
        continue
    
    time.sleep(3)
