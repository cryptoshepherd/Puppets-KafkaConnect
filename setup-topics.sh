#!/bin/bash

echo "Creating quickstart-avro-offsets"
docker exec broker1 kafka-topics --create --topic quickstart-avro-offsets --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092 --if-not-exists --config cleanup.policy=compact
echo "Creating quickstart-avro-config"
docker exec broker1 kafka-topics --create --topic quickstart-avro-config --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092 --if-not-exists --config cleanup.policy=compact
echo "Creating quickstart-avro-status"
docker exec broker1 kafka-topics --create --topic quickstart-avro-status --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092 --if-not-exists --config cleanup.policy=compact
