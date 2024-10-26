from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
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
        self.main_layout = BoxLayout(orientation="vertical", padding=200, spacing=10)

        # Set background color
        with self.main_layout.canvas.before:
            Color(0.9608, 0.9608, 0.9804, 1)  # #F5F5FA in RGBA
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self.update_rect, pos=self.update_rect)

        # Home Screen
        self.show_home_screen()

        return self.main_layout

    def update_rect(self, *args):
        self.rect.size = self.main_layout.size
        self.rect.pos = self.main_layout.pos

    def show_home_screen(self):
        self.main_layout.clear_widgets()
        home_layout = BoxLayout(orientation="vertical", spacing=30, padding=10)
        home_layout.add_widget(Label(text="Welcome to the Feedback System", font_size=24, color=(0.396, 0.607, 0.749, 1), size_hint_y=None, height=50))
        
        # MANAGER Button
        manager_button = Button(text="MANAGER", size_hint_y=None, height=50)
        manager_button.bind(on_press=self.show_manager_actions)
        home_layout.add_widget(manager_button)

        # TEACHER Button
        teacher_button = Button(text="TEACHER", size_hint_y=None, height=50)
        teacher_button.bind(on_press=self.show_teacher_actions)
        home_layout.add_widget(teacher_button)

        self.main_layout.add_widget(home_layout)

    def show_manager_actions(self, instance):
        self.main_layout.clear_widgets()
        manager_layout = BoxLayout(orientation="vertical", spacing=10)

        manager_layout.add_widget(Label(text="Manager Actions", font_size=20, color=(0.396, 0.607, 0.749, 1), size_hint_y=None, height=40))
        manager_layout.add_widget(Button(text="Add Teacher", on_press=self.add_teacher, size_hint_y=None, height=40))
        manager_layout.add_widget(Button(text="Delete Teacher", on_press=self.delete_teacher, size_hint_y=None, height=40))
        manager_layout.add_widget(Button(text="View All Feedback", on_press=self.view_all_feedback, size_hint_y=None, height=40))

        # Back Button to return to Home
        back_button = Button(text="Back to Home", size_hint_y=None, height=40)
        back_button.bind(on_press=lambda x: self.show_home_screen())
        manager_layout.add_widget(back_button)

        self.main_layout.add_widget(manager_layout)

    def show_teacher_actions(self, instance):
        self.main_layout.clear_widgets()
        teacher_layout = BoxLayout(orientation="vertical", spacing=10)

        teacher_layout.add_widget(Label(text="Teacher Actions", font_size=20, color=(0.396, 0.607, 0.749, 1), size_hint_y=None, height=40))
        teacher_layout.add_widget(Button(text="Manage Your Students", on_press=self.select_teacher, size_hint_y=None, height=40))

        # Back Button to return to Home
        back_button = Button(text="Back to Home", size_hint_y=None, height=40)
        back_button.bind(on_press=lambda x: self.show_home_screen())
        teacher_layout.add_widget(back_button)

        self.main_layout.add_widget(teacher_layout)

    def show_popup(self, title, content):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_layout.add_widget(Label(text=content))
        close_button = Button(text="Close", size_hint_y=None, height=40)
        close_button.bind(on_press=lambda x: popup.dismiss())
        popup_layout.add_widget(close_button)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.4, 0.3))
        popup.open()

    def add_teacher(self, instance):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        input_name = TextInput(hint_text="Enter teacher name", multiline=False)
        layout.add_widget(input_name)
        add_button = Button(text="Add", size_hint_y=None, height=40)
        layout.add_widget(add_button)
        add_button.bind(on_press=lambda x: self.save_teacher(input_name.text, popup))
        popup = Popup(title="Add Teacher", content=layout, size_hint=(0.4, 0.3))
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
        delete_button = Button(text="Delete", size_hint_y=None, height=40)
        layout.add_widget(delete_button)
        delete_button.bind(on_press=lambda x: self.remove_teacher(teacher_spinner.text, popup))
        popup = Popup(title="Delete Teacher", content=layout, size_hint=(0.4, 0.3))
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
            layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
            
            # Add a ScrollView for the feedback content
            scroll_view = ScrollView(size_hint=(1, 1))  # Keep it simple and scrollable
            feedback_label = Label(text=feedback_text, size_hint_y=None)
            feedback_label.bind(texture_size=feedback_label.setter('size'))  # Auto-resize label height
            scroll_view.add_widget(feedback_label)
            
            layout.add_widget(scroll_view)
            
            close_button = Button(text="Close", size_hint_y=None, height=40)
            close_button.bind(on_press=lambda x: popup.dismiss())
            layout.add_widget(close_button)
            
            popup = Popup(title="All Feedback", content=layout, size_hint=(0.6, 0.6))
            popup.open()
        else:
            self.show_popup("No Feedback", "No feedback available for any students.")

    def select_teacher(self, instance):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        teacher_names = [teacher.name for teacher in self.teachers]
        teacher_spinner = Spinner(text="Choose a teacher", values=teacher_names)
        layout.add_widget(teacher_spinner)

        manage_button = Button(text="Manage Students", size_hint_y=None, height=40)
        layout.add_widget(manage_button)
        manage_button.bind(on_press=lambda x: self.manage_teacher(teacher_spinner.text))

        popup = Popup(title="Select Teacher", content=layout, size_hint=(0.4, 0.4))
        popup.open()

    def manage_teacher(self, teacher_name):
        teacher = next((t for t in self.teachers if t.name == teacher_name), None)
        if teacher:
            layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

            student_names = [student.name for student in teacher.students]
            student_spinner = Spinner(text="Choose a student", values=student_names)
            layout.add_widget(student_spinner)

            view_feedback_button = Button(text="View Feedback", size_hint_y=None, height=40)
            layout.add_widget(view_feedback_button)
            view_feedback_button.bind(on_press=lambda x: self.view_student_feedback(teacher, student_spinner.text))

            add_feedback_button = Button(text="Add Feedback", size_hint_y=None, height=40)
            layout.add_widget(add_feedback_button)
            add_feedback_button.bind(on_press=lambda x: self.give_feedback(teacher, student_spinner.text))

            manage_popup = Popup(title="Manage Teacher", content=layout, size_hint=(0.4, 0.5))
            manage_popup.open()

    def view_student_feedback(self, teacher, student_name):
        student = next((s for s in teacher.students if s.name == student_name), None)
        if student:
            self.show_popup(f"Feedback for {student.name}", student.feedback or "No feedback provided yet.")

    def give_feedback(self, teacher, student_name):
        student = next((s for s in teacher.students if s.name == student_name), None)
        if student:
            layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
            feedback_input = TextInput(text=student.feedback, hint_text="Enter feedback", multiline=True)
            layout.add_widget(feedback_input)
            save_button = Button(text="Save Feedback", size_hint_y=None, height=40)
            layout.add_widget(save_button)
            save_button.bind(on_press=lambda x: self.save_feedback(student, feedback_input.text, popup))
            popup = Popup(title=f"Give Feedback for {student.name}", content=layout, size_hint=(0.6, 0.5))
            popup.open()

    def save_feedback(self, student, feedback, popup):
        student.feedback = feedback
        self.show_popup("Success", "Feedback saved.")
        popup.dismiss()


if __name__ == "__main__":
    FeedbackApp().run()
