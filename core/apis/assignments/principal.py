from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.apis.teachers.schema import TeacherSchema
from core.models.assignments import Assignment

from .schema import *
from models.teachers import Teacher

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)


# principal_view_all_the_assignments
@principal_assignments_resources.route(
    "/teachers", methods=["GET"], strict_slashes=False
)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""

    teachers = Teacher.get_all_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


# principal_view_all_the_assignments
@principal_assignments_resources.route(
    "/assignments", methods=["GET"], strict_slashes=False
)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""

    teachers_assignments = Assignment.get_assignments_by_teacher()
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)
