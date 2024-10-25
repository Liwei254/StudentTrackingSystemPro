from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

# Set a custom background color for the app
Window.clearcolor = (0.9, 0.9, 0.95, 1)  # Light grey-blue

class Student:
    def __init__(self, name="", feedback=""):
        self.name = name
        self.feedback = feedback

class Teacher:
    def __init__(self, name=""):
        self.name = name
        self.students = []

class TeacherScreen(Screen):
    def __init__(self, teacher, **kwargs):
        super().__init__(**kwargs)
        self.teacher = teacher

        # Outer BoxLayout to center the layout
        outer_layout = BoxLayout(orientation='vertical', padding=20)
        inner_layout = GridLayout(cols=1, spacing=10, row_default_height=40, size_hint=(0.6, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Header label
        self.label = Label(text=f"Teacher: {self.teacher.name}", font_size=24, bold=True, color=(0, 0, 0, 1))
        inner_layout.add_widget(self.label)

        # Input field for adding students
        self.student_name_input = TextInput(hint_text="Enter Student Name", multiline=False, size_hint_y=None, height=30)
        inner_layout.add_widget(self.student_name_input)

        # Add Student button
        self.add_student_btn = Button(text="Add Student", background_color=(0.2, 0.6, 0.8, 1))
        self.add_student_btn.bind(on_press=self.add_student)
        inner_layout.add_widget(self.add_student_btn)

        # Dropdown spinner for deleting students
        self.student_spinner = Spinner(text="Select Student to Delete",
                                       values=[student.name for student in self.teacher.students],
                                       size_hint=(None, None), size=(200, 44))
        inner_layout.add_widget(self.student_spinner)

        # Delete Student button
        self.delete_student_btn = Button(text="Delete Selected Student", background_color=(0.8, 0.4, 0.4, 1))
        self.delete_student_btn.bind(on_press=self.delete_student)
        inner_layout.add_widget(self.delete_student_btn)

        # Feedback button
        self.give_feedback_btn = Button(text="Give Feedback to First Student", background_color=(0.4, 0.8, 0.4, 1))
        self.give_feedback_btn.bind(on_press=self.give_feedback)
        inner_layout.add_widget(self.give_feedback_btn)

        # Exit button
        self.exit_btn = Button(text="Return to Role Selection", background_color=(0.6, 0.6, 0.8, 1))
        self.exit_btn.bind(on_press=lambda x: setattr(App.get_running_app().root, 'current', 'role_selection'))
        inner_layout.add_widget(self.exit_btn)

        # Center the layout
        outer_layout.add_widget(inner_layout)
        self.add_widget(outer_layout)

    def add_student(self, instance):
        student_name = self.student_name_input.text.strip()
        if student_name:
            new_student = Student(name=student_name)
            self.teacher.students.append(new_student)
            self.label.text = f"Added student: {new_student.name}"
            self.student_name_input.text = ""
            self.student_spinner.values = [student.name for student in self.teacher.students]
        else:
            self.label.text = "Please enter a valid student name."

    def delete_student(self, instance):
        selected_student_name = self.student_spinner.text
        student_to_delete = next((student for student in self.teacher.students if student.name == selected_student_name), None)
        if student_to_delete:
            self.teacher.students.remove(student_to_delete)
            self.label.text = f"Deleted student: {student_to_delete.name}"
            self.student_spinner.values = [student.name for student in self.teacher.students]
        else:
            self.label.text = "No student selected or available."

    def give_feedback(self, instance):
        if self.teacher.students:
            student = self.teacher.students[0]
            student.feedback = "Updated feedback."
            self.label.text = f"Feedback updated for {student.name}."
        else:
            self.label.text = "No students available for feedback."

class RoleSelectionScreen(Screen):
    def __init__(self, screen_manager, teachers, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.teachers = teachers

        # Outer BoxLayout to center the layout
        outer_layout = BoxLayout(orientation='vertical', padding=20)
        inner_layout = GridLayout(cols=1, spacing=10, row_default_height=40, size_hint=(0.6, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Header label
        self.label = Label(text="Select Role", font_size=24, bold=True, color=(0, 0, 0, 1))
        inner_layout.add_widget(self.label)

        # Manager button
        self.manager_btn = Button(text="Manager", font_size=18, background_color=(0.4, 0.8, 0.6, 1))
        self.manager_btn.bind(on_press=self.go_to_manager_screen)
        inner_layout.add_widget(self.manager_btn)

        # Teacher button
        self.teacher_btn = Button(text="Teacher", font_size=18, background_color=(0.6, 0.4, 0.8, 1))
        self.teacher_btn.bind(on_press=self.go_to_teacher_screen)
        inner_layout.add_widget(self.teacher_btn)

        # Center the layout
        outer_layout.add_widget(inner_layout)
        self.add_widget(outer_layout)

    def go_to_manager_screen(self, instance):
        self.screen_manager.current = 'manager'

    def go_to_teacher_screen(self, instance):
        if self.teachers:
            teacher = self.teachers[0]
            if 'teacher' in self.screen_manager.screen_names:
                self.screen_manager.remove_widget(self.screen_manager.get_screen('teacher'))
            self.screen_manager.add_widget(TeacherScreen(teacher=teacher, name='teacher'))
            self.screen_manager.current = 'teacher'
        else:
            self.label.text = "No teachers available. Please add a teacher first."

class ManagerScreen(Screen):
    def __init__(self, teachers, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.teachers = teachers
        self.screen_manager = screen_manager

        # Outer BoxLayout to center the layout
        outer_layout = BoxLayout(orientation='vertical', padding=20)
        inner_layout = GridLayout(cols=1, spacing=10, row_default_height=40, size_hint=(0.6, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Header label
        self.label = Label(text="Manager Menu", font_size=24, bold=True, color=(0, 0, 0, 1))
        inner_layout.add_widget(self.label)

        # Input for teacher name
        self.teacher_name_input = TextInput(hint_text="Enter Teacher Name", multiline=False, size_hint_y=None, height=30)
        inner_layout.add_widget(self.teacher_name_input)

        # Add Teacher button
        self.add_teacher_btn = Button(text="Add Teacher", background_color=(0.2, 0.6, 0.8, 1))
        self.add_teacher_btn.bind(on_press=self.add_teacher)
        inner_layout.add_widget(self.add_teacher_btn)

        # Dropdown for selecting teacher to delete
        self.teacher_spinner = Spinner(text="Select Teacher to Delete",
                                       values=[teacher.name for teacher in self.teachers],
                                       size_hint=(None, None), size=(200, 44))
        inner_layout.add_widget(self.teacher_spinner)

        # Delete Teacher button
        self.delete_teacher_btn = Button(text="Delete Selected Teacher", background_color=(0.8, 0.4, 0.4, 1))
        self.delete_teacher_btn.bind(on_press=self.delete_teacher)
        inner_layout.add_widget(self.delete_teacher_btn)

        # View All Feedback button
        self.view_feedback_btn = Button(text="View All Feedback", background_color=(0.4, 0.8, 0.4, 1))
        self.view_feedback_btn.bind(on_press=self.view_all_feedback)
        inner_layout.add_widget(self.view_feedback_btn)

        # Return button
        self.exit_btn = Button(text="Return to Role Selection", background_color=(0.6, 0.6, 0.8, 1))
        self.exit_btn.bind(on_press=self.return_to_role_selection)
        inner_layout.add_widget(self.exit_btn)

        # Center the layout
        outer_layout.add_widget(inner_layout)
        self.add_widget(outer_layout)

    def add_teacher(self, instance):
        teacher_name = self.teacher_name_input.text.strip()
        if teacher_name:
            new_teacher = Teacher(name=teacher_name)
            self.teachers.append(new_teacher)
            self.teacher_spinner.values = [teacher.name for teacher in self.teachers]
            self.teacher_name_input.text = ""
            self.label.text = f"Added teacher: {new_teacher.name}"
        else:
            self.label.text = "Please enter a valid teacher name."

    def delete_teacher(self, instance):
        selected_teacher_name = self.teacher_spinner.text
        teacher_to_delete = next((teacher for teacher in self.teachers if teacher.name == selected_teacher_name), None)
        if teacher_to_delete:
            self.teachers.remove(teacher_to_delete)
            self.teacher_spinner.values = [teacher.name for teacher in self.teachers]
            self.label.text = f"Deleted teacher: {teacher_to_delete.name}"
        else:
            self.label.text = "No teacher selected or available."

    def view_all_feedback(self, instance):
        feedback_text = "\n".join([f"{teacher.name}: {', '.join([student.feedback for student in teacher.students])}" for teacher in self.teachers if teacher.students])
        self.label.text = f"All Feedback:\n{feedback_text}" if feedback_text else "No feedback available."

    def return_to_role_selection(self, instance):
        self.screen_manager.current = 'role_selection'

class FeedbackApp(App):
    def build(self):
        sm = ScreenManager()
        teachers = []
        sm.add_widget(RoleSelectionScreen(screen_manager=sm, teachers=teachers, name='role_selection'))
        sm.add_widget(ManagerScreen(teachers=teachers, screen_manager=sm, name='manager'))
        return sm

if __name__ == '__main__':
    FeedbackApp().run()
