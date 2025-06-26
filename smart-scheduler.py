import datetime

exams = {}

def dates(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def times(time):
    try:
        datetime.datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False

def calculate_duration(start, end):
    Hour_min = "%H:%M"
    starttime = datetime.datetime.strptime(start, Hour_min)
    endtime = datetime.datetime.strptime(end, Hour_min)
    if endtime <= starttime:
        return None
    Hours = endtime - starttime
    total_minutes = int(Hours.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"

def add_exam():
    while True:
        code = input("Enter exam code (Ex. MATH112): ").strip().upper()
        if 5 <= len(code) <= 10 and " " not in code:
            if code in exams:
                print("This exam code already exists.\n")
                return
            break
        print("Code must be 5 to 10 characters with no spaces.")

    name = input("Enter exam name: ").strip()

    while True:
        date = input("Enter exam date (YYYY-MM-DD): ").strip()
        if dates(date):
            break
        print("Invalid date format.")

    while True:
        start = input("Enter start time (HH:MM): ").strip()
        if times(start):
            break
        print("Invalid start time.")

    while True:
        end = input("Enter end time (HH:MM): ").strip()
        if times(end):
            duration = calculate_duration(start, end)
            if duration:
                break
        print("End time must be after start time, in HH:MM format.")

    room = input("Enter exam room: ").strip()

    for exam in exams.values():
        if exam["date"] == date and (
            exam["start_time"] < end and start < exam["end_time"]
        ):
            print(f"Conflict with another exam on {date} from {exam['start_time']} to {exam['end_time']}.\n")
            return

    exams[code] = {
        "name": name,
        "date": date,
        "start_time": start,
        "end_time": end,
        "duration": duration,
        "room": room
    }
    print(f"✅ Exam added successfully! Duration: {duration}\n")

def view_exams():
    if not exams:
        print(" No exams scheduled.\n")
        return
    print("\n📋 Scheduled Exams:")
    for code, info in exams.items():
        print(f"\nExamCode {code}")
        for key, val in info.items():
            print(f"   {key.replace('_', ' ').capitalize()}: {val}")
    print()

def edit_exam():
    code = input("Enter exam code to edit: ").strip().upper()
    if code not in exams:
        print("Exam not found.\n")
        return

    print("Leave fields blank to keep current value.")
    for field in ["name", "date", "start_time", "end_time", "room"]:
        current = exams[code][field]
        new_val = input(f"{field.replace('_', ' ').capitalize()} [{current}]: ").strip()
        if new_val:
            if field == "date" and not dates(new_val):
                print("Invalid date. Edit canceled.\n")
                return
            if field in ["start_time", "end_time"] and not times(new_val):
                print("Invalid time. Edit canceled.\n")
                return
            exams[code][field] = new_val

    s = exams[code]["start_time"]
    e = exams[code]["end_time"]
    new_duration = calculate_duration(s, e)
    if not new_duration:
        print("End time must be after start time. Edit canceled.\n")
        return
    exams[code]["duration"] = new_duration
    print("Exam updated successfully!\n")

def delete_exam():
    code = input("Enter exam code to delete: ").strip().upper()
    if exams.pop(code, None):
        print("Exam deleted.\n")
    else:
        print("Exam not found.\n")

def menu():
    while True:
        print("=== SMART SCHEDULER ===")
        print("1. Add Exam")
        print("2. View Exams")
        print("3. Edit Exam")
        print("4. Delete Exam")
        print("5. Exit")
        choice = input("Enter a number from (1–5): ").strip()

        if choice == "1":
            add_exam()
        elif choice == "2":
            view_exams()
        elif choice == "3":
            edit_exam()
        elif choice == "4":
            delete_exam()
        elif choice == "5":
            print("👋 Goodbye!\n")
            break
        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    menu()
