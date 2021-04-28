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
        'MTL146':['13:00','14:00']],
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

dummy_date = datetime.date.today()
for day in timeTable:
    courses_curr = timeTable[day]
    for course in courses_curr:
        h1 = courses_curr[]
        start = datetime.time(hour=int(),minute=0)
        end = datetime.time(hour=17,minute=0)

st_date = datetime.datetime.combine(dummy_date,start)
en_date = datetime.datetime.combine(dummy_date,end)
print(st_date, en_date)
t1 = TimeTable(Course_ID = "CSL333", Day= 1, Semester=6, Start_Time = st_date, End_Time = en_date)