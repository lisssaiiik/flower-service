import json
import pika
from rabbit.config import settings
from rabbit.tasks import send_done_order_confirmation_email
def callback(ch, method, properties, body):
    message = json.loads(body)
    send_done_order_confirmation_email(message['order_id'],
                                    message['total_cost'],
                                    message['email'])
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=settings.DONE_QUEUE_NAME)
channel.basic_consume(queue=settings.DONE_QUEUE_NAME, on_message_callback=callback)
print("Брокер ожидает сообщений")
channel.start_consuming()