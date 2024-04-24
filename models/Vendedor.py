from database import db
from datetime import datetime


class Vendedor(db.Model):
    __tablename__ = 'vendedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    apelido = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(20), unique=True)
    fone = db.Column(db.String(50))
    email = db.Column(db.String(250))
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(150))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    pais = db.Column(db.String(50))
    complemento = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    
    

    def __repr__(self):
        return f'<Vendedor {self.apelido}>'
