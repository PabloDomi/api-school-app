from flask_restx import fields

from src.extensions import api

###
#
#       MODELOS DE DATOS DE LA API, USADOS EN GET, POST, PUT... PARA MODELAR EL TIPO DE DATOS QUE ESPERA UN SERVICIO O QUE DEVUELVE
#
###

subject_input_model = api.model("Subject", {
    "subject_name": fields.String,
    "id_teacher": fields.Integer,
    "id_students": fields.List(fields.Integer)
})

subject_model = api.model("SubjectInputs", {
    "id": fields.Integer,
    "subject_name": fields.String,
    "id_teacher": fields.Integer,
    "id_students": fields.List(fields.Integer)
})


register_model_student = api.model("RegisterModel", {
    "username": fields.String,
    "name": fields.String,
    "surnames": fields.String,
    "password": fields.String,
    "email": fields.String,
    "rol": fields.Integer
})

register_model_teacher = api.model("RegisterModel", {
    "username": fields.String,
    "name": fields.String,
    "surnames": fields.String,
    "password": fields.String,
    "email": fields.String,
    "rol": fields.Integer,
    "validateToken": fields.String
})

login_model = api.model("LoginModel", {
    "username": fields.String,
    "password": fields.String
})

logged_model = api.model("LoggedModel", {
    "name": fields.String,
    "username": fields.String,
    "access_token": fields.String
})

registered_model = api.model("RegisteredModel", {
    "id": fields.String,
    "username": fields.String
})

check_username_model = api.model("CheckIdModel", {
    "validUsername": fields.Boolean
})

active_input_model = api.model("ActiveInputModel", {
    "username": fields.String
})

active_model = api.model("ActiveModel", {
    "username": fields.String,
    "active": fields.Boolean
})

getEmail_model = api.model("GetEmailModel", {
    "email": fields.String
})

check_email_model = api.model("CheckIdModel", {
    "validEmail": fields.Boolean
})

check_password_model = api.model("CheckPasswordModel", {
    "samePassword": fields.Boolean
})

change_password_forgot_model = api.model("ChangePasswordModel", {
    "username": fields.String,
    "password": fields.String,
    "password_token": fields.String
})

change_password_model = api.model("ChangePasswordModel", {
    "username": fields.String,
    "password": fields.String,
})

password_token_model = api.model("PasswordTokenModel", {
    "password_token": fields.String
})

send_email_model = api.model("PasswordTokenModel", {
    "sended": fields.Boolean
})