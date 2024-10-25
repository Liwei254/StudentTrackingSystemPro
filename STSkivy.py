from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Define the data classes for Students and Teachers
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

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teachers = [Teacher("Teacher1"), Teacher("Teacher2"), Teacher("Teacher3")]
        self.build_main_menu()

    def build_main_menu(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text="Teacher-Student Feedback System", font_size=24))

        add_teacher_btn = Button(text="Add Teacher", size_hint=(1, 0.2))
        add_teacher_btn.bind(on_press=self.add_teacher)
        layout.add_widget(add_teacher_btn)

        delete_teacher_btn = Button(text="Delete Teacher", size_hint=(1, 0.2))
        delete_teacher_btn.bind(on_press=self.delete_teacher)
        layout.add_widget(delete_teacher_btn)

        view_feedback_btn = Button(text="View All Feedback", size_hint=(1, 0.2))
        view_feedback_btn.bind(on_press=self.view_all_feedback)
        layout.add_widget(view_feedback_btn)

        manage_teacher_btn = Button(text="Manage Teacher", size_hint=(1, 0.2))
        manage_teacher_btn.bind(on_press=self.go_to_manage_teacher)
        layout.add_widget(manage_teacher_btn)

        self.add_widget(layout)

    def add_teacher(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_field = TextInput(hint_text="Enter teacher's name")
        content.add_widget(input_field)

        add_button = Button(text="Add")
        add_button.bind(on_press=lambda x: self.add_teacher_to_list(input_field.text))
        add_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(add_button)

        popup = Popup(title="Add Teacher", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def add_teacher_to_list(self, teacher_name):
        if teacher_name:
            self.teachers.append(Teacher(name=teacher_name))

    def delete_teacher(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_field = TextInput(hint_text="Enter teacher's name to delete")
        content.add_widget(input_field)

        delete_button = Button(text="Delete")
        delete_button.bind(on_press=lambda x: self.delete_teacher_from_list(input_field.text))
        delete_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(delete_button)

        popup = Popup(title="Delete Teacher", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def delete_teacher_from_list(self, teacher_name):
        self.teachers = [teacher for teacher in self.teachers if teacher.name != teacher_name]

    def view_all_feedback(self, instance):
        feedback_text = ""
        for teacher in self.teachers:
            feedback_text += f"\nFeedback for {teacher.name}'s students:\n"
            for student in teacher.students:
                if student.name:
                    feedback_text += f"Student: {student.name}, Feedback: {student.feedback}\n"
        if feedback_text:
            self.show_popup("All Feedback", feedback_text)
        else:
            self.show_popup("All Feedback", "No feedback available for any students.")

    def go_to_manage_teacher(self, instance):
        self.manager.current = "manage_teacher"

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.7, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class ManageTeacherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teacher = None
        self.build_teacher_menu()

    def build_teacher_menu(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text="Manage Teacher", font_size=24))

        self.teacher_name_input = TextInput(hint_text="Enter teacher name", size_hint=(1, 0.2))
        layout.add_widget(self.teacher_name_input)

        select_teacher_btn = Button(text="Select Teacher", size_hint=(1, 0.2))
        select_teacher_btn.bind(on_press=self.select_teacher)
        layout.add_widget(select_teacher_btn)

        add_student_btn = Button(text="Add Student", size_hint=(1, 0.2))
        add_student_btn.bind(on_press=self.add_student)
        layout.add_widget(add_student_btn)

        delete_student_btn = Button(text="Delete Student", size_hint=(1, 0.2))
        delete_student_btn.bind(on_press=self.delete_student)
        layout.add_widget(delete_student_btn)

        give_feedback_btn = Button(text="Give Feedback", size_hint=(1, 0.2))
        give_feedback_btn.bind(on_press=self.give_feedback)
        layout.add_widget(give_feedback_btn)

        back_btn = Button(text="Back to Main Menu", size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back_to_main)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def select_teacher(self, instance):
        teacher_name = self.teacher_name_input.text
        self.teacher = next((t for t in self.manager.get_screen("main").teachers if t.name == teacher_name), None)
        if self.teacher:
            self.teacher_name_input.hint_text = f"Managing {self.teacher.name}"
        else:
            self.show_popup("Error", "Teacher not found.")

    def add_student(self, instance):
        if not self.teacher:
            self.show_popup("Error", "No teacher selected.")
            return

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        name_input = TextInput(hint_text="Student Name")
        phone_input = TextInput(hint_text="Phone Number")
        email_input = TextInput(hint_text="Email Address")

        content.add_widget(name_input)
        content.add_widget(phone_input)
        content.add_widget(email_input)

        add_button = Button(text="Add")
        add_button.bind(on_press=lambda x: self.add_student_to_teacher(name_input.text, phone_input.text, email_input.text))
        add_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(add_button)

        popup = Popup(title="Add Student", content=content, size_hint=(0.7, 0.5))
        popup.open()

    def add_student_to_teacher(self, name, phone, email):
        if name and phone and email:
            new_student = Student(name=name, phone_number=phone, email_address=email)
            self.teacher.students.append(new_student)

    def delete_student(self, instance):
        if not self.teacher:
            self.show_popup("Error", "No teacher selected.")
            return

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        student_input = TextInput(hint_text="Enter student name to delete")
        content.add_widget(student_input)

        delete_button = Button(text="Delete")
        delete_button.bind(on_press=lambda x: self.delete_student_from_teacher(student_input.text))
        delete_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(delete_button)

        popup = Popup(title="Delete Student", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def delete_student_from_teacher(self, student_name):
        self.teacher.students = [s for s in self.teacher.students if s.name != student_name]

    def give_feedback(self, instance):
        if not self.teacher:
            self.show_popup("Error", "No teacher selected.")
            return

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        student_name_input = TextInput(hint_text="Student Name")
        feedback_input = TextInput(hint_text="Enter feedback")
        
        content.add_widget(student_name_input)
        content.add_widget(feedback_input)

        submit_button = Button(text="Submit")
        submit_button.bind(on_press=lambda x: self.give_feedback_to_student(student_name_input.text, feedback_input.text))
        submit_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(submit_button)

        popup = Popup(title="Give Feedback", content=content, size_hint=(0.7, 0.5))
        popup.open()

    def give_feedback_to_student(self, student_name, feedback):
        student = next((s for s in self.teacher.students if s.name == student_name), None)
        if student:
            student.feedback = feedback
        else:
            self.show_popup("Error", "Student not found.")

    def go_back_to_main(self, instance):
        self.manager.current = "main"

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.7, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class FeedbackApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(ManageTeacherScreen(name="manage_teacher"))
        return sm

if __name__ == "__main__":
    FeedbackApp().run()
