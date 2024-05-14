from confluent_kafka.admin import (AdminClient, NewTopic, ConfigResource)


conf = {
    'bootstrap.servers' : ['kafka-0:9092,kafka-1:9092']
}

admin = AdminClient(
    conf
)


# return True if topic exists and False if not
def topic_exists(admin,topic):
    
    #Get metadata of topics
    metadata = admin.list_topics()
    
    #Check whether topic already exists
    for i in iter(metadata.topics.value()):
        if (i == topic):
            return True
    return False


# create new topic and return results dictionary
def create_topic(admin, topic, **kwargs):
    
     # Define default attribute for a topic
    defaults = {
        "num_partitions": 1,
        "replication_factor": 1
    }
    
    # Get the value for topic params. Default to the default value or user specification if defined.
    topicParams = {key: kwargs.get(key, default) for key, default in defaults.items()}
    
    # Get the num_partition from param 
    num_partitions = topicParams['num_partitions']
    
    #Get the replication factor from param
    replication_factor = topicParams['replication_factor']
    
    new_topic = NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor) 
    
    
    result_dict = admin.create_topics([new_topic])
    
    
    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
            
# get max.message.bytes property
def get_max_size(admin, topic):
    resource = ConfigResource('topic', topic)
    result_dict = admin.describe_configs([resource])
    config_entries = result_dict[resource].result()
    max_size = config_entries['max.message.bytes']
    return max_size.value

# set max.message.bytes for topic
def set_max_size(admin, topic, max_k):
    config_dict = {'max.message.bytes': str(max_k*1024)}
    resource = ConfigResource('topic', topic, config_dict)
    result_dict = admin.alter_configs([resource])
    result_dict[resource].result()
             
create_topic(admin,'toll',num_partitions = 2, replication_factor = 2)