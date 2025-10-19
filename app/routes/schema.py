from marshmallow import fields, Schema


class UserSchema(Schema):
    uid = fields.Int()
    firstname = fields.Str()
    lastname = fields.Str()
    username = fields.Str()
    email = fields.Str()


class AuthorSchema(Schema):
    firstname = fields.Str()
    lastname = fields.Str()


class PostSchema(Schema):
    pid = fields.Int()
    title = fields.Str()
    body = fields.Str()
    created_at = fields.DateTime()
    author = fields.Nested(AuthorSchema)