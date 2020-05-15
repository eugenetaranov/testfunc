from kafka import KafkaProducer
from os import getenv

def handle(req):
    kafka_host = getenv("KAFKA_HOST")
    kafka_port = getenv("KAFKA_PORT")
    kafka_topic = getenv("KAFKA_TOPIC")

    producer = KafkaProducer(
        bootstrap_servers=[f"{kafka_host}:{kafka_port}"],
        value_serializer=lambda x: x.encode("utf-8"),
    )
    producer.send(topic=kafka_topic, value=req)
    producer.close()

    return