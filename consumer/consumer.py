import time
import logging
import redis
from pykafka import KafkaClient
from pykafka.protocol import CreateTopicRequest


POST_TOPIC = "post".encode("utf-8")
VIEW_TOPIC = "view".encode("utf-8")
TOPICS = (POST_TOPIC, VIEW_TOPIC)
RECENT_KEY = 'posts'
TOP_KEY = 'top_posts'

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
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, queued_max_messages=1)
    logging.info("Starting to consume %s", topic)
    for message in consumer:
        if message is not None:
            logging.warning("%s: %s", message.offset, message.value)
            path = message.value.decode('utf-8')

            # handle weird old data
            prefix = 'http://localhost:5000'
            if path.startswith(prefix):
                path = path[len(prefix):]
            r = redis.Redis(host='redis')
            ts = int(time.time())
            r.zadd(RECENT_KEY, path, ts)
            r.zincrby(TOP_KEY, path, 1)

if __name__ == "__main__":
    run()
