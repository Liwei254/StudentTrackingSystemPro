from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle


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


class FeedbackApp(App):
    def build(self):
        self.teachers = [
            Teacher("Teacher1"),
            Teacher("Teacher2"),
            Teacher("Teacher3")
        ]

        # Initialize student data
        self.teachers[0].students[0] = Student("Student1", "111-111-1111", "student1@gmail.com", "")
        self.teachers[0].students[1] = Student("Student2", "222-222-2222", "student2@gmail.com", "")
        self.teachers[1].students[0] = Student("Student3", "333-333-3333", "student3@gmail.com", "")
        self.teachers[1].students[1] = Student("Student4", "444-444-4444", "student4@gmail.com", "")
        self.teachers[2].students[0] = Student("Student5", "555-555-5555", "student5@gmail.com", "")
        self.teachers[2].students[1] = Student("Student6", "666-666-6666", "student6@gmail.com", "")

        # Main Layout
        main_layout = GridLayout(cols=1, padding=10, spacing=10)

        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # Set background color to white
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)

        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Manager Section
        manager_layout = BoxLayout(orientation="vertical", spacing=10)
        manager_layout.add_widget(Label(text="Manager Actions", font_size=20, color=(0, 0, 0, 1), size_hint_y=None, height=40))  # Black text
        manager_layout.add_widget(Button(text="Add Teacher", on_press=self.add_teacher, size_hint_y=None, height=40))
        manager_layout.add_widget(Button(text="Delete Teacher", on_press=self.delete_teacher, size_hint_y=None, height=40))
        manager_layout.add_widget(Button(text="View All Feedback", on_press=self.view_all_feedback, size_hint_y=None, height=40))

        # Teacher Section
        teacher_layout = BoxLayout(orientation="vertical", spacing=10)
        teacher_layout.add_widget(Label(text="Teacher Actions", font_size=20, color=(0, 0, 0, 1), size_hint_y=None, height=40))  # Black text
        teacher_layout.add_widget(Button(text="Manage Teacher", on_press=self.select_teacher, size_hint_y=None, height=40))

        # Add sections to main layout
        main_layout.add_widget(manager_layout)
        main_layout.add_widget(teacher_layout)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_popup(self, title, content):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_layout.add_widget(Label(text=content))
        popup_layout.add_widget(Button(text="Close", size_hint_y=None, height=40, on_press=lambda x: popup.dismiss()))
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        popup.open()

    def add_teacher(self, instance):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        input_name = TextInput(hint_text="Enter teacher name", multiline=False)
        layout.add_widget(input_name)
        layout.add_widget(Button(text="Add", size_hint_y=None, height=40, on_press=lambda x: self.save_teacher(input_name.text, popup)))
        popup = Popup(title="Add Teacher", content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def save_teacher(self, name, popup):
        if name:
            self.teachers.append(Teacher(name))
            self.show_popup("Success", f"Teacher {name} added successfully.")
            popup.dismiss()

    def delete_teacher(self, instance):
        teacher_names = [teacher.name for teacher in self.teachers]
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        teacher_spinner = Spinner(text="Choose a teacher", values=teacher_names)
        layout.add_widget(teacher_spinner)
        layout.add_widget(Button(text="Delete", size_hint_y=None, height=40, on_press=lambda x: self.remove_teacher(teacher_spinner.text, popup)))
        popup = Popup(title="Delete Teacher", content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def remove_teacher(self, name, popup):
        self.teachers = [teacher for teacher in self.teachers if teacher.name != name]
        self.show_popup("Success", f"Teacher {name} deleted.")
        popup.dismiss()

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
            self.show_popup("No Feedback", "No feedback available for any students.")

    def select_teacher(self, instance):
        teacher_names = [teacher.name for teacher in self.teachers]
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        teacher_spinner = Spinner(text="Select a teacher", values=teacher_names)
        layout.add_widget(teacher_spinner)
        layout.add_widget(Button(text="Manage", size_hint_y=None, height=40, on_press=lambda x: self.manage_teacher(teacher_spinner.text, popup)))
        popup = Popup(title="Select Teacher", content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def manage_teacher(self, teacher_name, popup):
        teacher = next((t for t in self.teachers if t.name == teacher_name), None)
        popup.dismiss()
        if teacher:
            layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
            student_spinner = Spinner(text="Select a student", values=[s.name for s in teacher.students if s.name])
            layout.add_widget(student_spinner)
            layout.add_widget(Button(text="Give Feedback", size_hint_y=None, height=40, on_press=lambda x: self.give_feedback(teacher, student_spinner.text, popup)))
            layout.add_widget(Button(text="Add Student", size_hint_y=None, height=40, on_press=lambda x: self.add_student(teacher, popup)))
            layout.add_widget(Button(text="Delete Student", size_hint_y=None, height=40, on_press=lambda x: self.delete_student(teacher, student_spinner.text, popup)))
            popup = Popup(title=f"Manage Teacher: {teacher.name}", content=layout, size_hint=(0.8, 0.6))
            popup.open()

    def give_feedback(self, teacher, student_name, popup):
        student = next((s for s in teacher.students if s.name == student_name), None)
        if student:
            layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
            feedback_input = TextInput(hint_text="Enter feedback", multiline=False)
            layout.add_widget(feedback_input)
            layout.add_widget(Button(text="Submit", size_hint_y=None, height=40, on_press=lambda x: self.save_feedback(student, feedback_input.text, popup)))
            popup.dismiss()
            popup = Popup(title=f"Give Feedback for {student.name}", content=layout, size_hint=(0.8, 0.5))
            popup.open()

    def save_feedback(self, student, feedback, popup):
        student.feedback = feedback
        self.show_popup("Success", f"Feedback updated for {student.name}.")
        popup.dismiss()

    def add_student(self, teacher, popup):
        if len([s for s in teacher.students if s.name]) >= 2:
            self.show_popup("Limit", "Each teacher can only have 2 students.")
            return
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        name_input = TextInput(hint_text="Enter student name", multiline=False)
        phone_input = TextInput(hint_text="Enter phone number", multiline=False)
        email_input = TextInput(hint_text="Enter email address", multiline=False)
        layout.add_widget(name_input)
        layout.add_widget(phone_input)
        layout.add_widget(email_input)
        layout.add_widget(Button(text="Add", size_hint_y=None, height=40, on_press=lambda x: self.save_student(teacher, name_input.text, phone_input.text, email_input.text, popup)))
        popup = Popup(title="Add Student", content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def save_student(self, teacher, name, phone, email, popup):
        new_student = Student(name, phone, email)
        teacher.students.append(new_student)
        self.show_popup("Success", f"Student {name} added successfully.")
        popup.dismiss()

    def delete_student(self, teacher, student_name, popup):
        student = next((s for s in teacher.students if s.name == student_name), None)
        if student:
            teacher.students.remove(student)
            self.show_popup("Success", f"Student {student_name} deleted.")
            popup.dismiss()


if __name__ == "__main__":
    FeedbackApp().run()
