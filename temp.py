from attendance.models import TimeTable, Attendance_Entry, Student
from attendance import db
import datetime

def getattendance():
	# add logic to get attendance
	user_id = '2018UCS0065'
	course_id = 'CSL333'
    # TODO: Get the DateTime objects
	#  from the request form.
	date_upper = datetime.datetime.utcnow()
	date_lower = datetime.datetime.utcnow() - datetime.timedelta(days=10)

	records = Attendance_Entry.query.filter(Attendance_Entry.User_ID==user_id, Attendance_Entry.Course_ID==course_id, Attendance_Entry.Date <= date_upper, Attendance_Entry.Date >= date_lower)

	slots = TimeTable.query.filter(TimeTable.Course_ID==course_id)

	result = dict()

	curr = date_lower
	while(curr <= date_upper):
		class_happens = False
		
		for slot in slots:
			if(slot.Day == curr.weekday()):
				st_time = slot.Start_Time.time()
				end_time = slot.End_Time.time()
				class_happens = True
				result[curr.day] = False
				break
		

		if(class_happens):
			for atten in records:
				if(atten.Date.day == curr.day and  atten.Date.time() <= end_time and atten.Date.time() >= st_time ):
					result[curr.day] = True
		
		curr += datetime.timedelta(days=1)

	return result

dummy_date = datetime.date.today()
start = datetime.time(hour=15,minute=0)
end = datetime.time(hour=17,minute=0)

st_date = datetime.datetime.combine(dummy_date,start)
en_date = datetime.datetime.combine(dummy_date,end)
print(st_date, en_date)
t1 = TimeTable(Course_ID = "CSL333", Day= 1, Semester=6, Start_Time = st_date, End_Time = en_date)
t2 = TimeTable(Course_ID = "CSL333", Day= 2, Semester=6, Start_Time = st_date, End_Time = en_date)

# db.session.add(t1)
# db.session.add(t2)

# db.session.commit()
d1 = datetime.datetime(year=2021, month=4, day=21, hour=9, minute=5)
a1 = Attendance_Entry(Course_ID = "CSL333", User_ID="2018UCS0065", Semester=6, Date = d1)
# db.session.add(a1)
# db.session.commit()
# print(datetime.datetime.utcnow().weekday())
# print(getattendance())

s1 = Student(Stud_ID = "2018UCS0065", Name="Samarth", DOB=d1, Email="samarth@gmail.com", Phone="9191919191", Gender="M",Semester=6, Dept_ID="CS", Path="somepath" )
db.session.add(s1)
db.session.commit()