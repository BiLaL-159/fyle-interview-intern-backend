from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.libs import assertions
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """List all submitted and graded assignments"""
    submitted_and_graded_assignments = Assignment.query.filter(
        Assignment.state.in_(['SUBMITTED', 'GRADED'])
    ).all()
    assignments_dump = AssignmentSchema().dump(submitted_and_graded_assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment_id = grade_assignment_payload.id

    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    assertions.assert_found(assignment, 'Assignment not found')
    assertions.assert_valid(assignment.state != AssignmentStateEnum.DRAFT, "Assignment is in DRAFT state and cannot be graded")

    graded_assignment = Assignment.mark_grade(
        _id=assignment_id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

