def print_list(items, header=None):
    if header !=None:
        print(header)

    for item in items:
        print(f"{item}")

students = ["Sania","Baljot","Shivam","Joseph","Sahil","Osman","Ethan","Hussein","Percy","Sean"]
print("STUDENTS:", students)

students.append("Alice")
students.append("Bob")
students.append("Jack")

students.insert(0, "Sam")
print("After inserting Sam:", students)

total_students = len(students)
print("Total number of students:", total_students)

students.remove("Baljot")
print("After removing Baljot:", students)

students.sort()
print("STUDENTS sorted:", students)

students.reverse()
print("STUDENTS reversed:", students)

students.clear()
print("No STUDENTS:", students)
