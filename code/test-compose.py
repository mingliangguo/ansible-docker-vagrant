import testcontainers.compose
import time
from time import sleep
from json import dumps
from json import loads
from kafka import KafkaProducer 
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic


COMPOSE_PATH = "." #the folder containing docker-compose.yml

def setup_module():  
    compose = testcontainers.compose.DockerCompose(COMPOSE_PATH)  
    compose.start()  
    print("compose started ...")
    time.sleep(10)  
    return compose

def teardown_module(compose):  
    compose.stop()

def create_topic(topic_name):
    print(f"create topic: {topic_name} ...")
    try:
        admin_client = KafkaAdminClient(
                bootstrap_servers="localhost:9092",
                client_id='test'
                )
        topic_list = []
        topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as ex:
        print(f"caught error: and ignore ...")

def test_kafka():  
    topic_name = "numtest"
    create_topic(topic_name)

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x:
            dumps(x).encode('utf-8'))

    message_count = 10
    print(f"try to send {message_count}  messages to topic: {topic_name} ...")
    for e in range(message_count):
        data = {'number' : e}
        print(f"try to send message: {data} to topic: {topic_name} ...")
        producer.send(topic_name, value=data)
        sleep(1)

    consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        message = message.value
        print('Received message {}'.format(message))
        message_count -= 1
        if message_count == 0:
            break


if  __name__ == "__main__":
    compose = setup_module()  
    test_kafka()
    print("begin to tear down ...")
    teardown_module(compose)
