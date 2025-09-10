from flask_sqlalchemy import SQLAlchemy
from __main__ import app
db = SQLAlchemy(app)

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.Integer,unique=True, nullable=False )
    correo = db.Column(db.String(80),unique=True, nullable=False)
    legajo = db.Column(db.Integer, unique=True,nullable=False)
    horas = db.Column(db.Integer,nullable=False)
    funcion = db.Column(db.String(40), nullable=False)
    RegistroHorario = db.relationship('registro_horario', backref='trabajador', cascade="all, delete-orphan")


class registro_horario(db.Model):
    __tablename__ = 'registrohorario'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    HoraEntrada = db.Column(db.Time, nullable=False)
    HoraSalida = db.Column(db.Time, nullable=True)
    dependencia = db.Column(db.String(10))
    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.id')) 

