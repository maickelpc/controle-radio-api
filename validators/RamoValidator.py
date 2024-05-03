from marshmallow import Schema, fields, validate, EXCLUDE

class RamoValidator(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    descricao = fields.Str( validate=validate.Length( max=250))
    
    class Meta:
        unknown = EXCLUDE
