import json
from flask import app, jsonify, request
from flask_jwt_extended import create_access_token, current_user, decode_token, jwt_required
from flask_restful import Resource
from sqlalchemy import and_, asc, desc
from models.model import VideoSchema, db_session,  Video
import datetime
# from celery import Celery
from flask.views import MethodView

from google.cloud import pubsub_v1

# Set your Google Cloud Project ID
project_id = "proyecto-fpv-idrl"
# Set the Pub/Sub topic name you created
topic_name = "video"

# Create a PublisherClient
publisher = pubsub_v1.PublisherClient()
# Create the topic path
topic_path = publisher.topic_path(project_id, topic_name)

class Task(MethodView):
    @jwt_required()
    def get(self):
        # Get query parameters
        max_results = request.json["max"]
        order = request.json["order"]
      
        user_id =current_user.id
       
       
        if order ==1:
            tasks = db_session.query(Video).filter(Video.user_id == user_id).order_by(desc(Video.id))[:max_results]
        else:
            tasks = db_session.query(Video).filter(Video.user_id == user_id).order_by(asc(Video.id))[:max_results]

        # Return tasks as JSON
        video_schema = VideoSchema()
        return video_schema.dump(tasks, many=True)

    @jwt_required()
    def post(self):
        file_name = request.json["filename"]
        # Create a variable with the current date and time
        timestamp = datetime.datetime.now()
        user_id =current_user.id
        video = Video(name="video_dron",time_stamp=timestamp,path_folder=file_name,status="uploaded",user_id=user_id)
        db_session.add(video)
        db_session.commit()
        #logica cola
        
        message_data=[video.id, video.path_folder]
        # Convert all items to strings
        message_data = [str(item) for item in message_data]
        # Data should be in bytes
        message_string = '\n'.join(message_data)
        message_bytes = message_string.encode("utf-8")
        # Publish the message
        future = publisher.publish(topic_path, data=message_bytes)
        # Wait for the message to be published
        future.result()
        print(f"Published message to {topic_path}.")
        return  {"message": "Task created successfully"}

