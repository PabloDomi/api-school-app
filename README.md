# API para app school

CRUD school management example API built with Python Flask-RestX and SQLAlchemy.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

You only have to create a `.env` file in the `src` directory with the following data:

- `SQLALCHEMY_DATABASE_URI_DEV = 'postgresql://user:password@localhost/mydatabase'`
- `SQLALCHEMY_TRACK_MODIFICATIONS = '(usually FALSE)'`
- `JWT_SECRET_KEY = 'SECRET-KEY-FOR-JWT-AUTH'`
- `TEACHER_TOKEN = 'TOKEN-FOR-TEACHER-LOGIN-IN-APP'`

After that, you have to run these commands:

```bash
python -m venv env --------------> CREAR EL VIRTUAL ENVIRONMENT
Source env/Scripts/Activate --------------> ACTIVAR EL VIRTUAL ENVIRONMENT (SI AUN NO LO HAS EJECUTADO)
pip install -r requirements.txt ----------> PARA INSTALAR DEPENDENCIAS DEL REQUIREMENTS.TXT


flask db init  # Create instance and migrations folders
flask db migrate -m "initial commit"  # Creates the `database.db` file in the `instance` folder
flask db upgrade  # Creates the user tables and other tables based on the schema specified in the models in the db specified before
```

## Usage

Run these commands to initiate the API:
```bash
    Source env/Scripts/Activate --------------> ACTIVAR EL VIRTUAL ENVIRONMENT (SI AUN NO LO HAS EJECUTADO)
    flask run --------------------------------> PARA LANZAR LA API
```


~ Mas información de como se creó esta estructura de carpetas: [Folder Structure](https://ashleyalexjacob.medium.com/flask-api-folder-guide-2023-6fd56fe38c00)