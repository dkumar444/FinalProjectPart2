import csv
from datetime import date
from datetime import datetime

class Student:
    def __init__(self, Id="", Major="", fName="", lName="", Gpa=0.0, grad_date='', dispAct="No"):
        self.id = Id
        self.major = Major
        self.fname = fName
        self.lname = lName
        self.gpa = Gpa
        self.gradDate = grad_date
        self.dispAction = dispAct

    def getData(self):
        return f'{self.id},{self.major},{self.fname},{self.lname},{self.gpa},{self.gradDate}, {self.dispAction}'

def readFile(name, type='csv'):
    if type == 'csv':
        file = open(f"{name}.{type}")
        csvreader = csv.reader(file)
        mylist = []
        for row in csvreader:
            mylist.append(row)
        file.close()
        return mylist
    pass

def validateGpa(val,disp, std, factor):
    today = date.today()
    currentDate = today.strftime("%m/%d/%y")

    # convert string to date object
    d2 = datetime.strptime(currentDate, "%m/%d/%y")
    d1 = datetime.strptime(f"{std.gradDate}", "%m/%d/%Y")

    delta = d2 - d1# student is graduated or not?
    delta =int(delta.days)


    if (val + factor) >= std.gpa >= (val - factor) and std.dispAction=='No' and std.major==disp and delta <=0:
        return True
    return False

if __name__ == '__main__':
    studentList = []
    templist = []
    gpas = readFile("GPAList")
    majors = readFile('StudentsMajorsList')
    grad_dates = readFile('GraduationDatesList')
    opt = ''

    for row in majors:
        id = row[0]
        lname = row[1]
        fname = row[2]
        major = row[3]
        action = row[4]

        if action in ['Y', 'Yes', 'yes', 'y']:
            action = 'Yes'
        else:
            action = "No"

        if id != "":
            s1 = Student(id, major, fname, lname, 0.0, '', action)
            studentList.append(s1)

    for row in grad_dates:
        for i in range(len(studentList)):
            if row[0] == studentList[i].id:
                studentList[i].gradDate = row[1]

    for row in gpas:
        for i in range(len(studentList)):
            if row[0] == studentList[i].id:
                try:
                    studentList[i].gpa = float(row[1])
                except Exception as e:
                    studentList[i].gpa = 0.0
                pass

    while (opt!='q'):

        print("Enter Query")
        print("OR")
        print("Press q to exit")
        print("Query: -",end = '  ')
        opt = input()

        if opt=='q':
            break

        #part2 graduation date validation
        qlist = opt.split(" ")
        gpa = 0.0
        foundGpa = False
        foundGpaIndex = -1
        # verifying valid query

        if len(qlist)<2:
            print("No such student")
            break

        for i in range(len(qlist)):
            try:
                gpa = float(qlist[i])
                foundGpa=True
                foundGpaIndex = i
            except Exception as e:
                pass

        if not foundGpa:
            print("No such student")
            break

        qlist.pop(foundGpaIndex)

        disp = ' '.join([item for item in qlist])

        found = False
        for item in studentList:
            if item.major==disp:
                found=True

        if not found:
            print("No such student")
            break


        found = False

        print("\nYour student(s):\n")
        for i in range(len(studentList)):
            if validateGpa(gpa,disp, studentList[i],0.1):
                print(f"Id : {studentList[i].id}\n"
                      f"First Name : {studentList[i].fname}\n"
                      f"Last Name : {studentList[i].lname}\n"
                      f"GPA : {studentList[i].gpa}")
                print('\n')
                templist.append(studentList[i].id)
                found = True
                pass

        #

        print("\nYou may, also, consider:\n")
        for i in range(len(studentList)):
            if validateGpa(gpa, disp, studentList[i], 0.25):
                if studentList[i].id not in templist:
                    print(f"Id : {studentList[i].id}\n"
                          f"First Name : {studentList[i].fname}\n"
                          f"Last Name : {studentList[i].lname}\n"
                          f"GPA : {studentList[i].gpa}")
                    print('\n')
                    found = True
                pass

        print("\nFinally, consider:\n")
        factor = 0.3
        while found!=True:
            if factor>5.0:
                break
            for i in range(len(studentList)):
                if validateGpa(gpa, disp, studentList[i], factor):
                    print(f"Id : {studentList[i].id}\n"
                          f"First Name : {studentList[i].fname}\n"
                          f"Last Name : {studentList[i].lname}\n"
                          f"GPA : {studentList[i].gpa}")
                    print('\n')
                    found = True
                    pass
            factor +=0.1

        #part2end