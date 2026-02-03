def get_student():
    with open('students.txt', 'r') as file:
        students = file.readlines()
        return students
def add_student(name):
    with open('students.txt',"a") as file:
        file.write("\n  -"+name)
    return "done"