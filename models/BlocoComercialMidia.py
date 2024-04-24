from database import db
from datetime import datetime

class BlocoComercialMidia(db.Model):
    __tablename__ = 'blocos_comercial_midia'

    id = db.Column(db.Integer, primary_key=True)
    midia_id = db.Column(db.Integer, db.ForeignKey('midias.id'), primary_key=True)
    blocoComercial_id = db.Column(db.Integer, db.ForeignKey('blocos_comerciais.id'), primary_key=True)
    ordem = db.Column(db.Integer, nullable=False)  

    midia = db.relationship('Midia', backref=db.backref('midias', lazy='dynamic'))
    blocoComercial = db.relationship('BlocoComercial', backref=db.backref('midias', lazy='dynamic'))
