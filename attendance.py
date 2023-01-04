import sqlite3
from datetime import datetime ,date
import pandas as pd
import numpy as np
from dateutil import parser
#connecting to database

conn = sqlite3.connect('attendance.db')
c= conn.cursor()

def get_attendance(employee,day):
    employee_q = c.execute("SELECT * FROM Attendance WHERE employee = :employee AND day=:day ",{'employee':employee,'day':day})
    employee_available = c.fetchall()
    if (employee_available):
        employee_id= c.execute("SELECT ActionTime FROM AttendanceActions WHERE AttendanceId =:id",{'id':int(employee_available[0][0])})
        dates = employee_id.fetchall()
        date_string_AM = parser.parse(str(dates[0]).strip('(,)'))
        date_string_PM = parser.parse(str(dates[1]).strip('(,)'))
        duration = datetime.combine(date.min, date_string_PM.time()) - datetime.combine(date.min, date_string_AM.time())
        hours=(duration.seconds//3600)
        minutes = ((duration.seconds//60)%60)
        return({'attended':True,'duration':str(hours)+":"+str(minutes)})
    else:
        return({'attended':False})

   

print(get_attendance('EMP01','2020-04-01'))

conn.close()

#
#