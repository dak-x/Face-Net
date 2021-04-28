timeTable = {
    '0':{
        'CSL352':['9:00','10:00'],
        'CSL362':['12:00','13:00'],
        'MTL146':['13:00','14:00'],
        'CSL733':['14:10','15:20']
    },
    '1':{
        'CSL380':['9:00','10:00'],
        'CSL352':['10:00','11:00'],
        'CSL362':['12:00','13:00'],
        'MTL146':['13:00','14:00'],
        'HUL211':['17:00','18:00']
    },
    '2':{
        'CSL331':['9:00','10:00'],
        'CSL380':['10:00','11:00'],
        'CSL362':['12:00','13:00'],
        'MTL146':['13:00','14:00'],
        'CSL352':['14:00','15:00'],
        'HUL211':['18:10','19:20']
    },
    '3':{
        'CSL733':['9:00','10:00'],
        'CSL331':['10:00','11:00'],
        'HUL211':['11:00','12:00'],
        'CSL380':['12:00','13:00']
    },
    '4':{
        'CSL733':['10:00','11:00'],
        'CSL331':['14:00','16:00']
    }
}
import datetime
import attendance, attendance.models



def populate_timetable():
    dummy_date = datetime.date.today()

    entries = []
    for day in timeTable:
        courses_curr = timeTable[day]
        for course in courses_curr:

            h1,m1 = map(int,courses_curr[course][0].split(":"))
            h2,m2 = map(int,courses_curr[course][1].split(":"))

            start = datetime.time(hour=h1,minute=m1)
            end = datetime.time(hour=h2,minute=m2)
            st_date = datetime.datetime.combine(dummy_date,start)
            en_date = datetime.datetime.combine(dummy_date,end)

            ob = attendance.models.TimeTable(Course_ID = course, Day=day,Start_Time = st_date, End_Time=en_date,Semester=6)
            # ob.Course_ID = course
            # ob.Day = day
            # ob.Start_Time = st_date
            # ob.End_Time = en_date
            # ob.Semester = 6
            print(ob.Course_ID)
            entries.append(ob)

    # attendance.db.session.add_all(entries)
# commit using this.
    # attendance.db.session.commit()


# t1 = attendance.models.TimeTable(Course_ID = "CSL333", Day= 1, Semester=6, Start_Time = st_date, End_Time = en_date)
# populate_timetable()
# check = attendance.models.TimeTable.query.all()
# for records in check:
    # print(records.Course_ID, records.Day, records.Start_Time, records.End_Time ,records.Semester)

import random 

# Give entry number and course_list. 
# Auto fetch details form timetable and generate entries.
def populate_attendance(entry_no, course_list):
    
    entries = []

    date = datetime.datetime.today()

    # populate for a month starting from today
    for i in range(30):
        shifted_date = date + datetime.timedelta(days=i)
        entry_date = shifted_date.date()
        weekday = entry_date.weekday()

        for course in timeTable[weekday]:
            if(course in course_list):
                x = random.uniform(0,1)
                #mark the attendance
                if( x < 0.75 ):
                    h,m = map(int, timeTable[weekday][course][0].split(":"))
                    t = datetime.time(hour=h,minute=m)
                    entry_date = datetime.datetime.combine(entry_date,t)
                    
                    ob = attendance.models.Attendance_Entry(Course_ID = course, Date=entry_date,Semester=6,User_ID=entry_no)

                    entries.append(ob)

    # Use this to commit.
    # attendance.db.session.add_all(entries)

# populate_attendance("2018UCS0065",["CSL352","CSL331","HUL211"])
