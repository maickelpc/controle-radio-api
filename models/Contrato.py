from database import db
from datetime import datetime
from sqlalchemy import Enum

class Contrato(db.Model):
    __tablename__ = 'contratos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    ramo_id = db.Column(db.Integer, db.ForeignKey('ramos.id'), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    
    valor_total = db.Column(db.Numeric(10, 2), nullable=False) 
    valor_mensal = db.Column(db.Numeric(10, 2), nullable=False)
    
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    data_cancelamento = db.Column(db.DateTime)
    observacao_cancelamento = db.Column(db.String(250))
    
    status = db.Column(Enum('ATIVO', 'ENCERRADO', 'CANCELADO', name='status_types'), default='ATIVO', nullable=False)
    
    cliente = db.relationship('Cliente', backref=db.backref('contratos', lazy=True))
    ramo = db.relationship('Ramo', backref=db.backref('contratos', lazy=True))
    

    
    def __repr__(self):
        return f'<Contrato {self.nome}>'
