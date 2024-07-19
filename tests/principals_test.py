from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_grade_non_existent_assignment(client, h_principal):
    """
    failure case: If an assignment does not exist, it cannot be graded
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 100,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'


def test_grade_invalid_grade(client, h_principal):
    """
    failure case: Invalid grade should not be accepted
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'Z'
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'


def test_grade_assignment_with_empty_grade(client, h_principal):
    """
    failure case: Grade cannot be empty
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': None
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'


#Adding new tests
def test_list_teachers(client, h_principal):
    """
    Test case for listing all teachers as a principal
    """
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    print(response.status_code)
    print(response.data)

    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)
    for teacher in data:
        assert 'id' in teacher
        assert 'created_at' in teacher
        assert 'updated_at' in teacher
        assert 'user_id' in teacher


def test_get_teachers_non_principal(client, h_student_1):
    """
    Test failure case: User is not a principal
    """
    response = client.get(
        '/principal/teachers',
        headers=h_student_1
    )

    assert response.status_code == 403
    assert response.json['message'] == 'requester should be a principal'

def test_get_teachers_as_student(client, h_student_1):
    """
    Test failure case: User is a student
    """
    response = client.get(
        '/principal/teachers',
        headers=h_student_1
    )

    assert response.status_code == 403
    assert response.json['message'] == 'requester should be a principal'


def test_get_teachers_as_teacher(client, h_teacher_1):
    """
    Test failure case: User is a teacher
    """
    response = client.get(
        '/principal/teachers',
        headers=h_teacher_1
    )

    assert response.status_code == 403
    assert response.json['message'] == 'requester should be a principal'
