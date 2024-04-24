from database import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    apelido = db.Column(db.String(50), unique=True, nullable=False)
    CNPJ = db.Column(db.String(20), unique=True)
    contato_principal = db.Column(db.String(50))
    contato_principal_fone = db.Column(db.String(50))
    contato_principal_email = db.Column(db.String(250))
    contato_financeiro = db.Column(db.String(50))
    contato_financeiro_fone = db.Column(db.String(50))
    contato_financeiro_email = db.Column(db.String(250))
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
        return f'<Cliente {self.apelido}>'
