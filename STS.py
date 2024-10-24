class Student:
    def __init__(self, name="", phone_number="", email_address="", feedback=""):
        self.name = name
        self.phone_number = phone_number
        self.email_address = email_address
        self.feedback = feedback

class Teacher:
    def __init__(self, name=""):
        self.name = name
        self.students = [Student() for _ in range(2)]

def give_feedback(student):
    print("\nStudent Information:")
    print(f"Name: {student.name}")
    print(f"Phone Number: {student.phone_number}")
    print(f"Email Address: {student.email_address}")
    print(f"Feedback: {student.feedback}")
    
    student.feedback = input("\nEnter updated feedback for the student: ")

def add_student(teacher):
    new_student = Student()
    new_student.name = input("\nEnter student name: ")
    new_student.phone_number = input("Enter student phone number: ")
    new_student.email_address = input("Enter student email address: ")
    
    for i in range(len(teacher.students)):
        if not teacher.students[i].name:
            teacher.students[i] = new_student
            print("New student added successfully.")
            break

def delete_student(teacher):
    try:
        index = int(input(f"Enter the index of the student to delete (1-{len(teacher.students)}): ")) - 1
        if 0 <= index < len(teacher.students):
            teacher.students[index] = Student() 
            print("Student deleted successfully.")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input.")

def view_all_feedback(teacher):
    print(f"\nFeedback for students supervised by {teacher.name}:")
    for student in teacher.students:
        if student.name:
            print(f"Student: {student.name}")
            print(f"Feedback: {student.feedback}")

def add_teacher(teachers, num_teachers):
    if num_teachers >= 3:
        print("Cannot add more teachers. Maximum number reached.")
        return num_teachers
    
    new_teacher = Teacher()
    new_teacher.name = input("\nEnter teacher name: ")
    teachers.append(new_teacher)
    
    print("New teacher added successfully.")
    return num_teachers + 1

def delete_teacher(teachers, num_teachers):
    try:
        index = int(input(f"Enter the index of the teacher to delete (1-{num_teachers}): ")) - 1
        if 0 <= index < num_teachers:
            del teachers[index]
            print("Teacher deleted successfully.")
            return num_teachers - 1
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input.")
    
    return num_teachers

def main():
    teachers = [
        Teacher("Teacher1"),
        Teacher("Teacher2"),
        Teacher("Teacher3")
    ]
    
    # Initialize some students
    teachers[0].students[0] = Student("Student1", "111-111-1111", "student1@gmail.com", "")
    teachers[0].students[1] = Student("Student2", "222-222-2222", "student2@gmail.com", "")
    teachers[1].students[0] = Student("Student3", "333-333-3333", "student3@gmail.com", "")
    teachers[1].students[1] = Student("Student4", "444-444-4444", "student4@gmail.com", "")
    teachers[2].students[0] = Student("Student5", "555-555-5555", "student5@gmail.com", "")
    teachers[2].students[1] = Student("Student6", "666-666-6666", "student6@gmail.com", "")
    
    num_teachers = len(teachers)
    
    user_type = int(input("Enter user type (1 for Manager, 2 for Teacher): "))
    
    if user_type == 1:

        while True:
            print("\nManager Menu:")
            print("1. Add Teacher")
            print("2. Delete Teacher")
            print("3. View All Feedback")
            print("0. Exit")
            
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                num_teachers = add_teacher(teachers, num_teachers)
            elif choice == 2:
                num_teachers = delete_teacher(teachers, num_teachers)
            elif choice == 3:
                for teacher in teachers:
                    view_all_feedback(teacher)
            elif choice == 0:
                print("Exiting program.")
                break
            else:
                print("Invalid choice.")
    
    elif user_type == 2:
        teacher_name = input("Enter teacher's name: ")
        
        teacher = next((t for t in teachers if t.name == teacher_name), None)
        
        if teacher:
            print(f"\n\nTeacher: {teacher.name}")
            
            print("Existing students:")
            for idx, student in enumerate(teacher.students):
                if student.name:
                    print(f"{idx + 1}. {student.name}")
            
            while True:
                print("\nMenu:")
                print("1. Give Feedback")
                print("2. Add Student")
                print("3. Delete Student")
                print("0. Exit")
                
                choice = int(input("Enter your choice: "))
                
                if choice == 1:
                    feedback_index = int(input(f"Enter the index of the student to give feedback (1-{len(teacher.students)}): ")) - 1
                    if 0 <= feedback_index < len(teacher.students) and teacher.students[feedback_index].name:
                        give_feedback(teacher.students[feedback_index])
                    else:
                        print("Invalid index or empty student.")
                
                elif choice == 2:
                    add_student(teacher)
                
                elif choice == 3:
                    delete_student(teacher)
                
                elif choice == 0:
                    print("Exiting program.")
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Teacher not found.")
    
    else:
        print("Invalid user type.")

if __name__ == "__main__":
    main()
