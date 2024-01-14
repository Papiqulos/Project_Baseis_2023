import random
import string
from captcha.image import ImageCaptcha


class Student:
    def __init__(self, student):
        self.fname = student[0]
        self.minit = student[1]
        self.lname = student[2]
        self.AM = student[3]
        self.username = student[4]
        self.phone = student[5]
        self.email = student[6]
        self.admission_date = student[7]
        self.kwd_kat = student[8]

    def __str__(self):
        return f'First name: {self.fname}\n' \
               f'Middle initial: {self.minit}\n' \
               f'Last name: {self.lname}\n' \
               f'AM: {self.AM}\n' \
               f'Username: {self.username}\n' \
               f'Phone number: {self.phone}\n' \
               f'Email address: {self.email}\n' \
               f'Admission date: {self.admission_date}\n' \
               f'Kwdikos kateuthinshs: {self.kwd_kat}\n'

    def to_list(self):
        return [self.fname, self.minit, self.lname, self.AM, self.username, self.phone, self.email, 
                self.admission_date, self.kwd_kat]


class Professor:
    def __init__(self, professor):
        self.fname = professor[0]
        self.minit = professor[1]
        self.lname = professor[2]
        self.ID = professor[3]
        self.username = professor[4]
        self.phone = professor[5]
        self.email = professor[6]
        self.bathmida = professor[7]

    def __str__(self):
        return f'First name: {self.fname}\n' \
               f'Middle initial: {self.minit}\n' \
               f'Last name: {self.lname}\n' \
               f'ID number: {self.ID}\n' \
               f'Username: {self.username}\n' \
               f'Phone number: {self.phone}\n' \
               f'Email address: {self.email}\n' \
               f'Academic rank: {self.bathmida}\n'
    
    def to_list(self):
        return [self.fname, self.minit, self.lname, self.ID, self.username, self.phone, self.email, self.bathmida]


class Course:
    def __init__(self, mathima):
        self.code = mathima[0]
        self.title = mathima[1]
        self.group = mathima[2]
        self.ECTS = mathima[3]
        self.credits = mathima[4]
        self.weight = mathima[5]
        self.semester = mathima[6]

    def __str__(self):
        return f'Course code: {self.code}\n' \
               f'Title: {self.title}\n' \
               f'Course group: {self.group}\n' \
               f'ECTS: {self.ECTS}\n' \
               f'Credits: {self.credits}\n' \
               f'Weight: {self.weight}\n' \
               f'Semester: {self.semester}\n'
    
    def to_list(self):
        return [self.code, self.title, self.group, self.ECTS, self.credits, self.weight, self.semester]


class StudentCourse:
    def __init__(self, student, course, status):
        self.student = student
        self.course = course
        self.status = status

    def __str__(self):
        return f'Student AM: {self.student.AM}\n' \
               f'Course code: {self.course.code}\n' \
               f'Course title: {self.course.title}\n' \
               f'Status: {self.status}\n'


class ProfessorCourse:
    def __init__(self, professor, course, activities):
        self.professor = professor
        self.course = course
        self.activities = activities

    def __str__(self):
        string = f'Professor ID: {self.professor.ID}\n' \
                 f'Course code: {self.course.code}\n' \
                 f'Course title: {self.course.title}\n' \

        for i, activity in enumerate(self.activities):
            string += f'Activity {i+1}: {activity.title}\n'

        return string


class Grade:
    def __init__(self, mark, status):
        self.mark = mark
        self.status = status

    def __str__(self):
        return f'Grade mark: {self.mark}\n' \
               f'Grade status: {self.status}\n'
    

class Activity:
    def __init__(self, activity):
        self.activity_code = activity[0]
        self.course_code = activity[1]
        self.professorID = activity[2]
        self.title = activity[3]
        self.weight = activity[4]
        self.room = activity[5]

    def __str__(self):
        return f'Activity code: {self.activity_code}\n' \
               f'Course code: {self.course_code}\n' \
               f'Professor ID: {self.professorID}\n' \
               f'Title: {self.title}\n' \
               f'Weight: {self.weight}\n' \
               f'Room: {self.room}\n'

    def to_list(self):
        return [self.activity_code, self.course_code, self.professorID, self.title, self.weight, self.room]


class FieldOfStudy:
    def __init__(self, fos):
        self.code = fos[0]
        self.title = fos[1]

    def __str__(self):
        return f'Κωδικός Κατεύθυνσης: {self.code}\n' \
               f'Τίτλος Κατεύθυνσης: {self.title}\n'


class Captcha:
    def __init__(self, length):
        self.length = length
        self.string = Captcha.generate_captcha_string(self.length)
        self.image = Captcha.generate_captcha_image(self.string)
        

    @staticmethod
    def generate_captcha_string(length: int):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def generate_captcha_image(string: str):
        return ImageCaptcha().generate_image(string)
    

class Thesis:
    def __init__(self, thesis):
        self.code = thesis[0]
        self.title = thesis[1]
        self.professorID = thesis[2]

    def __str__(self):
        return f'Κωδικός Διπλωματικής: {self.code}\n' \
                f'Τίτλος Διπλωματικης: {self.title}\n' \
                f"ΑΤ Επιβλέπων Καθηγητή: {self.professorID}\n"