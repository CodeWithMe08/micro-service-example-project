import pika,json
from main import Product, db 

params = pika.URLParameters('amqps://frufafpl:OvSjyF7gBcuTw3bvGd3OZh8soLyI5FWg@cow.rmq2.cloudamqp.com/frufafpl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main01')

def callback(ch, method, properties, body):
    print('Received in main01')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')

channel.basic_consume(queue='main01', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()