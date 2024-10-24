from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

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
    def __init__(self, teachers, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.teachers = teachers
        self.screen_manager = screen_manager
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

        # Spinner for Teacher Selection (Dropdown)
        self.teacher_spinner = Spinner(text="Select Teacher to Delete",
                                       values=[teacher.name for teacher in self.teachers],
                                       size_hint=(None, None), size=(200, 44))
        layout.add_widget(self.teacher_spinner)

        # Delete Teacher Button
        self.delete_teacher_btn = Button(text="Delete Selected Teacher")
        self.delete_teacher_btn.bind(on_press=self.delete_teacher)
        layout.add_widget(self.delete_teacher_btn)

        # View All Feedback Button
        self.view_feedback_btn = Button(text="View All Feedback")
        self.view_feedback_btn.bind(on_press=self.view_all_feedback)
        layout.add_widget(self.view_feedback_btn)

        # Exit Button (to return to role selection)
        self.exit_btn = Button(text="Return to Role Selection")
        self.exit_btn.bind(on_press=self.return_to_role_selection)
        layout.add_widget(self.exit_btn)

        self.add_widget(layout)

    def add_teacher(self, instance):
        teacher_name = self.teacher_name_input.text.strip()
        if teacher_name:
            new_teacher = Teacher(name=teacher_name)
            self.teachers.append(new_teacher)
            self.label.text = f"Added teacher: {new_teacher.name}"
            self.teacher_name_input.text = ""  # Clear the input field after adding

            # Update the spinner with new teacher list
            self.teacher_spinner.values = [teacher.name for teacher in self.teachers]
        else:
            self.label.text = "Please enter a valid teacher name."

    def delete_teacher(self, instance):
        selected_teacher_name = self.teacher_spinner.text
        teacher_to_delete = next((teacher for teacher in self.teachers if teacher.name == selected_teacher_name), None)

        if teacher_to_delete:
            self.teachers.remove(teacher_to_delete)
            self.label.text = f"Deleted teacher: {teacher_to_delete.name}"

            # Update the spinner with updated teacher list
            if self.teachers:
                self.teacher_spinner.values = [teacher.name for teacher in self.teachers]
                self.teacher_spinner.text = "Select Teacher to Delete"
            else:
                self.teacher_spinner.values = []
                self.teacher_spinner.text = "No Teachers Available"
        else:
            self.label.text = "No teacher selected or available."

    def view_all_feedback(self, instance):
        feedback_text = "\n".join(
            f"Teacher: {teacher.name}\nFeedback: {[student.feedback for student in teacher.students if student.name]}"
            for teacher in self.teachers
        )
        self.label.text = feedback_text if feedback_text else "No feedback available."

    def return_to_role_selection(self, instance):
        self.screen_manager.current = 'role_selection'  # Go back to the Role Selection screen


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

        # Exit Button (return to role selection screen)
        self.exit_btn = Button(text="Return to Role Selection")
        self.exit_btn.bind(on_press=lambda x: setattr(App.get_running_app().root, 'current', 'role_selection'))
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
        if self.teachers:
            # Create the teacher screen dynamically and switch to it
            teacher = self.teachers[0]  # You can implement a selection process here if needed
            if 'teacher' in self.screen_manager.screen_names:
                self.screen_manager.remove_widget(self.screen_manager.get_screen('teacher'))
            self.screen_manager.add_widget(TeacherScreen(teacher=teacher, name='teacher'))
            self.screen_manager.current = 'teacher'
        else:
            self.label.text = "No teachers available. Please add a teacher first."


class FeedbackApp(App):
    def build(self):
        self.teachers = []

        # Create screen manager and add screens
        sm = ScreenManager()
        sm.add_widget(RoleSelectionScreen(screen_manager=sm, teachers=self.teachers, name="role_selection"))
        sm.add_widget(ManagerScreen(teachers=self.teachers, screen_manager=sm, name="manager"))

        return sm


if __name__ == "__main__":
    FeedbackApp().run()
