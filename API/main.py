from asyncio import Task
from services.login import LogIn
from services.sing_up import SingUp
from services.task import Task
from services.task_id import TaskId
from flask import Flask, render_template, request
from flask_jwt_extended import JWTManager, decode_token
from flask_restful import Api
from typing import Any, List
from flask import jsonify
from models.model import db, engine,User,db_session
import os

def add_urls(app):
    api = Api(app)
    # api.add_resource(LogIn, '/auth/login')
    # api.add_resource(SingUp, '/auth/signup')
    # api.add_resource(Task, '/task')
    # api.add_resource(Task_Id, '/task/<int:id_task>') 
    app.add_url_rule('/auth/login', view_func=LogIn.as_view('login'))
    app.add_url_rule('/auth/signup', view_func=SingUp.as_view('signup'))
    app.add_url_rule('/task', view_func=Task.as_view('task'))
    app.add_url_rule('/task/<int:id_task>', view_func=TaskId.as_view('taskid'))

def create_flask_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app_context = app.app_context()
    app_context.push()
    add_urls(app)
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db_session.query(User).filter(User.id==identity).first()
    
    return app

app =  create_flask_app()
db.metadata.create_all(engine)

# @app.route("/auth/login", methods=["POST"])
# def index():
#     login_service = LogIn()
#     return login_service.post(request)

# if __name__ == '__main__':
#   app =  create_flask_app()
#   db.metadata.create_all(engine)
#   app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
# gcloud builds submit --tag us-central1-docker.pkg.dev/master-cloud-420017/fpv-cloud/api
# gcloud run deploy api --image us-central1-docker.pkg.dev/master-cloud-420017/fpv-cloud/api
