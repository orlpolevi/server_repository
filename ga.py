#prime build
import random
from pymongo import MongoClient
import json
from flask import jsonify

#-----------------------------------------------------------------------------------------------#  
#connection to db
cluster = MongoClient()
cluster = MongoClient("mongodb+srv://ormatan:Ormatanormatan123@cluster0.ayazu.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]

#-----------------------------------------------------------------------------------------------#  
#json user data example without unnecessery data
"""
User = []
User.append(
    {"name":"Or",
     "lastName":"Levi",
     "id":"01",
     "type":"student",
     "department":"software",
     "requiredCourses":["algebra", "calculus", "probability", "mishdif"],
     "daysRequired":[
             {"day":"sunday","hours":[1,2,3,4]},
             {"day":"monday","hours":[5,6,7,8]},
             #{"day":"wednesday","hours":[5,6,7,8]},
             {"day":"tursday","hours":[1,2]}],
     "fitness":0}
            ) """
#sunday,monday,tuesday,wednesday,tursday
#-----------------------------------------------------------------------------------------------#  
#corssed individual
crossed = []
   
class crossed_individual_obj():
    def __init__(self, studentDays,toturDays,daysCongruence):
        self.studentDays = studentDays
        self.toturDays = toturDays
        self.daysCongruence = daysCongruence
    studentID = ""
    toturID = ""


#-----------------------------------------------------------------------------------------------#
#auxilary functions
'''
def week_convert_to_binary(a):
    week = []
    day = [0,0,0,0,0]
    hour = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(a)):
        if (a[i]["day"] == "sunday"): 
            day[0]=1 
            
        if (a[i]["day"] == "monday"):
            day[1]=1 
        if (a[i]["day"] == "tuesday"): 
            day[2]=1 
        if (a[i]["day"] == "wednesday"): 
            day[3]=1 
        if (a[i]["day"] == "thursday"): 
            day[4]=1 
        hour = day_convert_to_binary(a[i])
        week[0]={"day":1,"hours":+ hour }
    return week

def day_convert_to_binary(a):
    hour = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(a["hours"])):
        hour[int(a["hours"][i])]+=1
    return hour
 '''

#---------------------GENETIC_ALGORITHM---------------------------------------------------------#

def selection(User, Course, department):
    #data retrival phase
    
    #test cuz of dict problem
    User_from_db = collection.find_one({"name":"" + User["name"]})
    
    query_finds_counter = 0
    sorted_tutors_list = []
    selection_query = collection.find({"coursesProvide":"" + Course, "department":""+department})
    for doc in selection_query:
        sorted_tutors_list.append(doc)
        query_finds_counter+=1
    
    #selection phase based on fitness value which is greater or equal to user's fitness
    toturs_with_good_fitness = []
    for i in sorted_tutors_list:
        if int(i["fitness"]) >= User_from_db["fitness"]:
            toturs_with_good_fitness.append(i)

    for i in range(len(toturs_with_good_fitness)):
        crossover(User,toturs_with_good_fitness[i])
    
  
    #showing congruency
    

    return Course

def crossover(User, totur_to_check):
    #check congruence between users
    #full congruence, partial congruence, no congruence
    #this crossover version also contains the evaluation phase
    studentDays = []
    toturDays = []
    daysCongruence = []
    
    crossed_object = crossed_individual_obj(studentDays,toturDays,daysCongruence)
    crossed_object.studentID = User["id"]
    crossed_object.toturID = totur_to_check["id"]
    crossed_object.studentDays = User["daysProvide"] #need to change<---
    crossed_object.toturDays = totur_to_check["daysProvide"]
    
    check_student_congruence = User.get("daysProvide") #need to change<---
    check_totur_congruence = totur_to_check.get("daysProvide")
    

    for i in range(len(check_student_congruence)):
        if check_totur_congruence[i] is None: break
        else:
            temp1 = check_student_congruence[i]["day"]
            temp2 = check_totur_congruence[i]["day"]
            for j in range(len(check_totur_congruence)): 
                temp3 = check_totur_congruence[j]["day"]
                if (check_student_congruence[i]["day"] == check_totur_congruence[j]["day"]):
                    crossed_object.daysCongruence.append(check_student_congruence[i])
                    crossed_object.daysCongruence.append(check_totur_congruence[j])
                    break
                
    crossed.append(crossed_object)
    
    return

def send_to_solutions(crossed):
    #sending the solution to the database
    #-------NOT RELEVANT AT THE MOMENT--------#
    return
    
def department_mutation(User, course):
    #in case a crossover did not create any solutions
    print("if this is printed - user has no congruence\n")
    print("searching in another department")
    selection(User, course, "mechanics")
    
    return

def indivudual_mutation(User):
    
    return
    
def fitness_calc(User):
    #day = 5, hour = 1, department = 10
    hours_count = 0
    day_count = 0
    dep = 0
    if (User["department"] == "software"): dep = 10
    #aux = User["daysRequired"] --> need to become this not the one below
    aux = User["daysProvide"]
    for i in aux:
        day_count+=1
        hours_count+= len(i["hours"])
    fs = hours_count+(day_count*5)+dep
    fs_dic = {"fitness":int(fs)}
    User["fitness"] = fs_dic
    return fs
        
def initialize(User, course):
    User_from_db = collection.find_one({"name":"" + User})
    
    fitness_calc(User_from_db)
#------random choice for testing-----------------------#
    #course_needed = random.choice(User.get("requiredCourses"))
#------------------------------------------------------#    
    course_needed = course
    Course = selection(User_from_db, course_needed, User_from_db["department"])
    decide_if_need_mutation(User_from_db,Course)
    return terminate(User_from_db, Course)
    

def terminate(User_from_db, Course):
    print("Matching procces completed:\n")
    print("\nFor course: "+ Course + "\nUser: " + User_from_db["name"] + "\nFrom department: "+ User_from_db["department"] + "\nHas congruence with:\n")
    for i in crossed:
        print()
        print(i.toturID + " " + str(i.daysCongruence))
        print("\n")
    return {"msg":"termintation"}  
    
def decide_if_need_mutation(User_from_db,Course):
    if (len(crossed)==0):
        department_mutation(User_from_db,Course)
    else:
        send_to_solutions(crossed)

def evaluation():

    return        

    
#-----------------------------------------------------------------------------------------------#  
  
def initialize2(User, course):
    User_from_db = collection.find_one({"name":"" + User})
    return User_from_db #this returns a dict
