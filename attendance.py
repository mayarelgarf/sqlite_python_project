import sqlite3
from datetime import datetime ,date
import pandas as pd
import numpy as np
from dateutil import parser
from dateutil import tz
import json

#connecting to database

conn = sqlite3.connect('attendance.db')
c= conn.cursor()

def get_attendance(employee,day):
    employee_q = c.execute("SELECT * FROM Attendance WHERE employee = :employee AND day=:day ",{'employee':employee,'day':day})
    employee_available = c.fetchall()
    if (employee_available):
        employee_id= c.execute("SELECT ActionTime FROM AttendanceActions WHERE AttendanceId =:id",{'id':int(employee_available[0][0])})
        dates = employee_id.fetchall()
        if(dates):
            date_string_AM = parser.parse(str(dates[0]).strip('(,)'))
            date_string_PM = parser.parse(str(dates[1]).strip('(,)'))
            duration = datetime.combine(date.min, date_string_PM.time()) - datetime.combine(date.min, date_string_AM.time())
            hours=(duration.seconds//3600)
            minutes = ((duration.seconds//60)%60)
            print({'attended':True,'duration':str(hours)+":"+str(minutes)})
        else:
            print({'attended':False})
    else:
        print({'attended':False})

   

get_attendance('EMP01','2020-04-02')



def attendance_history(employee):
    days_q= c.execute("SELECT day FROM Attendance where employee = :employee",{'employee':employee})
    total_days = days_q.fetchall()
    #json_days = json.dumps(total_days,indent=2)
    attendance = {'days':[],'actions':[]}
    for day in total_days:
        attendance['days'].append(day)
    ID_q= c.execute("SELECT id FROM Attendance where employee = :employee",{'employee':employee})
    employee_id = ID_q.fetchall()
    action_q = c.execute("SELECT action,ActionTime FROM AttendanceActions WHERE AttendanceId =:id",{'id':int(employee_id[0][0])})
    employee_action = action_q.fetchall()
    for i in employee_action:
        only_time = i[1]
        time_stamp=parser.parse(only_time)
        to_zone= tz.gettz('UTC')
        tt= time_stamp.astimezone(to_zone)
        iso_date = json.dumps(datetime.isoformat(tt))
        attendance['actions'].append(iso_date)
    print(attendance)

attendance_history('EMP01')

conn.close()

#
#