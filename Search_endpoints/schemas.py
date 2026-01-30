from marshmallow import Schema, fields, validate


class BuildingSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    code = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=200))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LecturerSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(validate=validate.Length(max=100))
    department = fields.Str(validate=validate.Length(max=100))
    title = fields.Str(validate=validate.Length(max=50))
    office_room = fields.Str(validate=validate.Length(max=20))
    phone = fields.Str(validate=validate.Length(max=20))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


building_schema = BuildingSchema()
buildings_schema = BuildingSchema(many=True)
lecturer_schema = LecturerSchema()
lecturers_schema = LecturerSchema(many=True)