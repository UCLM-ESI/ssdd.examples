# Launch the Kafka server

$ docker-compose -d

# Produce messages

$ echo "Hello world" | kafkacat -b localhost:9092 -P -t test

# Consume messages

$ kafkacat -b localhost:9092 -C -t test

