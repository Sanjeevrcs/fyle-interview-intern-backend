from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core.models.principals import Principal
from core.models.teachers import Teacher


def test_request_headers(client, h_principal):
    response = client.get("/principal/assignments", headers="")

    assert response.status_code == 401


def test_get_assignments(client, h_principal):
    response = client.get("/principal/assignments", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["state"] in [
            AssignmentStateEnum.SUBMITTED,
            AssignmentStateEnum.GRADED,
            AssignmentStateEnum.DRAFT,
        ]


def test_grade_assignment_draft_assignment(client, h_principal):

    from core import db

    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """

    assignemnt = Assignment.get_by_id(2)
    assignemnt.state = AssignmentStateEnum.DRAFT
    db.session.commit()
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 2, "grade": GradeEnum.A.value},
        headers=h_principal,
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):

    from core import db

    assignment = Assignment.get_by_id(1)
    assignment.state = AssignmentStateEnum.SUBMITTED
    db.session.commit()

    response = client.post(
        "/principal/assignments/grade",
        json={"id": 1, "grade": GradeEnum.C.value},
        headers=h_principal,
    )
    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):

    response = client.post(
        "/principal/assignments/grade",
        json={"id": 1, "grade": GradeEnum.A.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.A


def test_get_all_principals():

    principals = Principal.get_all_principals()
    assert principals is not None
    assert Principal.get_by_id(principals[0].id) is not None


def test_get_all_teachers(client, h_principal):

    response = client.get("/principal/teachers", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for teacher in data:
        assert Teacher.get_by_id(teacher["id"]) is not None

    assert len(data) == len(Teacher.get_all_teachers())


def test_invalid_api(client, h_principal):

    response = client.get("/invalid_url/")
    assert response.status_code == 404
