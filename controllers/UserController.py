
from flask import jsonify, request
from flask import current_app as app
from flask_jwt_extended import  jwt_required
from models.User import User
from database import db
from flask import Blueprint
from validators.UserValidator import UserValidator
from marshmallow import ValidationError
from sqlalchemy import or_

user_blueprint = Blueprint('user', __name__)
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
    users = []
    for u in pagination.items:
        users.append(u.to_dict())
    
    data = {
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        },
        'data': users
    }
    
    return jsonify(data)

@user_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get(id):
    return jsonify({"message": f"get do user {id}"})

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
        return jsonify(err.messages), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': 'Ocorreu um erro interno.'}), 400

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
        return jsonify(err.messages), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': 'Ocorreu um erro interno.'}), 400


@user_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def destroy(id):
    
    try:
        registro = User.query.filter_by(id=id).first()
        registro.ativo = False
        db.session.commit()
        
        return jsonify(registro.to_dict()), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': 'Ocorreu um erro interno.'}), 400




