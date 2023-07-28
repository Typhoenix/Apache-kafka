from confluent_kafka import Consumer  # Import the Consumer class from confluent_kafka module

################

c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
# Create a new Consumer instance with the specified configuration parameters and assign it to variable 'c'
# Parameters include bootstrap servers, consumer group ID, and auto offset reset policy

print('Available topics to consume: ', c.list_topics().topics)  # Print the list of available topics to consume

c.subscribe(['user-tracker'])  # Subscribe the consumer to the 'user-tracker' topic 

################

def main():  # Define the main function
    while True:  # Start an infinite loop
        msg = c.poll(1.0)  # Poll for the next message with a timeout of 1.0 second
        if msg is None:  # If no message is retrieved, continue to the next iteration
            continue
        if msg.error():  # If there is an error in the message, print the error message and continue to the next iteration
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')  # Decode the message value from bytes to a string
        print(data)  # Print the message data
    c.close()  # Close the consumer connection

if __name__ == '__main__':  # If the script is run directly as the main program
    main()  # Call the main function to start consuming messages from the Kafka topic
