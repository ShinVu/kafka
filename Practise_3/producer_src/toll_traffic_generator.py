"""
Top Traffic Simulator
"""
from time import sleep, time, ctime
from random import random, randint, choice
from confluent_kafka import Producer

conf = {
    'bootstrap.servers' : ['kafka-0:9092,kafka-1:9092']
}

producer = Producer(conf)

TOPIC = 'toll'

VEHICLE_TYPES = ("car", "car", "car", "car", "car", "car", "car", "car",
                 "car", "car", "car", "truck", "truck", "truck",
                 "truck", "van", "van")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        # print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        pass
        
# Generate mock data for producer
for _ in range(100000):
    # Trigger any available delivery report callbacks from previous produce() calls
    producer.poll(0)
    vehicle_id = randint(10000, 10000000)
    vehicle_type = choice(VEHICLE_TYPES)
    now = ctime(time())
    plaza_id = randint(4000, 4010)
    message = f"{now},{vehicle_id},{vehicle_type},{plaza_id}"
    print(f"A {vehicle_type} has passed by the toll plaza {plaza_id} at {now}.")
    message = message.encode("utf-8")
    
       # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    producer.produce(TOPIC, message, callback=delivery_report)
    sleep(random() * 2)
    
producer.flush()
