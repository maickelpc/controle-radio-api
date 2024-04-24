from database import db
from datetime import datetime

class Ramo(db.Model):
    __tablename__ = 'ramos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(250))
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return f'<Ramo {self.nome}>'
