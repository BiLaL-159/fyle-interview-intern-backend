-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grade_counts AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
),
max_grades_teacher AS (
    SELECT
        teacher_id
    FROM
        teacher_grade_counts
    ORDER BY
        total_graded DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    teacher_id = (SELECT teacher_id FROM max_grades_teacher)
    AND grade = 'A';


