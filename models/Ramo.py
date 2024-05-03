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
    
    def to_dict(self):
        # Cria um dicionário com todos os campos, exceto 'password_hash'
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password_hash'}
