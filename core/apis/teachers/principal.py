from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import TeacherSchema
from core.libs import assertions

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    
    teachers = Teacher.query.all()
    teacher_schema = TeacherSchema(many=True)
    teachers_dump = teacher_schema.dump(teachers)
    return APIResponse.respond(data=teachers_dump)
