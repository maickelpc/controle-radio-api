from marshmallow import Schema, fields, validate

class VozValidator(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=4, max=25))
    descricao = fields.Str(required=True, validate=validate.Length(min=4, max=25))
    