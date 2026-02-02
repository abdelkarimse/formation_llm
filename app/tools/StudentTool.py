def get_student():
    with open('student.txt', 'r') as file:
        students = file.readlines()
        return students
def add_student(name):
    with open('student.txt',"a") as file:
        file.write("\n  -"+name)
    return "done"