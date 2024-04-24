from database import db
from datetime import datetime

class ContratoVendedor(db.Model):
    __tablename__ = 'contrato_vendedor'

    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'), primary_key=True)
    comissao = db.Column(db.Numeric(10, 2), nullable=False)  # Precisão 10, Escala 2

    contrato = db.relationship('Contrato', backref=db.backref('contratos', lazy='dynamic'))
    vendedor = db.relationship('Vendedor', backref=db.backref('contratos', lazy='dynamic'))
