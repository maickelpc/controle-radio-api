from database import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200))
    nome = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    perfil = db.Column(Enum('ADMIN', 'VENDEDOR', 'OPERACIONAL', 'FINANCEIRO', name='perfil_types'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.id} : {self.nome}"

    def to_dict(self):
        # Cria um dicionário com todos os campos, exceto 'password_hash'
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password_hash'}

