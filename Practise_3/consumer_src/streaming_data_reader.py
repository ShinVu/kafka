"""
Streaming data consumer
"""
from datetime import datetime
from confluent_kafka import Consumer, KafkaError
import mysql.connector as mysql

TOPIC='toll'
DATABASE = 'tolldata'
USERNAME = 'root'
PASSWORD = 'root'

# Configuration details for mysql connection
config = {
    'user': USERNAME,
    'password': PASSWORD,
    'host': 'mysql',  # This is the service name defined in docker-compose.yml
    'port': 3306,
    'db': DATABASE
}

print("Connecting to the database")
try:
    connection = mysql.connect(**config)
except Exception as e:
    print(e)
else:
    print("Connected to database")
    
cursor = connection.cursor()


print("Connecting to Kafka")

conf = {
    'bootstrap.servers' : ['kafka-0:9092,kafka-1:9092'],
    'group.id': "toll",
}

consumer = Consumer(conf)
print("Connected to Kafka")

# Subscribe to topic(s)
consumer.subscribe(['toll'])
print(f"Reading messages from the topic {TOPIC}")

while True:
    msg = consumer.poll(timeout=1.0)  # Poll for new messages
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition, the consumer reached the end of the topic
            continue
        else:
            # Handle other errors
            print(msg.error())
            break
    # Extract information from kafka
    message = msg.value().decode("utf-8")

    # Transform the date format to suit the database schema
    (timestamp, vehcile_id, vehicle_type, plaza_id) = message.split(",")

    dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
    timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

    # Loading data into the database table

    sql = "insert into livetolldata values(%s,%s,%s,%s)"
    result = cursor.execute(sql, (timestamp, vehcile_id, vehicle_type, plaza_id))
    print(f"A {vehicle_type} was inserted into the database")
    connection.commit()
    
connection.close()
