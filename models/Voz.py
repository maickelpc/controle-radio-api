from database import db
from datetime import datetime

class Voz(db.Model):
    __tablename__ = 'vozes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Voz {self.nome}>'

    def to_dict(self):
        # Cria um dicionário com todos os campos, exceto 'password_hash'
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password_hash'}