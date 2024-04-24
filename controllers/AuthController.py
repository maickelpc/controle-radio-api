from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from models.User import User
from werkzeug.security import check_password_hash
from database import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    check_users()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    print(f"User: {user}")
    if user and check_password_hash(user.password_hash, password):
        # Cria o token de acesso JWT
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Invalid username or password.'}), 401

@auth_blueprint.route('/logout')
def logout():
    # O logout com JWT geralmente requer que o token seja adicionado a uma lista negra
    return jsonify({'message': 'Logged out successfully.'}), 200


@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'Você pode ver isso porque está autenticado!'})


def check_users():
    user_count = User.query.count()
    if(user_count == 0):
        new_user = User(username='maickelpc', nome='Maickel')  # Adapte os campos conforme necessário
        new_user.set_password('teste123')
        db.session.add(new_user)
        db.session.commit()