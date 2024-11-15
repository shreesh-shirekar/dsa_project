from datetime import datetime, timedelta
import time
import schedule
from collections import defaultdict
import threading

# List to store class information
classes = []
# Dictionary to store student registrations for each class by subject
student_registration = defaultdict(list)

def schedule_class(subject, date, time_str, teacher):
    try:
        date_time = datetime.strptime(date + " " + time_str, "%d-%m-%Y %H:%M")
        classes.append({
            'subject': subject,
            'date_time': date_time,
            'teacher': teacher
        })
        print(f"Class scheduled: {subject} on {date_time} by {teacher}")
    except ValueError:
        print("Invalid date or time format. Please use DD-MM-YYYY for date and HH:MM for time.")

def register_student(student_name, section_number, student_email):
    # Check if the section number is valid
    emails = []
    if 0 <= section_number < len(classes):
        subject = classes[section_number]['subject']
        student_registration[subject].append(student_name)
        emails.append(student_email)
        print(f"Student {student_name} registered for {subject}")
    else:
        print("Invalid class index. Please enter a valid index.")

def view_classes():
    if not classes:
        print("No classes scheduled.")
        return
    for i, cls in enumerate(classes):
        print(f"{i}: {cls['subject']} - {cls['date_time']} (Teacher: {cls['teacher']})")

# Function to send reminders
# def send_reminders():
#     current_time = datetime.now()
#     for cls in classes:
#         time_diff = cls['date_time'] - current_time
#         if timedelta(minutes=0) < time_diff < timedelta(minutes=30):
#             subject = cls['subject']
#             students = student_registration[subject]
#             for student in students:
#                 print(f"Reminder: {student}, your class '{subject}' starts at {cls['date_time']}")

# # Automated reminder system
# def start_reminder_system():
#     def run_reminder_system():
#         while True:
#             schedule.run_pending()
#             time.sleep(1)

#     reminder_thread = threading.Thread(target=run_reminder_system)
#     reminder_thread.daemon = True  # This allows the thread to exit when the main program exits
#     reminder_thread.start()
#     schedule.every(1).minute.do(send_reminders)

def main():
    while True:
        print("\n1. Schedule a class")
        print("2. Register a student")
        print("3. View scheduled classes")
        # print("4. Start reminder system")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            subject = input("Enter subject: ")
            date = input("Enter date (DD-MM-YYYY): ")
            time_str = input("Enter time (HH:MM, 24-hour format): ")
            teacher = input("Enter teacher's name: ")
            schedule_class(subject, date, time_str, teacher)
        
        elif choice == '2':
            view_classes()  # Show available classes
            if classes:  # Only prompt for student registration if there are classes
                try:
                    section_number = int(input(f"Enter Section (index from 0 to {len(classes) - 1}): "))
                    student_name = input("Enter student name: ")
                    student_email = input("Enter student email address: ")
                    register_student(student_name, section_number, student_email)
                except ValueError:
                    print("Invalid input. Please enter a valid section index.")
        
        elif choice == '3':
            view_classes()
        
        # elif choice == '4':
        #     print("Starting reminder system...")
        #     start_reminder_system()
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
        