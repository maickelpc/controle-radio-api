from marshmallow import Schema, fields, validate, ValidationError,EXCLUDE

class UserValidator(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=25))
    email = fields.Str(required=True, validate=validate.And(
        validate.Email(), 
        validate.Length(min=4, max=250)
    ))
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    ativo = fields.Bool(required=True)
    perfil = fields.Str(required=True) 
    
    def validate_perfil(self, data, **kwargs):
        if not (data['perfil'] in ['ADMIN', 'VENDEDOR', 'OPERACIONAL', 'FINANCEIRO']):
            raise ValidationError('Perfil inválido')
        return data
    
    # password = fields.Str(required=True, validate=validate.Length(min=6))
    # confirm = fields.Str(required=True)
    # def validate_password(self, data, **kwargs):
    #     if data['password'] != data['confirm']:
    #         raise ValidationError('Passwords must match.')
    #     return data


    class Meta:
        unknown = EXCLUDE

    