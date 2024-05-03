
from flask import jsonify, request
from flask import current_app as app
from flask_jwt_extended import  jwt_required
from models.Ramo import Ramo
from database import db
from flask import Blueprint
from validators.RamoValidator import RamoValidator
from marshmallow import ValidationError
from sqlalchemy import or_
from exceptions.BusinessException import BusinessException
# from flask_cors import CORS

ramo_blueprint = Blueprint('ramos', __name__)
page_default = '1'
per_page_default = '20'

# Configurar CORS para aceitar todos os origins e permitir o cabeçalho Authorization
# CORS(ramo_blueprint, methods=['GET', 'POST', 'OPTIONS','DELETE','PUT'], allow_headers=["Authorization", "Content-Type","Accept"], supports_credentials=True, origins="*")


@ramo_blueprint.route('/', methods=['GET'])
@jwt_required()
def index():
    page = int(request.args.get('page', default=page_default))
    per_page = int(request.args.get('per_page', default=per_page_default))
    pagination = Ramo.query
    if request.args.get('texto', default=False):
        pagination = pagination.filter(or_(
            Ramo.nome.ilike( '%' + request.args.get('texto') + '%'),
            Ramo.descricao.ilike( '%' + request.args.get('texto') + '%')
        ))
  
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



@ramo_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get(id):
    try:
        registro = Ramo.query.filter_by(id=id).first()
        return jsonify(registro.to_dict()), 200
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400



@ramo_blueprint.route('/', methods=['POST'])
@jwt_required()
def store():
    validator = RamoValidator()
    try:
        data = validator.load(request.json)
        registro = Ramo.query.filter(Ramo.nome.ilike( data["nome"])).first()
        if registro != None:
            
            raise BusinessException(f"O nome {data['nome']} ja está em uso.")
        registro = Ramo(**data)  # Adapte os campos conforme necessário
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



@ramo_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    validator = RamoValidator()
    try:
        data = validator.load(request.json)
        registro = Ramo.query.filter(
            Ramo.nome.ilike( data["nome"]),
            Ramo.id != id
        ).first()
        if registro != None:
            
            raise BusinessException(f"O nome {data['nome']} ja está em uso.")
        
        registro = Ramo.query.filter_by(id=id).first()
        data.pop('id',None)
        data.pop('data_criacao',None)
        for key, value in data.items():
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



@ramo_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def destroy(id):
    
    try:
        registro = Ramo.query.filter_by(id=id).first()
        db.session.delete(registro)
        db.session.commit()
        
        return jsonify(registro.to_dict()), 200
    
    except BusinessException as err:
        return jsonify({'erro': str(err)}), 400
    except Exception as err:
        app.logger.info(err)
        return jsonify({'erro': "Ocorreu um erro interno no sistema"}), 400




