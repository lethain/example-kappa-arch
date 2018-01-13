from flask import Flask
from pykafka import KafkaClient
from pykafka.protocol import CreateTopicRequest


POST_TOPIC = "post".encode("utf-8")
VIEW_TOPIC = "view".encode("utf-8")
TOPICS = (POST_TOPIC, VIEW_TOPIC)


app = Flask(__name__)
client = None


def get_client():
    global client
    if client is None:
        client = KafkaClient(hosts='kafka:9092')
        client.cluster.update()
        existing_topics = set(client.topics.keys())
        app.logger.info(existing_topics)
        missing = set(TOPICS).difference(existing_topics)
        app.logger.info("missing: %s" % (missing,))
        if missing:
            create_topic(client, list(missing))
    return client


def create_topic(client, names):
    topics = [CreateTopicRequest(name.encode(), 1, 1, [], []) for name in names]
    broker = list(client.cluster._brokers.values())[0]
    broker.create_topics(topics, 5000)


@app.route('/')
def hello():
    client = get_client()

    return "Hello world!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
