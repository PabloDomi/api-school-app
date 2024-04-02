from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

from .extensions import db, mail
from flask_mail import Message

from src.models.api_models import password_token_model, change_password_model, change_password_forgot_model, send_email_model
from src.models.api_models import subject_input_model, registered_model, check_username_model, active_model, active_input_model, check_email_model
from src.models.api_models import register_model_student, register_model_teacher, login_model, logged_model, subject_model, getEmail_model, check_password_model

from src.models.models import User, StudentTeacherRelation, Subject, User_logins, Rol

from flask_cors import cross_origin

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace("api", authorizations = authorizations)	


@ns.route("/checkUsername/<string:new_username>")
class CheckUsername(Resource):
    @ns.marshal_with(check_username_model)
    def get(self, new_username):
        usuario = db.session.query(User).filter_by(username = new_username).first()
        if usuario:
            return {'validUsername': True}, 400
        else:
            return {'validUsername': True}, 200

@ns.route("/checkActive/<string:username>")
class CheckActive(Resource):
    @ns.marshal_with(check_username_model)
    def get(self, username):
        usuario = User.query.filter_by(username = username).first()
        if not usuario.active:
            return {'validUsername': False}, 400
        else:
            return {'validUsername': True}, 200

@ns.route("/getEmail/<string:username>")
class getEmail(Resource):
    @ns.marshal_with(getEmail_model)
    def get(self, username):
        usuario = User.query.filter_by(username = username).first()
        if usuario:
            return usuario
        else:
            return "Este usuario no existe", 400

@ns.route("/checkEmailExists/<string:email>")
class checkEmailExists(Resource):
    @ns.marshal_with(check_email_model)
    def get(self, email):
        usuario = User.query.filter_by(email = email).first()
        if usuario and usuario.active :
            return {'validEmail': True}, 200
        else:
            return {'validEmail': False}, 400

@ns.route("/checkSamePassword/<string:password>/<string:username>")
class checkSamePassword(Resource):
    @ns.marshal_with(check_password_model)
    def get(self, password, username):
        usuario = User.query.filter_by(username = username).first()
        if usuario and check_password_hash(usuario.password_token, password):
            return {'samePassword': True}, 200
        else:
            return {'samePassword': False}, 20

@ns.route("/changePasswordForgot")
class changePasswordForgot(Resource):
    @ns.expect(change_password_forgot_model)
    @ns.marshal_with(password_token_model)
    def put(self):
        usuario = User.query.filter_by(username = ns.payload["username"]).first()
        if usuario and check_password_hash(usuario.password_token, ns.payload["password_token"]):
            usuario.password_token = generate_password_hash(ns.payload["password"])

        db.session.commit()

        return usuario

@ns.route("/changePassword")
class changePassword(Resource):
    @ns.expect(change_password_model)
    @ns.marshal_with(password_token_model)
    def put(self):
        usuario = User.query.filter_by(username = ns.payload["username"]).first()
        if usuario:
            usuario.password_token = generate_password_hash(ns.payload["password"])
        else:
            return 400

        db.session.commit()

        return usuario, 200

@ns.route("/getPasswordToken/<string:username>")
class getPasswordToken(Resource):
    @ns.marshal_with(password_token_model)
    def get(self, username):
        usuario = User.query.filter_by(username = username).first()
        if usuario:
            return usuario, 200
        else:
            return 400

@ns.route("/sendEmailToken/<string:password_token>")
class sendEmailToken(Resource):
    @ns.marshal_with(send_email_model)
    def get(self, password_token):
        usuario = User.query.filter_by(password_token = password_token).first()
        if usuario:
            msg = Message('Password Recovery', sender = 'schoolSupport@example.com', recipients = [usuario.email])
            url = 'http://localhost:5173/activateAccount/' + password_token + '/' + usuario.username
            body = f'Hola usuario,\n\nEste es su correo de recuperación de contraseña. Por favor, acceda al siguiente link para obtener su token de recuperacion de contraseña:\n\n{url}'
            msg.body = body
            mail.send(msg)

        return { "sended": True }

@ns.route("/registerStudent")
class RegisterStudent(Resource):

    @ns.expect(register_model_student)
    @ns.marshal_with(registered_model)
    def post(self):

        user = User(username = ns.payload["username"], name = ns.payload["name"], surnames = ns.payload["surnames"], 
                    password_token = generate_password_hash(ns.payload["password"]), email = ns.payload["email"], rol = ns.payload["rol"])

        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route("/registerTeacher")
class RegisterTeacher(Resource):

    @ns.expect(register_model_teacher)
    @ns.marshal_with(registered_model)
    def post(self):

        if (ns.payload["teacher_token"] != os.environ.get("TEACHER_TOKEN")) :
            return "Token de registro inválido", 500
        

        user = User(username = ns.payload["username"], name = ns.payload["name"], surnames = ns.payload["surnames"], 
                    password_token = generate_password_hash(ns.payload["password"]), email = ns.payload["email"], rol = ns.payload["rol"])

        db.session.add(user)
        db.session.commit()
        return user, 201


@ns.route("/updateActive")
class UpdateActive(Resource):

    @ns.expect(active_input_model)
    @ns.marshal_with(active_model)
    def put(self):
        user = User.query.filter_by(username = ns.payload["username"]).first()
        user.active = not user.active
        db.session.commit()

        return user


@ns.route("/login")
class Login(Resource):

    @ns.expect(login_model)
    @ns.marshal_with(logged_model)
    def post(self):
        user = User.query.filter_by(username = ns.payload["username"]).first()
        if not user:
            return {"error": "User does not exists"}, 401
        if not check_password_hash(user.password_token, ns.payload["password"]):
            return {"error": "Incorrect password"}, 401
        
        # actualiza el access_token en la base de datos
        user.access_token = create_access_token(user)
        db.session.commit()

        return user, 201


@ns.route("/subject")
class AddSubject(Resource):
    method_decorators = [jwt_required()]
    
    @ns.doc(security="jsonWebToken")
    @ns.expect(subject_input_model)
    @ns.marshal_with(subject_model)
    def post(self):
        subject = Subject(subject_name = ns.payload["subject_name"], id_teacher = ns.payload["id_teacher"], id_students = ns.payload["id_students"])
        db.session.add(subject)
        db.session.commit()

        subject.add_student_teacher_relations()

        return subject, 201