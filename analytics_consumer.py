import pika
from pika.exchange_type import ExchangeType


def on_message_received(ch, method, properties, body):
    print(f"Analytics Service received: {body}")
   

connection_parameters = pika.ConnectionParameters('13.214.190.7')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="routing", exchange_type=ExchangeType.direct)

queue = channel.queue_declare(queue="", exclusive=True)
channel.queue_bind(exchange="routing", queue=queue.method.queue, routing_key="analytics")

channel.basic_consume(queue=queue.method.queue, auto_ack=True,
    on_message_callback=on_message_received)

print('Starting Consuming')

channel.start_consuming()