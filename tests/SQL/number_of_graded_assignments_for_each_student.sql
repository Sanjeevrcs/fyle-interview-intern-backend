-- Write query to get number of graded assignments for each student:

SELECT student_id, COUNT(id) AS graded_assignments_count FROM Assignments
GROUP BY student_id
ORDER BY student_id;
