import courses_module as cm
import personal as p

# This program will allow you to calcualte different types of values depending on different variables

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, p.DATABASE)

calculation_options = [
    "Average Grade",
    "Math Average",
    "Number of Course Type",
    "Total Credits",
    "GPA Calculator",
    "Academic Plan Requirements"
]

requirement_options = [
    "Mandatory",
    "Required Choice",
    "Not Required",
    "Mandatory + Required Choice"
]

cm.print_list(calculation_options)
type = int(input("What would you like to calculate?: "))

def calculate_avg():
    query = """
    SELECT 
        ROUND(AVG(Grade), 2)
    FROM
        course_info
    WHERE 
        Completion = "Completed" AND
        Grade IS NOT NULL;
    """
    return query

def math_avg():
    query = """
    SELECT 
        ROUND(AVG(Grade), 2)
    FROM
        course_info
    WHERE 
        Completion = "Completed" AND
        Grade IS NOT NULL AND
        CourseType = "Math";
    """
    return query

def num_course_type():
    cm.print_list(cm.COMPLETION_TYPES + ["All"])
    completion = int(input("What completion status would you like to calculate?: "))
    if 1 <= completion <= 5:
        query = f"""
        SELECT
            COUNT(CourseCode)
        FROM 
            course_info
        WHERE 
            Completion = "{cm.COMPLETION_TYPES[completion - 1]}";
        """
    elif completion == 6:
        query = """
        SELECT
            COUNT(CourseCode)
        FROM 
            course_info;
        """
    else:
        return
    return query

def num_credit():
    cm.print_list(["Course Type", "Completion Type", "All Completed Coures (Excluding PD Courses)"])
    column = int(input("How you like to view the number of credits?: "))
    if column == 1:
        cm.print_list(cm.COURSE_TYPE)
        type = int(input("What type of course would you like to view?: "))
        query = f"""
        SELECT
            SUM(Credits)
        FROM 
            course_info
        WHERE 
            CourseType = "{cm.COURSE_TYPE[type - 1]}"
        """
    elif column == 2:
        cm.print_list(cm.COMPLETION_TYPES)
        status = int(input("What course status would you like to view (excludes PD courses)?: "))
        query = f"""
        SELECT
            SUM(Credits)
        FROM 
            course_info
        WHERE 
            Completion = "{cm.COMPLETION_TYPES[status - 1]}" AND
            CourseType != "PD";
        """
    elif column == 3:
        query = """
        SELECT
            SUM(Credits)
        FROM 
            course_info
        WHERE 
            Completion = "Completed" AND
            CourseType != "PD";
        """
    else:
        return
    return query

def gpa_calc():
    query = """
    SELECT
	SUM(GPA * Credits)/SUM(Credits)
    FROM
        (SELECT 
            CourseCode,
            CASE
                WHEN Grade >= 90 THEN 4.00
                WHEN Grade >= 85 AND Grade <= 89 THEN 3.90
                WHEN Grade >= 80 AND Grade <= 84 THEN 3.70
                WHEN Grade >= 77 AND Grade <= 79 THEN 3.30
                WHEN Grade >= 73 AND Grade <= 76 THEN 3.00
                WHEN Grade >= 70 AND Grade <= 72 THEN 2.70
                WHEN Grade >= 67 AND Grade <= 69 THEN 2.30
                WHEN Grade >= 63 AND Grade <= 66 THEN 2.00
                WHEN Grade >= 60 AND Grade <= 62 THEN 1.70
                WHEN Grade >= 56 AND Grade <= 59 THEN 1.30
                ELSE "STOP"
            END AS GPA
        FROM
            course_info
        WHERE
            Credits != 0 AND
            Grade IS NOT NULL AND
            Completion = "Completed") AS G
    INNER JOIN
        course_info AS C
    ON 
        C.CourseCode = G.CourseCode
    WHERE
        C.Credits != 0 AND
        C.Grade IS NOT NULL AND
        C.Completion = "Completed";
    """
    return query

def plan_requirements():
    cm.PLAN_COLUMNS.remove("CourseCode")
    cm.print_list(cm.PLAN_COLUMNS)
    plan = int(input("Which academic plan would you like to calculate?: "))
    cm.print_list(requirement_options)
    requirement = int(input("What would you like to calculate?: "))
    if 1 <= requirement <= 3:
        query = f"""
        SELECT 
            SUM(C.Credits)
        FROM
            academic_plan AS P
        INNER JOIN
            course_info AS C
        ON 
            C.CourseCode = P.CourseCode
        WHERE 
            {cm.PLAN_COLUMNS[plan - 1]} = "{requirement_options[requirement - 1]}";
        """
    elif requirement == 4:
        query = f"""
        SELECT 
            SUM(C.Credits)
        FROM
            academic_plan AS P
        INNER JOIN
            course_info AS C
        ON 
            C.CourseCode = P.CourseCode
        WHERE 
            {cm.PLAN_COLUMNS[plan - 1]} IN ("Mandatory", "Required Choice");
        """
    else:
        return
    return query

table = []

def calculate():
    if type == 1:
        query = calculate_avg()
        cm.display_info(connection, query, ["Cumulative Average"], table)
    elif type == 2:
        query = math_avg()
        cm.display_info(connection, query, ["Math Average"], table)
    elif type == 3:
        query = num_course_type()
        cm.display_info(connection, query, ["Number of Courses"], table)
    elif type == 4:
        query = num_credit()
        cm.display_info(connection, query, ["Number of Credits"], table)
    elif type == 5:
        query = gpa_calc()
        cm.display_info(connection, query, ["GPA"], table)
    elif type == 6:
        query = plan_requirements()
        cm.display_info(connection, query, ["Total Credits"], table)
    else:
        return
    
calculate()
    