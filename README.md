# API para app school

A brief description of your project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

You only have to create a `.env` file in the `src` directory with the following data:

- `SQLALCHEMY_DATABASE_URI_DEV = ''`
- `SQLALCHEMY_TRACK_MODIFICATIONS = ''`
- `JWT_SECRET_KEY = ''`
- `TEACHER_TOKEN = ''`

After that, you have to run these commands:

```bash
flask db init  # Create instance and migrations folders
flask db migrate -m "initial commit"  # Creates the `database.db` file in the `instance` folder
flask db upgrade  # Creates the user tables and other tables based on the schema specified in the models in the db specified before
```

## Usage

run these commands:
```bash
    python -m venv env --------------> CREAR EL VIRTUAL ENVIRONMENT
    Source env/Scripts/Activate --------------> ACTIVAR EL VIRTUAL ENVIRONMENT
    pip install -r requirements.txt ----------> PARA INSTALAR DEPENDENCIAS DEL REQUIREMENTS.TXT
    flask run --------------------------------> PARA LANZAR LA API
```


~ Mas información de como se creó esta estructura de carpetas: [Folder Structure](https://ashleyalexjacob.medium.com/flask-api-folder-guide-2023-6fd56fe38c00)