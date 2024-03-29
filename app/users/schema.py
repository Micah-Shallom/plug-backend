from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.String()
    fullname =  fields.String()
    email = fields.String()
    password = fields.String()
    role =  fields.String()