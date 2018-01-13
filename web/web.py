from flask import Flask
from pykafka import KafkaClient
from pykafka.protocol import CreateTopicRequest


app = Flask(__name__)


def create_topic(client, names):
    topics = [CreateTopicRequest(name, 1, 1, [], []) for name in names]
    broker = list(client.cluster._brokers.values())[0]
    broker.create_topics(topics, 5.0)

@app.route('/')
def hello():
    client = KafkaClient(hosts='kafka:9092')
    app.logger.info(client)
    app.logger.info(client.cluster)
    client.cluster.update()
    app.logger.info(client.cluster._brokers)
    print(client.cluster.controller_broker)
    
    create_topic(client, ["post", "view"])
    return "Hello world!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
