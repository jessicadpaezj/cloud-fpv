import json
from flask import app, jsonify, request
from flask_jwt_extended import create_access_token, current_user, decode_token, jwt_required
from flask_restful import Resource
from sqlalchemy import and_, asc, desc
from models.model import VideoSchema, db_session,  Video
from flask.views import MethodView

class TaskId(MethodView):
    
    @jwt_required()
    def get(self, id_task: int):
      task = db_session.query(Video).filter(Video.id == id_task).first()
      video_schema = VideoSchema()    
      return video_schema.dump(task)
    
    @jwt_required()
    def delete(self, id_task: int):
        task = db_session.query(Video).filter(Video.id == id_task).first()
        db_session.delete(task)
        db_session.commit()
        return  {"message": "Task deleted successfully"}
   