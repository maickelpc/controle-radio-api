
from flask import jsonify, request
from flask import current_app as app
from flask_jwt_extended import  jwt_required, get_jwt_identity
from models.User import User
from database import db
from flask import Blueprint
from validators.UserValidator import UserValidator
from marshmallow import ValidationError
from sqlalchemy import or_
from exceptions.BusinessException import BusinessException
from werkzeug.security import check_password_hash

user_blueprint = Blueprint('users', __name__)
page_default = '1'
per_page_default = '20'


@user_blueprint.route('/', methods=['GET'])
@jwt_required()
def index():
    page = int(request.args.get('page', default=page_default))
    per_page = int(request.args.get('per_page', default=per_page_default))
    pagination = User.query
    if request.args.get('texto', default=False):
        pagination = pagination.filter(or_(
            User.username.ilike( '%' + request.args.get('texto') + '%'),
            User.nome.ilike( '%' + request.args.get('texto') + '%')
        ))
    ativo = request.args.get('ativo', default='TODOS')
    if ativo != 'TODOS':
        if ativo == 'ATIVO':
            pagination = pagination.filter( User.ativo == True)
        if ativo == 'INATIVO':
            pagination = pagination.filter( User.ativo == False)
    
    pagination = pagination.paginate(page=page, per_page=per_page, error_out=False)
    dados = []
    for u in pagination.items:
        dados.append(u.to_dict())
    
    data = {
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        },
        'data': dados
    }
    
    return jsonify(data)



@user_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get(id):
    try:
        registro = User.query.filter_by(id=id).first()
        return jsonify(registro.to_dict()), 200
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400



@user_blueprint.route('/', methods=['POST'])
@jwt_required()
def store():
    validator = UserValidator()
    try:
        data = validator.load(request.json)
        registro = User(**data)  # Adapte os campos conforme necessário
        registro.set_password('trocar123')
        db.session.add(registro)
        db.session.commit()
        
        return jsonify(registro.to_dict()), 200
    except ValidationError as err:
        return jsonify(err.messages), 422
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400



@user_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    validator = UserValidator()
    try:
        data = validator.load(request.json)
        registro = User.query.filter_by(id=id).first()
        for key, value in data.items():
            if(key == 'id'):
                continue
            setattr(registro, key, value)
        db.session.commit()
        
        return jsonify(registro.to_dict()), 200
    except ValidationError as err:
        return jsonify(err.messages), 422
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400



@user_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def destroy(id):
    
    try:
        registro = User.query.filter_by(id=id).first()
        registro.ativo = False
        db.session.commit()
        
        return jsonify(registro.to_dict()), 200
    
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400





@user_blueprint.route('/<int:id>/trocar-senha', methods=['POST'])
@jwt_required()
def trocarSenha(id):
    
    try:
        registro = User.query.filter_by(id=id).first()
        
        if(request.json['new_password'] != request.json['confirm_password']):
            raise BusinessException('As novas senhas digitadas não conferem')
        
        current_user = get_jwt_identity()
        
        if(current_user == id) :
            if not check_password_hash(registro.password_hash, request.json['password']):
                raise BusinessException('Senha Inválida!')
        else:
            current_user = User.query.filter_by(id=current_user).first()
            if(current_user.perfil != 'ADMIN'):
                raise BusinessException('Você não tem permissão para executar esta ação!')
            
        
        registro.set_password(request.json['new_password'])
        db.session.add(registro)
        db.session.commit()
        
        return jsonify(registro.to_dict()), 200
    except ValidationError as err:
        return jsonify(err.messages), 422
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400

