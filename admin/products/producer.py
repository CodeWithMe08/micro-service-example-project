import json
import pika

params = pika.URLParameters('amqps://frufafpl:OvSjyF7gBcuTw3bvGd3OZh8soLyI5FWg@cow.rmq2.cloudamqp.com/frufafpl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main01', body=json.dumps(body), properties= properties)
