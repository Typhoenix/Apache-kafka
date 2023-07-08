from confluent_kafka import Producer  # Import the Producer class from confluent_kafka module
from faker import Faker  # Import the Faker module for generating fake data
import json  # Import the json module for working with JSON data
import time  # Import the time module for adding delays
import logging  # Import the logging module for logging messages
import random  # Import the random module for generating random values

fake = Faker()  # Create an instance of the Faker class for generating fake data

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')
# Configure the logging module to log messages with a specific format and write them to a file

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create a logger object and set its log level to INFO

####################
p = Producer({'bootstrap.servers': 'localhost:9092'})
# Create a new Producer instance with the specified bootstrap servers and assign it to variable 'p'
# The bootstrap servers specify the Kafka broker addresses

print('Kafka Producer has been initiated...')  # Print a message indicating that the Kafka Producer has been initiated

#####################
def receipt(err, msg):
    if err is not None:
        print('Error: {}'.format(err))  # If there is an error in producing the message, print the error message
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)  # Log the produced message with the topic and value
        print(message)  # Print the produced message

#####################
def main():
    for i in range(10):  # Repeat the following steps 10 times
        data = {
            'user_id': fake.random_int(min=20000, max=100000),  # Generate a random user ID
            'user_name': fake.name(),  # Generate a fake user name
            'user_address': fake.street_address() + ' | ' + fake.city() + ' | ' + fake.country_code(),  # Generate a fake user address
            'platform': random.choice(['Mobile', 'Laptop', 'Tablet']),  # Choose a random platform from the given options
            'signup_at': str(fake.date_time_this_month())  # Generate a fake sign-up date and time for this month
        }
        m = json.dumps(data)  # Convert the data dictionary to a JSON string
        p.poll(1)  # Poll the producer for events with a timeout of 1 second
        p.produce('user-tracker', m.encode('utf-8'), callback=receipt)
        # Produce a message to the 'user-tracker' topic with the JSON string as the value and the receipt callback function
        p.flush()  # Wait for any outstanding messages to be delivered
        time.sleep(3)  # Add a delay of 3 seconds before sending the next message

if __name__ == '__main__':
    main()  # Call the main function if the script is run directly as the main program