from database import db
from datetime import datetime
from sqlalchemy import Enum

class Midia(db.Model):
    __tablename__ = 'midias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False, unique=True)
    descricao = db.Column(db.String(200))
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    voz_id = db.Column(db.Integer, db.ForeignKey('vozes.id'), nullable=False)
    
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)    
    data_criacao = db.Column(db.DateTime, default=datetime.now())
        
    contrato = db.relationship('Contrato', backref=db.backref('midias', lazy=True))
    voz = db.relationship('Voz', backref=db.backref('midias', lazy=True))
    ativo = db.Column(db.Boolean, default=True)  
    
    #Adicionar os Blocos
    
    def __repr__(self):
        return f'<midia {self.nome}>'
