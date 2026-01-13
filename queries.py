# List of constant queries that are used in the programs

ORDERING = """
(CASE 
    WHEN C.Completion = "Completed" THEN 1
    WHEN C.Completion = "Current" THEN 2
    WHEN C.Completion = "Planned" THEN 3
    WHEN C.Completion = "Available" THEN 4
    WHEN C.Completion = "Prereq" THEN 5
    ELSE 6
    END) ASC,
(CASE 
    WHEN Term = NULL THEN 1
    ELSE 2
    END) DESC,
(CASE 
    WHEN LEFT(C.Term, 1) = 'F' THEN CONCAT(RIGHT(C.Term, 2), '-', '3')
    WHEN LEFT(C.Term, 1) = 'W' THEN CONCAT(RIGHT(C.Term, 2), '-', '1')
    WHEN LEFT(C.TERM, 1) = 'S' THEN CONCAT(RIGHT(C.Term, 2), '-', '2')
    ELSE NULL
    END) ASC,
(CASE 
    WHEN C.CourseType = "Non-Math" THEN 1
    WHEN C.CourseType = "PD" THEN 2
    WHEN C.CourseType = "Math" THEN 3
    ELSE 4
	END) ASC
"""

COLUMNS_1 = ["Course Code", "Course Name", "Course Type", "Prerequisite Code", "Prerequisite Name", "Minimum Grade"]
PREREQS = f"""
SELECT
	C.CourseCode,
    C.CourseName,
    C.CourseType,
    PC.PrereqCode,
    PC.CourseName,
    P.MinGrade
FROM
	course_info AS C
INNER JOIN
	prerequisite_courses AS P
ON
	P.CourseCode = C.CourseCode
INNER JOIN
	(SELECT DISTINCT
        PC.PrereqCode,
        C.CourseName,
        C.Completion
    FROM
		prerequisite_courses AS PC
	INNER JOIN
		course_info AS C
	ON 
		PC.PrereqCode = C.CourseCode) AS PC
ON
	PC.PrereqCode = P.PrereqCode
WHERE 
	PC.Completion != "Completed" AND PC.Completion != "Current"
ORDER BY 
    C.CourseCode ASC;
"""