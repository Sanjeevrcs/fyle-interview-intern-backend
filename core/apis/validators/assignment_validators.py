from marshmallow import ValidationError
from core.libs import assertions
from core.libs.exceptions import FyleError
from core.models.principals import Principal


def validate_content(assignment):
    if not assignment.content:
        raise ValidationError(
            message="Assignment content cannot be empty", status_code=400
        )


def validate_grade_for_draft(assignment):

    from core.models.assignments import AssignmentStateEnum

    if assignment.state == AssignmentStateEnum.DRAFT:
        raise ValidationError(
            message="Draft assignment cannot have a grade", status_code=400
        )


def validate_already_submitted(assignment):

    from core.models.assignments import AssignmentStateEnum

    if assignment.state != AssignmentStateEnum.DRAFT:
        raise ValidationError(
            message="only a draft assignment can be submitted", status_code=400
        )


# validate grade assignment by teacher and allow if user is principal
def validate_grade_assignment_by_teacher(assignment, auth_principal):

    from core.models.assignments import AssignmentStateEnum

    # Check if the principal is a principal
    is_principal = (
        Principal.query.filter_by(user_id=auth_principal.user_id).first() is not None
    )

    if not is_principal and assignment.teacher_id != auth_principal.teacher_id:
        raise FyleError(
            message="Only the teacher who created the assignment can grade it",
            status_code=400,
        )


def validate_grade_choice(grade):

    from core.models.assignments import GradeEnum

    if grade not in [GradeEnum.A, GradeEnum.B, GradeEnum.C, GradeEnum.D]:
        raise ValidationError(
            message="Grade should be one of A, B, C, D", status_code=400
        )
