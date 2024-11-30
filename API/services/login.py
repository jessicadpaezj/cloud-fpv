from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from sqlalchemy import and_
from models.model import db_session, User
from flask.views import MethodView

class LogIn(MethodView):

    def post(self):
        user = db_session.query(User).filter(User.email == request.json["email"],
                                             User.password == request.json["password"]).first()
        if user is None:
            return "Check the data entered", 404
        token_de_acceso = create_access_token(identity=user.id)
        return {"token": token_de_acceso}
