from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from sqlalchemy import and_
from models.model import db_session, User
from flask.views import MethodView

class SingUp(MethodView):

    def post(self):
        if request.json["password1"] != request.json["password2"]:
            return "The password are not equal",  406
        user = db_session.query(User).filter(User.email == request.json["email"]).first()
        if user:
            return "The email is already registered",  406
        new_user = User(username = request.json["username"],
                        password = request.json["password1"],
                        email = request.json["email"])
        db_session.add(new_user)
        db_session.commit()
        return {"message": "Account created successfully"}, 200
