#Script to load data
import sys
from attendance_tracker.models import Counter
from attendance_tracker.models import StudentBasic
from attendance_tracker.models import StudentGrLevel
from attendance_tracker.models import StudentCntInf
import datetime
from django.contrib.auth.models import User

def LoadData(idnum, fname, lname, yyyy, mm, dd, grade, address, city, state, zipcode, personal_cell, f_cell, m_cell, parent_email, student_email):
    student_1 = StudentBasic(id_num=str(idnum),first_name=fname,last_name=lname,dob=datetime.date(int(yyyy), int(mm), int(dd)), archived=False)
    student_1.save()
    grade_1 = StudentGrLevel(student=StudentBasic.objects.get(id_num=str(idnum)),grade=int(grade))
    grade_1.save()
    contact_1 = StudentCntInf(student_grade=StudentGrLevel.objects.get(student=StudentBasic.objects.get(id_num=str(idnum))),address=address,city=city,state=state,zipcode=zipcode,personal_cell=personal_cell,father_cell=f_cell,mother_cell=m_cell,parent_email=parent_email,student_email=student_email)
    contact_1.save()

def ParseFile(text_file_name):
    user_id = Counter.objects.get(counter_name='student_id').counter_value
    fileHandle = open(text_file_name, "r")
    for line in fileHandle:
        fields = line.split('|')
        LoadData(user_id,fields[0],fields[1],(fields[2]),fields[3],fields[4],fields[5],fields[6],fields[7],fields[8],fields[9],fields[10],fields[11],fields[12],fields[13],fields[14])
        print(user_id,fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],fields[8],fields[9],fields[10],fields[11],fields[12],fields[13],fields[14])
        user_id += 1

text_file = sys.argv[3]
ParseFile(text_file)

