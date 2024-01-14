import sqlite3
import utils
from datetime import datetime
import hashlib

def custom_hash(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()


def user_exists(username: str) -> bool:
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get user
        user = cur.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchall()
        
        return bool(user)


def check_password(username: str, password: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get user's password
        data_password = cur.execute('SELECT password FROM User WHERE username = ?', (username,)).fetchone()
        
        # User does not exist
        if not data_password[0]:
            return False

        return custom_hash(password) == data_password[0]


def get_all_courses():
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get all courses
        courses = cur.execute('SELECT * FROM Mathima').fetchall()

        # Course list is empty
        if not courses:
            return False

        return [utils.Course(course) for course in courses]


def change_password(username: str, password: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()
        password = custom_hash(password)
        # Get user's info
        user = cur.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()

        # User does not exist
        if not user:
            return False

        # Change user's password
        conn.execute('UPDATE User SET password = ? WHERE username = ?', (password, username))
        conn.commit()

        return True


def is_admin(username: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get user's role
        role = cur.execute('SELECT role FROM User WHERE username = ?', (username,)).fetchone()

        return role[0] == 'professor'


def create_user(ID: str, password: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        password = custom_hash(password)

        students = cur.execute('SELECT * FROM Student').fetchall()
        student_am_list, student_username_list = [], []
        for student in students:
            student_am_list.append(student[3])
            student_username_list.append(student[4])

        professors = cur.execute('SELECT * FROM Professor').fetchall()
        professor_id_list, professor_username_list = [], []
        for professor in professors:
            professor_id_list.append(professor[3])
            professor_username_list.append(professor[4])

        if ID.isnumeric():  # Student
            if int(ID) in student_am_list:
                if student_username_list[student_am_list.index(int(ID))] is not None:
                    # User already exists
                    return False

                # Create user and add username
                username = 'up' + ID
                conn.execute('INSERT INTO User VALUES (?, ?, ?)', (username, password, 'student'))
                conn.execute('UPDATE Student SET username = ? WHERE AM = ?', (username, int(ID)))
                conn.commit()
                return True

        else:  # Professor
            if ID in professor_id_list:
                if professor_username_list[professor_id_list.index(ID)] is not None:
                    # User already exists
                    return False

                # Create user and add username
                username = 'up' + ID
                conn.execute('INSERT INTO User VALUES (?, ?, ?)', (username, password, 'professor'))
                conn.execute('UPDATE Professor SET username = ? WHERE ID = ?', (username, ID))
                conn.commit()
                return True

        return False


def get_id_from_user(username: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        user = cur.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()

        # User does not exist
        if not user:
            return False

        if user[2] == 'student':
            return cur.execute('SELECT AM FROM Student WHERE username = ?', (username,)).fetchone()[0]
        elif user[2] == 'professor':
            return cur.execute('SELECT ID FROM Professor WHERE username = ?', (username,)).fetchone()[0]


def get_student(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        return utils.Student(student)


def get_professor(ID: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        professor = cur.execute('SELECT * FROM Professor WHERE ID = ?', (ID,)).fetchone()

        # Student does not exist
        if not professor:
            return False

        return utils.Professor(professor)


def calculate_course_grade(AM: int, kwd_math: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get course code
        teaching_code = cur.execute('''SELECT kwd_didask FROM Didaskalia NATURAL JOIN Eggrafetai_se_didask
                                       WHERE AM = ? AND kwd_math = ?
                                       ORDER BY strftime('%Y', etos) DESC''', (AM, kwd_math)).fetchone()[0]

        # Student has not signed up to that course
        if not teaching_code:
            return False

        # Get all grades that correspond to that course
        grades = cur.execute('''SELECT weight, max(timh), status, ypoxrewtiko
                                FROM Did_Drasthriothta NATURAL JOIN Bathmos
                                WHERE AM = ?
                                AND kwd_didask = ?
                                GROUP BY kwd_drast''', (AM, teaching_code)
                             ).fetchall()

        # Student doesn't have any grades on that course yet
        if not grades:
            return utils.Grade(-2.0, '')

        # Calculate course grade
        course_grade = 0.0
        for grade in grades:
            if grade[3] and grade[1] < 0:
                course_grade = -1.0
                break

            course_grade += grade[0] * grade[1]
        

        # Calculate grade's status
        grade_status = 'Τελικό'
        if 'Προσωρινό' in (status_list := [grade[2] for grade in grades]):
            grade_status = 'Προσωρινό'
        elif 'Τελικό (Επαναληπτικές)' in status_list:
            grade_status = 'Τελικό (Επαναληπτικές)'

        return utils.Grade(round(course_grade * 2) / 2, grade_status)


def calculate_average_grade(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get all student's courses that he has signed up to (with weight for each course)
        courses = cur.execute('''SELECT kwd_math, weight
                                        FROM Eggrafetai_se_didask NATURAL JOIN Didaskalia NATURAL JOIN Mathima
                                        WHERE AM = ?''', (AM,)).fetchall()

        # Calculate average grade
        average_grade, weight_sum = 0.0, 0.0
        for course in courses:
            grade = calculate_course_grade(AM, course[0])

            # Student doesn't have grade on that course yet
            if not grade.mark:
                continue

            # Count only final grades and those over or equal to 5.0
            if grade.mark >= 5.0 and 'Τελικό' in grade.status:
                average_grade += grade.mark * course[1]
                weight_sum += course[1]

        if weight_sum:
            return round(average_grade / weight_sum, 2)

        return 0.0


def get_students_courses(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student's info
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        # Get all student's courses that he has signed up to
        courses_list = cur.execute('''SELECT DISTINCT kwd_math, titlos_math, omada, ECTS, didaktikes_mon, weight,
                                                      eksamhno, status
                                      FROM Eggrafetai_se_didask NATURAL JOIN Didaskalia NATURAL JOIN Mathima
                                      WHERE AM = ?''', (AM,)).fetchall()

        # Course list is empty
        if not courses_list:
            return False

        return [utils.StudentCourse(utils.Student(student), utils.Course(course[:-1]), course[-1])
                for course in courses_list]


def get_students_passed_courses(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student's info
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        # Get all student's courses that he has signed up to
        courses_list = cur.execute('''SELECT DISTINCT kwd_math, titlos_math, omada, ECTS, didaktikes_mon, weight,
                                                      eksamhno, status
                                      FROM Eggrafetai_se_didask NATURAL JOIN Didaskalia NATURAL JOIN Mathima
                                      WHERE AM = ? AND status = "OLOKLHRWMENO"''', (AM,)).fetchall()

        # Course list is empty
        if not courses_list:
            return False

        return [utils.StudentCourse(utils.Student(student), utils.Course(course[:-1]), course[-1])
                for course in courses_list]


def get_professors_courses(ID: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get professor's info
        professor = cur.execute('SELECT * FROM Professor WHERE ID = ?', (ID,)).fetchone()

        # Professor does not exist
        if not professor:
            return False

        # Get all professor's courses that he is teaching
        activities_list = cur.execute('''SELECT DISTINCT * FROM Mathima NATURAL JOIN
                                      (SELECT kwd_math, kwd_drast
                                       FROM Professor
                                       JOIN Did_Drasthriothta on ID = professorID
                                       NATURAL JOIN Didaskalia
                                       WHERE ID = ?
                                       AND strftime('%Y', etos) = (SELECT strftime('%Y', MAX(etos)) from Didaskalia))''',
                                      (ID,)).fetchall()

        # Activity list is empty
        if not activities_list:
            return False

        # Rearrange list elements
        activities_list = [(activity[:-1], activity[-1]) for activity in activities_list]

        # Use a dictionary to group values based on the first element
        grouped_dict = {}
        for key, value in activities_list:
            if key not in grouped_dict:
                grouped_dict[key] = []
            grouped_dict[key].append(value)

        # Convert the dictionary items back to a list of tuples
        course_list = [(key, tuple(values)) for key, values in grouped_dict.items()]

        # Replace activity codes with Activity objects
        professor_course_list = []
        professor_obj = utils.Professor(professor)
        for course in course_list:
            activities = [utils.Activity(cur.execute('''SELECT * FROM Did_Drasthriothta WHERE kwd_drast = ?''',
                                                     (act_code,)).fetchone()) for act_code in course[1]]
            professor_course_list.append(utils.ProfessorCourse(professor_obj, utils.Course(course[0]), activities))

        return professor_course_list


def get_students_by_course(course_code: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get all students that have signed up to that course
        student_list = cur.execute('''SELECT * FROM Student NATURAL JOIN
                                      (SELECT AM
                                      FROM Mathima NATURAL JOIN Didaskalia NATURAL JOIN Eggrafetai_se_didask
                                      WHERE kwd_math = ? 
                                      AND strftime('%Y', etos) = (SELECT strftime('%Y', MAX(etos)) from Didaskalia))''',
                                   (course_code,)).fetchall()

        # Student list is empty
        if not student_list:
            return False

        return [utils.Student(student) for student in student_list]


def set_grade(AM: int, activity_code: int, grade_value: float, exam_period: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        grade = cur.execute('SELECT * FROM Bathmos WHERE AM = ? AND kwd_drast = ? AND eksetastikh_periodos = ?',
                            (AM, activity_code, exam_period)).fetchone()

        if grade:
            # If grade already exists, just change the value
            conn.execute('UPDATE Bathmos SET timh = ? WHERE AM = ? AND kwd_drast = ? AND eksetastikh_periodos = ?',
                         (grade_value, AM, activity_code, exam_period))
        else:
            # ...or else insert it
            conn.execute('INSERT INTO Bathmos VALUES (?, ?, ?, ?, "Προσωρινό")',
                         (AM, activity_code, grade_value, exam_period))

        conn.commit()


def get_grade(AM: int, activity_code: int, exam_period: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()
        
        # Get grade
        grade = cur.execute('''SELECT timh, status FROM Bathmos
                               WHERE AM = ? AND kwd_drast = ? AND eksetastikh_periodos = ?''',
                            (AM, activity_code, exam_period)).fetchone()

        
        # Student doesn't have a grade on that activity and period
        if not grade:
            return False
        
        

        return utils.Grade(grade[0], grade[1])


def finalize_grades(activity_code: int, exam_period: str):
    with sqlite3.connect('student_services.db') as conn:

        # Calculate grade's status
        status = 'Τελικό'
        if exam_period == 'SEPT':
            status += ' (Επαναληπτικές)'

        # Update grade status
        conn.execute("UPDATE Bathmos SET status = ? WHERE kwd_drast = ? AND eksetastikh_periodos = ?",
                     (status, activity_code, exam_period))
        conn.commit()

        update_students_course_status()
        
        return True


def update_students_course_status():
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get all courses
        courses = cur.execute('SELECT AM, kwd_math FROM Eggrafetai_se_didask NATURAL JOIN Didaskalia').fetchall()

        for course in courses:
            # Get student's grade on that course
            grade = calculate_course_grade(course[0], course[1])

            # Calculate student's course status
            if 'Τελικό' in grade.status:
                if grade.mark < 5.0:
                    status = 'Ολοκληρώθηκε Ανεπιτυχώς'
                else:
                    status = 'Ολοκληρωμένο με Επιτυχία'
            else:
                status = 'Εγγεγραμμένος'

            # Update course status
            conn.execute('''UPDATE Eggrafetai_se_didask SET status = ? WHERE AM = ? AND kwd_didask IN
                            (SELECT kwd_didask FROM Didaskalia WHERE kwd_math = ?)''',
                         (status, course[0], course[1]))
            conn.commit()

        return True


def can_set_field_of_study(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student's admission date
        admission_date = cur.execute("SELECT date_eisagwghs FROM Student WHERE AM = ?", (AM,)).fetchone()[0]

        # Student does not exist
        if not admission_date:
            return False

        # Get current date
        current_date = datetime.now().date()

        # Convert the date strings to datetime objects
        admission_date = datetime.strptime(admission_date, '%Y-%m-%d').date()

        # Calculate number of years between the two dates
        delta = current_date - admission_date
        years = delta.days / 365.25

        return years >= 3


def get_all_fields_of_study():
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get all fields of study
        fos_list = cur.execute('SELECT * FROM Kateuthunsh').fetchall()

        # FoS list is empty
        if not fos_list:
            return False

        return [utils.FieldOfStudy(fos) for fos in fos_list]


def get_field_of_study(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student's field of study
        fos = cur.execute('SELECT kwd_kat, titlos_kat FROM Student NATURAL JOIN Kateuthunsh WHERE AM = ?',
                          (AM,)).fetchone()

        # Student doesn't have a field of study
        if not fos:
            return False

        return utils.FieldOfStudy(fos)


def set_field_of_study(AM: int, fos_code: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        # Set student's field of study
        conn.execute('UPDATE Student SET kwd_kat = ? WHERE AM = ?', (fos_code, AM))
        conn.commit()

        return True


def get_all_theses():
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get all fields of study
        theses_list = cur.execute('SELECT * FROM Diplwmatikh').fetchall()

        # FoS list is empty
        if not theses_list:
            return False

        return [utils.Thesis(thesis) for thesis in theses_list]


def get_thesis(AM: int):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student's thesis
        thesis = cur.execute('''SELECT kwd_dipl, titlos_dipl, professorID
                                FROM Diplwmatikh NATURAL JOIN Dhlwnei_dipl
                                WHERE AM = ?''',
                             (AM,)).fetchone()

        # Student doesn't have a thesis
        if not thesis:
            return False

        return utils.Thesis(thesis)


def set_thesis(AM: int, thesis_code: str, semester_type: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False
        
        # Calculate student's semester
        student_year = datetime.now().year - datetime.strptime(student[7], '%Y-%m-%d').year
        student_semester = student_year * 2
        if semester_type == 'Χειμερινό':
            student_semester -= 1
            
        if student_semester < 8:
            return False

        # Get thesis
        thesis = cur.execute('SELECT * FROM Diplwmatikh WHERE kwd_dipl = ?', (thesis_code,)).fetchone()

        # Thesis does not exist
        if not thesis:
            return False

        # Set student's thesis
        conn.execute('INSERT OR IGNORE INTO Dhlwnei_dipl VALUES (?, ?)', (thesis_code, AM))
        conn.commit()

        return True


def get_students_available_courses(AM: int, semester_type: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        # Calculate student's semester
        if semester_type == 'FEBR':
            current_date_str = str(datetime.now().year) + '-01-15'
        elif semester_type == 'JUNE':
            current_date_str = str(datetime.now().year) + '-05-15'
        else:
            current_date_str = str(datetime.now().year) + '-08-15'

        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        admission_date = datetime.strptime(student[7], "%Y-%m-%d")
        days_difference = (current_date - admission_date).days

        semester = days_difference // 365 * 2 + 1
        if days_difference % 365 >= 167:
            semester += 1

        # Get all available courses to the student
        courses = cur.execute('''SELECT * FROM Mathima WHERE eksamhno % 2 = ? AND eksamhno <= ?
                                 EXCEPT
                                 SELECT kwd_math, titlos_math, omada, ECTS, didaktikes_mon, weight, eksamhno
                                 FROM Eggrafetai_se_didask NATURAL JOIN Didaskalia NATURAL JOIN Mathima
                                 WHERE status = "Ολοκληρωμένο με Επιτυχία" AND AM = ?''',
                              (semester % 2, semester, AM)).fetchall()

        # No available courses
        if not courses:
            return False

        return [utils.Course(course) for course in courses]


def sign_up_to_courses(AM: int, course_list: [str], semester_type: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        # Calculate student's semester
        if semester_type == 'FEBR':
            current_date_str = str(datetime.now().year) + '-01-15'
        elif semester_type == 'JUNE':
            current_date_str = str(datetime.now().year) + '-05-15'
        else:
            current_date_str = str(datetime.now().year) + '-08-15'

        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        admission_date = datetime.strptime(student[7], "%Y-%m-%d")
        days_difference = (current_date - admission_date).days

        semester = days_difference // 365 * 2 + 1
        if days_difference % 365 >= 167:
            semester += 1
        
        print(semester)

        # Count total ECTS credits
        ects_count = 0
        for course_code in course_list:
            ects_count += cur.execute('SELECT ECTS FROM Mathima WHERE kwd_math = ?', (course_code,)).fetchone()[0]

        # Check maximum number of ECTS credits
        if semester >= 7:
            if ects_count > 75:
                return False
        elif semester >= 5:
            if ects_count > 60:
                return False

        courses = []
        for course_code in course_list:
            courses.append(cur.execute('''SELECT kwd_didask FROM Didaskalia NATURAL JOIN Mathima
                                          WHERE kwd_math = ?
                                          AND strftime('%Y', etos) = (SELECT max(strftime('%Y', etos)) FROM Didaskalia)''',
                                       (course_code,)).fetchone()[0])

        # Sign student up to the courses
        for course in courses:
            conn.execute('''INSERT OR IGNORE INTO Eggrafetai_se_didask VALUES (?, ?, 'Εγγεγραμμένος')''', (AM, course))

        conn.commit()
        return True


def has_signed_up_to_courses(AM: int, semester_type: str):
    with sqlite3.connect('student_services.db') as conn:
        cur = conn.cursor()

        # Get student
        student = cur.execute('SELECT * FROM Student WHERE AM = ?', (AM,)).fetchone()

        # Student does not exist
        if not student:
            return False

        # Calculate student's semester
        if semester_type == 'FEBR':
            current_date_str = str(datetime.now().year) + '-01-15'
        elif semester_type == 'JUNE':
            current_date_str = str(datetime.now().year) + '-05-15'
        else:
            current_date_str = str(datetime.now().year) + '-08-15'

        

        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
        admission_date = datetime.strptime(student[7], "%Y-%m-%d")
        days_difference = (current_date - admission_date).days

        year = days_difference // 365 + 1

        print("year", year)

        # Get student's available courses
        courses = get_students_available_courses(AM, semester_type)

        course_codes = []
        for course in courses:
            course_codes.append(cur.execute('''SELECT kwd_didask FROM Eggrafetai_se_didask NATURAL JOIN Didaskalia
                                               WHERE AM = ? AND kwd_math = ? AND strftime('%Y', etos) = ?''',
                                            (AM, course.code, str(datetime.now().year - 1))).fetchone())
        print("course_codes", course_codes)
        if all(course is None for course in course_codes):
            return False
        


        return True
    

def course_grade_bar_chart(course_code: str):
    # Get all students that are signed up to that course
    students = get_students_by_course(course_code)

    # Student list is empty
    if not students:
        return False

    # Calculate grades bar chart
    grades = [0 for _ in range(21)]
    for student in students:
        grade = calculate_course_grade(student.AM, course_code)
        if not grade.mark:
            continue
        if grade.mark > 0:
            grades[int(grade.mark * 2)] += 1
    
    if any(grades):
        return grades
        
    return False


def course_pass_percentage(course_code: str):
    # Get all students that are signed up to that course
    students = get_students_by_course(course_code)

    # Student list is empty
    if not students:
        return False

    # Calculate percentage of students who have passed the course
    pass_counter = 0
    for student in students:
        if calculate_course_grade(student.AM, course_code).mark >= 5.0:
            pass_counter += 1

    return round(pass_counter / len(students), 1)


def top_performers(course_code: str):
    # Get all students that are signed up to that course
    students = get_students_by_course(course_code)

    # Student list is empty
    if not students:
        return False

    # Sort the students by their grade on the course
    student_grades = []
    for student in students:
        grade = calculate_course_grade(student.AM, course_code)
        if grade.mark >= 5:
            student_grades.append((student, grade.mark))

    student_grades = sorted(student_grades, key=lambda x: x[1], reverse=True)

    return student_grades[:3]


if __name__ == '__main__':
    

    
    print(custom_hash('pap2'))
    print(custom_hash('a'))
    print(custom_hash('g'))
    print(custom_hash('t'))
    

    