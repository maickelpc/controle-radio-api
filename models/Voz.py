from database import db
from datetime import datetime

class Voz(db.Model):
    __tablename__ = 'vozes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Voz {self.nome}>'
