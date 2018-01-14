import datetime
import time
from flask import Flask, request, render_template
from pykafka import KafkaClient
from pykafka.protocol import CreateTopicRequest
import redis


POST_TOPIC = "post".encode("utf-8")
VIEW_TOPIC = "view".encode("utf-8")
RECENT_KEY = 'posts'
TOP_KEY = 'top_posts'
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


def publish(client, topic, msg):
    with client.topics[topic].get_sync_producer(linger_ms=0) as producer:
        producer.produce(request.base_url.encode('utf-8'))



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    client = get_client()
    start = time.time()
    publish(client, VIEW_TOPIC, path)
    elapsed = time.time() - start

    r = redis.Redis(host='redis')

    recent = r.zrange(RECENT_KEY, 0, 10, desc=True, withscores=True)
    top = r.zrange(TOP_KEY, 0, 10, desc=True, withscores=True)

    now = datetime.datetime.now()           
    return render_template('index.html', path=path, recent=recent, top=top, elapsed=elapsed, now=now)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
