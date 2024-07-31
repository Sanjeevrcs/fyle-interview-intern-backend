from flask import Blueprint
from marshmallow import ValidationError
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, GradeEnum
from flask import jsonify, make_response

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(
        teacher_id=p.teacher_id
    )
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    try:
        # if incoming_payload["grade"] not in [
        #     GradeEnum.A,
        #     GradeEnum.B,
        #     GradeEnum.C,
        #     GradeEnum.D,
        # ]:
        #     raise ValidationError(
        #         status_code=400, message="Grade should be one of A, B, C, D, E"
        #     )

        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

        assignment = Assignment.get_by_id(grade_assignment_payload.id)
        if assignment is None:
            raise FyleError(status_code=404, message="Assignment not found")
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p,
        )

        db.session.commit()

        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

        response = jsonify({"data": graded_assignment_dump})
        response = make_response(response, 200)
        return response

    except ValidationError as e:
        raise FyleError(status_code=400, message=e.messages)
