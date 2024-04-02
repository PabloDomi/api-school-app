from src.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    surnames = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False)
    access_token = db.Column(db.String, unique = True, nullable = False)
    password_token = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = False)
    rol = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable = False)

    subjects = db.relationship("Subject", back_populates = "teacher")

class StudentTeacherRelation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_student = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    id_teacher = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    id_subject = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable = False)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    subject_name = db.Column(db.String(50), unique = True)
    id_teacher = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_students = db.Column(db.ARRAY(db.Integer))

    teacher = db.relationship("User", back_populates = "subjects")

    # Método para agregar relaciones automáticamente
    def add_student_teacher_relations(self):
        if self.id_students:
            if isinstance(self.id_students, list):
                students_ids = self.id_students
            else:
                students_ids = [int(student_id) for student_id in self.id_students.split(',')]
            for student_id in students_ids:
                student_teacher_relation = StudentTeacherRelation(id_student=student_id, id_teacher=self.id_teacher, id_subject=self.id)
                db.session.add(student_teacher_relation)
        db.session.commit()

        # Después de insertar una fila en Subject
        # subject = Subject.query.get(id_nuevo_subject)
        # subject.add_student_teacher_relations()


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    role_name = db.Column(db.String(50), unique = True, nullable = False)


class User_logins(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    signed_in = db.Column(db.DateTime, default=datetime.now)


#### Ejemplo de inserción de datos

# role1 = Role(id=1, role_name='estudiante')
# role2 = Role(id=2, role_name='profesor')
# user1 = User(username='student1', name='Juan', surenames='Pérez', email='student1@example.com', role_id=1)
# user2 = User(username='teacher1', name='Pedro', surenames='González', email='teacher1@example.com', role_id=2)
# session.add_all([role1, role2, user1, user2])
# session.commit()

# session.close()

####
