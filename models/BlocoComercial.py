from database import db
from datetime import datetime

class BlocoComercial(db.Model):
    __tablename__ = 'blocos_comerciais'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    dias_semana = db.Column(db.String(200), nullable=False)
    horario = db.Column(db.String(10), nullable=False)
    nome_arquivo_fisico = db.Column(db.String(250))
    
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    
        
    def __repr__(self):
        return f'<BlocoComercial {self.nome}>'
