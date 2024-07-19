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

# def test_list_assignments_no_auth(client):
#     """
#     failure case: Attempting to list assignments without authentication
#     """
#     response = client.get('/principal/assignments')
#     assert response.status_code == 401

# def test_list_all_teachers(client, h_principal):
#     """
#     success case: Principal can list all teachers
#     """
#     response = client.get('/principal/teachers', headers=h_principal)
#     assert response.status_code == 200

# def test_list_all_teachers(client, h_principal):
#     """
#     success case: Principal can list all teachers
#     """
#     response = client.get('/principal/teachers', headers=h_principal)
#     assert response.status_code == 200
#     data = response.json['data']
    

 
# def test_list_teachers_no_auth(client):
#     """
#     failure case: Attempting to list teachers without authentication
#     """
#     response = client.get('/principal/teachers')
#     assert response.status_code == 401


# def test_list_teachers_as_teacher(client, h_teacher_1):
#     """
#     failure case: A teacher should not be able to list all teachers
#     """
#     response = client.get('/principal/teachers', headers=h_teacher_1)
#     assert response.status_code == 403
#     data = response.json
#     assert data['error'] == 'FyleError'


# def test_list_teachers_as_teacher(client, h_teacher_1):
#     """
#     failure case: A teacher should not be able to list all teachers
#     """
#     response = client.get('/principal/teachers', headers=h_teacher_1)
#     assert response.status_code == 403
#     data = response.json
#     assert data['error'] == 'Unauthorized access'


# def test_list_teachers_as_student(client, h_student_1):
#     """
#     failure case: A student should not be able to list all teachers
#     """
#     response = client.get('/principal/teachers', headers=h_student_1)
#     assert response.status_code == 403
#     data = response.json
#     assert data['error'] == 'FyleError'

# def test_list_teachers_as_student(client, h_student_1):
#     """
#     failure case: A student should not be able to list all teachers
#     """
#     response = client.get('/principal/teachers', headers=h_student_1)
#     assert response.status_code == 403
#     data = response.json
#     assert data['error'] == 'Unauthorized access'

######






