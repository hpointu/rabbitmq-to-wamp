import time
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()
channel.queue_declare(queue='xsource')

i = 1
while True:
    channel.basic_publish(
        exchange='',
        routing_key='xsource',
        body='something-%03d' % i
    )
    i += 1
    time.sleep(1)
