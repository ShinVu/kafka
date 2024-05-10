from confluent_kafka.admin import AdminClient, NewTopic

admin_client = AdminClient({
    "bootstrap.servers" :"kafka_combined:9092"
})

topic_list = []
topic_list.append(NewTopic("exercise_topic", num_partitions=1,replication_factor=1))

# Call create_topics to asynchronously create topics. A dict
# of <topic,future> is returned.
fs = admin_client.create_topics(new_topics=topic_list,validate_only=False)

# # Wait for each operation to finish.
for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))