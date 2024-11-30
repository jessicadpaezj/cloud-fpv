from google.cloud import pubsub_v1
import time

from process_video import process_video

project_id = "proyecto-fpv-idrl"
subscription_id = "video-sub"
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message.data}.")
    video = message.data.decode("utf-8")
    parts_video = video.split("\n")
    process_video(int(parts_video[0]), parts_video[1])
    message.ack()
    
while True:
    streaming_pull_future = subscriber.subscribe(subscription_path, callback = callback)
    print(f"Listening for messages on {subscription_path}..\n")
    time.sleep(300)
    with subscriber:
        try:
            streaming_pull_future.result(timeout = timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()