import courses_module as cm
import personal as p

# This program will allow you to update a single entry for a specific course code in a table. Make sure 
#   your input matches exactly to the entries or columns in the database

connection = cm.database_connection(p.HOST_NAME, p.USERNAME, p.PASSWORD, p.DATABASE)

requirement_options = [
    "Mandatory",
    "Required Choice",
    "Not Required"
]

cm.print_list(["course_info", "prerequisite_courses", "academic_plan"])
table = int(input("Which table is being updated?: "))

def update_course():
    course_code = input("What is the course code of the coure being updated?: ")
    cm.print_list(cm.COURSE_COLUMNS)
    column = int(input("What column is being updated?: " ))
    cm.print_list(cm.dict_value(cm.COURSE_DICT, column - 1))
    value = input("What is the updated value?: ")

    if value == "":
        value = "NULL"
        query = f"""
        UPDATE 
            course_info
        SET {cm.COURSE_COLUMNS[column - 1]} = {value}
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """
    elif column == 3 or column == 7:
        query = f"""
        UPDATE 
            course_info
        SET {cm.COURSE_COLUMNS[column - 1]} = {value}
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """

    elif column == 1:
        prereq_query1 = f"""
        UPDATE
            prerequisite_courses
        SET {cm.PREREQ_COLUMNS[0]} = "{value}"
        WHERE {cm.PREREQ_COLUMNS[0]} = "{course_code}"
        """
        prereq_query2 = f"""
        UPDATE
            prerequisite_courses
        SET {cm.PREREQ_COLUMNS[1]} = "{value}"
        WHERE {cm.PREREQ_COLUMNS[1]} = "{course_code}"
        """
        cm.execute_query(connection, prereq_query1)
        cm.execute_query(connection, prereq_query2)
        
        plan_query = f"""
        UPDATE
            academic_plan
        SET {cm.PLAN_COLUMNS[0]} = "{value}"
        WHERE {cm.PLAN_COLUMNS[0]} = "{course_code}";
        """
        cm.execute_query(connection, plan_query)

        query = f"""
        UPDATE
            course_info
        SET {cm.COURSE_COLUMNS[0]} = "{value}"
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """
    elif column == 4 or column == 5:
        value = int(value)
        query = f"""
        UPDATE
            course_info
        SET {cm.COURSE_COLUMNS[column - 1]} = "{cm.dict_value(cm.COURSE_DICT, column - 1)[value - 1]}"
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """
    elif column == 2 or column == 6:
        query = f"""
        UPDATE
            course_info
        SET {cm.COURSE_COLUMNS[column - 1]} = "{value}"
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """
    else:
        print("No entries were updated")
        return
        
    cm.execute_query(connection, query)
    return

def update_prereq():
    course_code = input("What is the course code of the coure being updated?: ")
    prereq_code = input("What is the corresponding prerequisite code?: ")
    cm.print_list(cm.PREREQ_COLUMNS)
    column = int(input("What column is being updated?: "))
    cm.print_list(cm.dict_value(cm.PREREQ_DICT, column - 1))
    value = input("What is the updated value?: ")

    if value == "":
        value = "NULL"
        query = f"""
        UPDATE 
            prerequisite_courses
        SET {cm.PREREQ_COLUMNS[column - 1]} = {value}
        WHERE 
            {cm.PREREQ_COLUMNS[0]} = "{course_code}" AND
            {cm.PREREQ_COLUMNS[1]} = "{prereq_code}";
        """
    elif column == 3:
        query = f"""
        UPDATE 
            prerequisite_courses
        SET {cm.PREREQ_COLUMNS[2]} = {value}
        WHERE 
            {cm.PREREQ_COLUMNS[0]} = "{course_code}" AND
            {cm.PREREQ_COLUMNS[1]} = "{prereq_code}";
        """
    elif 1 <= column <= 3:
        query = f"""
        UPDATE
            prerequisite_courses
        SET {cm.PREREQ_COLUMNS[column - 1]} = "{value}"
        WHERE 
            {cm.PREREQ_COLUMNS[0]} = "{course_code}" AND
            {cm.PREREQ_COLUMNS[1]} = "{prereq_code}";
        """
    else:
        print("No entries were updated")
        return
        
    cm.execute_query(connection, query)
    return

def update_plan():
    course_code = input("What is the course code of the course being updated?: ")
    cm.PLAN_COLUMNS.remove("CourseCode")
    cm.print_list(cm.PLAN_COLUMNS)
    column = int(input("What column is being updated?: " ))
    cm.print_list(requirement_options)
    value = int(input("What is the updated value?: "))

    if 1 <= value <= 3:
        query = f"""
        UPDATE
            academic_plan
        SET {cm.PLAN_COLUMNS[column - 1]} = "{requirement_options[value - 1]}"
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """
    else:
        query = f"""
        UPDATE
            academic_plan
        SET {cm.PLAN_COLUMNS[column - 1]} = NULL
        WHERE {cm.COURSE_COLUMNS[0]} = "{course_code}";
        """
    cm.execute_query(connection, query)
    return

def update_table(table):
    if table == 1:
        update_course()
    elif table == 2:
        update_prereq()
    elif table == 3:
        update_plan()
    else:
        return
    return

update_table(table)
