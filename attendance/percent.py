from attendance.routes import get_course_wise
from datetime import datetime, timedelta
from attendance import models


def get_student_attendace_percent(student_id):
    # first get the courses.
    # then get the course attendance
    # then just simply put everything in a dictionary
    course_list = models.takes.query.all()
    course_list = [x.Course_ID for x in course_list]

    sem_start = datetime(year=2021, month=1, day=1, hour=0, minute=0)
    sem_end = sem_start + timedelta(days=90)
    
    res = {}

    for course in course_list:
        R = get_course_wise(sem_start,sem_end,student_id,course)
        cnt = 0.0
        for k in R:
            if(R[k] == True):
                cnt += 1.0
        res[course] = cnt / len(R) * 100

    return res
