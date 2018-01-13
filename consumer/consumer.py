from pykafka import KafkaClient
from pykafka.protocol import CreateTopicRequest


POST_TOPIC = "post".encode("utf-8")
VIEW_TOPIC = "view".encode("utf-8")
TOPICS = (POST_TOPIC, VIEW_TOPIC)


client = None


def get_client():
    global client
    if client is None:
        client = KafkaClient(hosts='kafka:9092')
        client.cluster.update()
    return client


def run():
    cli = get_client()
    topic = cli.topics[VIEW_TOPIC]
    consumer = topic.get_simple_consumer()
    for message in consumer:
        if message is not None:
            print("%s: %s" % (message.offset, message.value))


if __name__ == "__main__":
    run()