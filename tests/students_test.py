from core.models.assignments import Assignment, AssignmentStateEnum


def test_get_assignments_student_1(client, h_student_1):
    response = client.get("/student/assignments", headers=h_student_1)
    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = "ABCD TESTPOST"
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    from core import db

    assignment = Assignment.get_by_id(1)
    assignment.state = AssignmentStateEnum.DRAFT
    assignment.teacher_id = 2
    db.session.commit()

    response = client.post(
        "/student/assignments/submit",
        headers=h_student_1,
        json={"id": 1, "teacher_id": 2},
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 1
    assert data["state"] == "SUBMITTED"
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):

    from core import db

    assignment = Assignment.get_by_id(2)
    assignment.state = AssignmentStateEnum.SUBMITTED

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "ValidationError"
    assert "only a draft assignment can be submitted" in error_response["message"]


def test_update_assignment_error(client, h_student_1):
    """
    failure case: only a valid assignment can be updated
    """
    response = client.post(
        "/student/assignments",
        headers=h_student_1,
        json={"id": 100000, "content": "ABCD"},
    )

    assert response.status_code == 404
    error_response = response.json
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "No assignment with this id was found"


def test_update_assignment_draft(client, h_student_1):

    from core import db

    assignment = Assignment.get_by_id(2)
    assignment.state = AssignmentStateEnum.SUBMITTED
    db.session.commit()

    response = client.post(
        "/student/assignments",
        headers=h_student_1,
        json={"id": 2, "content": "ABCD"},
    )

    assert response.status_code == 400
    error_response = response.json
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "only assignment in draft state can be edited"


def test_update_assignment_without_content(client, h_student_1):

    from core import db

    assignment = Assignment.get_by_id(1)
    assignment.state = AssignmentStateEnum.DRAFT
    db.session.commit()

    response = client.post(
        "/student/assignments",
        headers=h_student_1,
        json={"id": 1, "content": None},
    )

    assert response.status_code == 400
    error_response = response.json
    assert error_response["error"] == "ValidationError"
    assert "Assignment content cannot be empty" in error_response["message"]
