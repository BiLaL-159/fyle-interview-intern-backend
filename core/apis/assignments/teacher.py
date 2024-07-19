from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core.libs import assertions

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments for the authenticated teacher"""
    teachers_assignments = Assignment.filter(
        Assignment.teacher_id == p.teacher_id,
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    assertions.assert_found(assignment, 'Assignment not found')

    # Ensure the assignment is for the authenticated teacher
    assertions.assert_valid(assignment.teacher_id == p.teacher_id, 'Assignment submitted to a different teacher')

    # Ensure the grade is valid
    assertions.assert_valid(grade_assignment_payload.grade in GradeEnum.__members__, 'Invalid grade')

    # Ensure the assignment is not in DRAFT state
    assertions.assert_valid(assignment.state == AssignmentStateEnum.SUBMITTED, 'Only submitted assignments can be graded')


    # Mark the grade and update the state
    assignment.grade = grade_assignment_payload.grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)
