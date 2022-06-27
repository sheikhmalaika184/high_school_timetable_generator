import pandas as pd
import numpy as np
import random

data = pd.read_excel (r'input.xlsx' , sheet_name='input')
df_rooms = pd.DataFrame(data , columns= ['Rooms'])
df_rooms = df_rooms.dropna()
df_teachrs_courses = pd.DataFrame(data , columns= ['Teachers' , 'Courses'])
df_teachrs_courses = df_teachrs_courses.dropna()
df_teachers = pd.DataFrame(data , columns= ['Teachers'])
df_teachers = df_teachers.dropna()
df_courses = pd.DataFrame(data , columns= ['Courses'])
df_courses_with_no = pd.DataFrame(data , columns= ['Courses' , 'No_per_week'])
df_courses = df_courses.dropna()

#lists
rooms_list = df_rooms.values.tolist()
courses_list = df_courses.values.tolist()
teachers_list = df_teachers.values.tolist()
teacher_courses_list = df_teachrs_courses.values.tolist()
courses_with_no_list = df_courses_with_no.values.tolist()
rooms = []
courses = []
teachers = []
for i in range(0,len(rooms_list)):
    rooms.append(rooms_list[i][0])
for i in range(0,len(courses_list)):
    courses.append(courses_list[i][0])
    teachers.append(teachers_list[i][0])
courses_set = list(set(courses))

#All subjects with no how many times it will be studied in a week
subjects_no_dict = {}
for i in range(0,len(courses_set)):
    for j in range(0,len(courses_with_no_list)):
        if courses_with_no_list[j][0] == courses_set[i]:
            subjects_no_dict[courses_set[i]] = int(courses_with_no_list[j][1])
            break

#teachers with theirs subjects
teachers_with_subjects = {}
for i in range(0,len(teacher_courses_list)):
    teachers_with_subjects[teacher_courses_list[i][0]] = teacher_courses_list[i][1]

#availablity of teachers
teachers_with_week_duties = {}
for i in range(0,len(teachers)):
    array=[[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0]]
    teachers_with_week_duties[teachers[i]] = array
    
all_classes_timetable_array = []
#print(teachers_with_subjects)
for clas in range(0,len(rooms)):
    # 5 days and 7 timeslots
    timetable_matrix = np.empty([5, 7] , dtype=object)
    for i in range(0,5):
        timetable_matrix[i,4] = "Lunch Break"
        
    #courses with no per week
    courses_no_per_week = {}
    for j in range(0,len(courses_set)):
        courses_no_per_week[courses_set[j]] = subjects_no_dict[courses_set[j]]
    
    print("Week Time Table for","class: ",rooms[clas])
    for day in range(0,5):
        if all(value == 0 for value in courses_no_per_week.values()):
            break
        else:
            day_courses = []
            for time_slot in range(0,7):
                if all(value == 0 for value in courses_no_per_week.values()):
                    break
                else:
                    if(time_slot == 4):
                        day_courses.append("break")
                    else:
                        random.shuffle(courses_set)
                        for r in range(0,len(courses_set)):
                            #random.shuffle(courses_set)
                            random_course = courses_set[r]
                            if(random_course in day_courses or courses_no_per_week[random_course]==0):
                                #print(random_course)
                                continue
                            else:
                                teachers_list = []
                                instructor =""
                                for teacher, subject in teachers_with_subjects.items():
                                    if subject == random_course:
                                        teachers_list.append(teacher)
                                for t in range(0,len(teachers_list)):
                                    if(teachers_with_week_duties[teachers_list[t]][day][time_slot]==0):
                                        instructor = teachers_list[t]
                                        teachers_with_week_duties[teachers_list[t]][day][time_slot]=1
                                        break
                                    else:
                                        continue
                                if(instructor==""):
                                    continue
                                else:
                                    day_courses.append(random_course)
                                    courses_no_per_week[random_course] = courses_no_per_week[random_course] - 1
                                    timetable_matrix[day][time_slot] = random_course+":" + instructor
                                    break
                                
    print(" ") 
    for tr in range(0,len(timetable_matrix)):
        print(timetable_matrix[tr])
    print(" ")
    all_classes_timetable_array.append(timetable_matrix)
#print(all_classes_timetable_array)