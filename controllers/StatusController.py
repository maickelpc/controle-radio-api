
from flask import jsonify, request
from flask import current_app as app
import os
import subprocess

from flask import Blueprint

status_blueprint = Blueprint('api', __name__)


@status_blueprint.route('/status', methods=['GET'])
def status():
    app.logger.info("Executando alguma função específica de Cliente")
    return jsonify({"message": "Hello, World!"})

@status_blueprint.route('/reiniciar', methods=['GET'])
def reiniciar():
    subprocess.run(["reiniciar.bat"], shell=True)

@status_blueprint.route('/sair', methods=['GET'])
def sair():
    os._exit(0)