from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class Student:
    def __init__(self, name="", phone_number="", email_address="", feedback=""):
        self.name = name
        self.phone_number = phone_number
        self.email_address = email_address
        self.feedback = feedback

class Teacher:
    def __init__(self, name=""):
        self.name = name
        self.students = []

class ManagerScreen(Screen):
    def __init__(self, teachers, **kwargs):
        super().__init__(**kwargs)
        self.teachers = teachers
        layout = BoxLayout(orientation='vertical')

        # Label for Manager Menu
        self.label = Label(text="Manager Menu", font_size=24)
        layout.add_widget(self.label)

        # TextInput for Teacher Name
        self.teacher_name_input = TextInput(hint_text="Enter Teacher Name", multiline=False)
        layout.add_widget(self.teacher_name_input)

        # Add Teacher Button
        self.add_teacher_btn = Button(text="Add Teacher")
        self.add_teacher_btn.bind(on_press=self.add_teacher)
        layout.add_widget(self.add_teacher_btn)

        # Delete Teacher Button
        self.delete_teacher_btn = Button(text="Delete Last Teacher")
        self.delete_teacher_btn.bind(on_press=self.delete_teacher)
        layout.add_widget(self.delete_teacher_btn)

        # View All Feedback Button
        self.view_feedback_btn = Button(text="View All Feedback")
        self.view_feedback_btn.bind(on_press=self.view_all_feedback)
        layout.add_widget(self.view_feedback_btn)

        # Exit Button
        self.exit_btn = Button(text="Exit", on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(self.exit_btn)

        self.add_widget(layout)

    def add_teacher(self, instance):
        teacher_name = self.teacher_name_input.text.strip()
        if teacher_name:
            new_teacher = Teacher(name=teacher_name)
            self.teachers.append(new_teacher)
            self.label.text = f"Added teacher: {new_teacher.name}"
            self.teacher_name_input.text = ""  # Clear the input field after adding
        else:
            self.label.text = "Please enter a valid teacher name."

    def delete_teacher(self, instance):
        if self.teachers:
            removed_teacher = self.teachers.pop()
            self.label.text = f"Deleted teacher: {removed_teacher.name}"
        else:
            self.label.text = "No teachers to delete."

    def view_all_feedback(self, instance):
        feedback_text = "\n".join(
            f"Teacher: {teacher.name}\nFeedback: {[student.feedback for student in teacher.students if student.name]}"
            for teacher in self.teachers
        )
        self.label.text = feedback_text if feedback_text else "No feedback available."


class TeacherScreen(Screen):
    def __init__(self, teacher, **kwargs):
        super().__init__(**kwargs)
        self.teacher = teacher
        layout = BoxLayout(orientation='vertical')

        # Label for Teacher Menu
        self.label = Label(text=f"Teacher: {self.teacher.name}", font_size=24)
        layout.add_widget(self.label)

        # TextInput for Student Name
        self.student_name_input = TextInput(hint_text="Enter Student Name", multiline=False)
        layout.add_widget(self.student_name_input)

        # Add Student Button
        self.add_student_btn = Button(text="Add Student")
        self.add_student_btn.bind(on_press=self.add_student)
        layout.add_widget(self.add_student_btn)

        # Delete Student Button
        self.delete_student_btn = Button(text="Delete Last Student")
        self.delete_student_btn.bind(on_press=self.delete_student)
        layout.add_widget(self.delete_student_btn)

        # Give Feedback Button
        self.give_feedback_btn = Button(text="Give Feedback to First Student")
        self.give_feedback_btn.bind(on_press=self.give_feedback)
        layout.add_widget(self.give_feedback_btn)

        # Exit Button
        self.exit_btn = Button(text="Exit", on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(self.exit_btn)

        self.add_widget(layout)

    def add_student(self, instance):
        student_name = self.student_name_input.text.strip()
        if student_name:
            new_student = Student(name=student_name)
            self.teacher.students.append(new_student)
            self.label.text = f"Added student: {new_student.name}"
            self.student_name_input.text = ""  # Clear the input field after adding
        else:
            self.label.text = "Please enter a valid student name."

    def delete_student(self, instance):
        if self.teacher.students:
            removed_student = self.teacher.students.pop()
            self.label.text = f"Deleted student: {removed_student.name}"
        else:
            self.label.text = "No students to delete."

    def give_feedback(self, instance):
        if self.teacher.students:
            student = self.teacher.students[0]  # For simplicity, we use the first student
            student.feedback = "Updated feedback."
            self.label.text = f"Feedback updated for {student.name}."
        else:
            self.label.text = "No students available for feedback."


class RoleSelectionScreen(Screen):
    def __init__(self, screen_manager, teachers, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.teachers = teachers

        layout = BoxLayout(orientation='vertical')

        # Role Selection Label
        self.label = Label(text="Select Role", font_size=24)
        layout.add_widget(self.label)

        # Manager Button
        self.manager_btn = Button(text="Manager", font_size=18)
        self.manager_btn.bind(on_press=self.go_to_manager_screen)
        layout.add_widget(self.manager_btn)

        # Teacher Button
        self.teacher_btn = Button(text="Teacher", font_size=18)
        self.teacher_btn.bind(on_press=self.go_to_teacher_screen)
        layout.add_widget(self.teacher_btn)

        self.add_widget(layout)

    def go_to_manager_screen(self, instance):
        self.screen_manager.current = 'manager'

    def go_to_teacher_screen(self, instance):
        # Automatically select the first teacher for now
        if self.teachers:
            self.screen_manager.current = 'teacher'
        else:
            self.label.text = "No teachers available. Please add a teacher first."


class FeedbackApp(App):
    def build(self):
        self.teachers = []

        # Create screen manager and add screens
        sm = ScreenManager()
        sm.add_widget(RoleSelectionScreen(screen_manager=sm, teachers=self.teachers, name="role_selection"))
        sm.add_widget(ManagerScreen(teachers=self.teachers, name="manager"))

        # Add a placeholder TeacherScreen (the real one will be added dynamically)
        if self.teachers:
            sm.add_widget(TeacherScreen(teacher=self.teachers[0], name="teacher"))
        
        return sm

if __name__ == "__main__":
    FeedbackApp().run()
