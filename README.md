# Apache-kafka
 
## Prerequisites  
 
Before getting started with the Kafka producer and consumer examples, make sure you have the following prerequisites installed:

1. Python: Install Python from the official Python website (https://www.python.org) based on your operating system. Make sure to select the appropriate version for your system.

2. Kafka: Set up a local Kafka cluster using Docker. eYou can find the Docker Compose file at [`./docker-compose.yaml`](https://github.com/Typhoenix/Apache-kafka/blob/main/docker-compose.yaml).

3. `confluent_kafka` Library: Install the `confluent_kafka` library, which provides the Kafka client for Python. Open a terminal or command prompt and run the following command:

   ```bash
   pip install confluent-kafka
   ```

4. `Faker` Library: Install the `Faker` library, which is used to generate fake user data for testing purposes. Run the following command in the terminal or command prompt:

   ```bash
   pip install faker
   ```

## Kafka Producer

The Kafka producer is responsible for generating fake user data and sending it to the Kafka cluster. It utilizes the `confluent_kafka` library and the `Faker` library to create realistic user information.

```python
from confluent_kafka import Producer
from faker import Faker
import json
import time
import logging
import random

fake = Faker()

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

p = Producer({'bootstrap.servers': 'localhost:9092'})
print('Kafka Producer has been initiated...')

def receipt(err, msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

def main():
    for i in range(10):
        data = {
            'user_id': fake.random_int(min=20000, max=100000),
            'user_name': fake.name(),
            'user_address': fake.street_address() + ' | ' + fake.city() + ' | ' + fake.country_code(),
            'platform': random.choice(['Mobile', 'Laptop', 'Tablet']),
            'signup_at': str(fake.date_time_this_month())
        }
        message = json.dumps(data)
        p.poll(1)
        p.produce('user-tracker', message.encode('utf-8'), callback=receipt)
        p.flush()
        time.sleep(3)

if __name__ == '__main__':
    main()
```

## Kafka Consumer

The Kafka consumer reads messages from the `user-tracker` topic and processes them accordingly. It utilizes the `confluent_kafka` library to interact with the Kafka cluster.

```python
from confluent_kafka import Consumer

c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})

print('Available topics to consume:', c.list_topics().topics)

c.subscribe(['user-tracker'])

def main():
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(data)
    c.close()

if __name__ == '__main__':
    main()
```

## Conclusion

In this tutorial, you learned how to set up a local Apache Kafka
