from flask import Flask
from flask_cors import CORS
from waitress import serve
import threading
import logging
from database import db
import os
import importlib
from flask_jwt_extended import JWTManager
from config import ProductionConfig
from controllers.StatusController import status_blueprint
from controllers.AuthController import auth_blueprint
from controllers.UserController import user_blueprint
from controllers.VozController import voz_blueprint

app = Flask(__name__)
app.config['DEBUG'] = True  # Ativa o modo debug e o reloading automático
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Deve ser uma chave segura e única

CORS(app)

### Configuracao do log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)



## Configuração de Banco de Dados
app.config.from_object(ProductionConfig)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_do_meu_pau.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db.init_app(app)

models_path = os.path.join(os.path.dirname(__file__), 'models')
for filename in os.listdir(models_path):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]  # remove a extensão .py
        importlib.import_module(f'models.{module_name}')

with app.app_context():
    db.create_all()

### Registro de Rotas

jwt = JWTManager(app)


app.register_blueprint(auth_blueprint, url_prefix='/auth')

app.register_blueprint(status_blueprint, url_prefix='/status')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(voz_blueprint, url_prefix='/vozes')



def run_api():
    port = 9000 #get_environment_setting('Porta')
    serve(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    app.logger.info("Iniciando o servidor da API...")
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    app.logger.info("O servidor da API está rodando. Acesse http://localhost:5000/api para testar.")
    api_thread.join()  # Isso irá esperar a thread da API terminar, o que só aconteceria se o servidor fosse interrompido.
