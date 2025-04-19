from google.cloud import pubsub_v1
import json
import time

project_id = "dataeng-s25-personal"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

with open("bcsample.json") as f:
    data = json.load(f)


for record in data:
    message = json.dumps(record).encode("utf-8")
    future = publisher.publish(topic_path, message)
    #print(f"Published message ID: {future.result()}")
    #time.sleep(0.1)  # Optional: slow down for demo/testing


print(f"\nNumber of records sent: {len(data)}")