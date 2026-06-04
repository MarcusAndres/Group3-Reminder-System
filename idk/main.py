import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# ======================================
# CUSTOMIZATION
# ======================================
WINDOW_WIDTH = 865
WINDOW_HEIGHT = 700
HEADER_COLOR = "#363955"
UPCOMING_COLOR = "#59598E"
INPUT_COLOR = "#54668E"
REMINDER_COLOR = "#363955"
BACKGROUND_COLOR = "#879EC6"

# ======================================
# MAIN WINDOW
# ======================================
root = tk.Tk()
root.title("Reminder System")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=BACKGROUND_COLOR)
root.resizable(False,False)
notifications = []  # List of dicts: {"time": str, "message": str, "notified": bool}


# ======================================
# HELPER FUNCTIONS
# ======================================
def get_reminder_datetime(time_str):
    now = datetime.now()
    try:
        reminder_time = datetime.strptime(time_str, "%I:%M %p")
        reminder = now.replace(
            hour=reminder_time.hour,
            minute=reminder_time.minute,
            second=0,
            microsecond=0
        )
        if reminder < now:
            reminder += timedelta(days=1)
        return reminder
    except:
        return now


# ======================================
# HEADER
# ======================================
header_frame = tk.Frame(root, bg=HEADER_COLOR, bd=15, relief="ridge")
header_frame.place(x=190, y=10, width=485, height=80)

clock_label = tk.Label(header_frame, text="", bg=HEADER_COLOR, fg="white",
                       font=("Segoe UI", 22, "bold"))
clock_label.pack(expand=True)


def update_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    clock_label.config(text=f"Current Time: {now}")
    root.after(1000, update_clock)


update_clock()

# ======================================
# UPCOMING REMINDERS
# ======================================
upcoming_frame = tk.Frame(root, bg=UPCOMING_COLOR, bd=10, relief="ridge")
upcoming_frame.place(x=320, y=100, width=535, height=250)

tk.Label(upcoming_frame, text="Upcoming Reminders", bg=UPCOMING_COLOR, fg="white",
         font=("Segoe UI", 14, "bold")).place(x=160, y=10)

upcoming_tree = ttk.Treeview(upcoming_frame, columns=("time", "message", "left"), show="headings", height=8)
upcoming_tree.heading("time", text="Time")
upcoming_tree.heading("message", text="Message")
upcoming_tree.heading("left", text="Time Left")
upcoming_tree.column("time", width=80)
upcoming_tree.column("message", width=280)
upcoming_tree.column("left", width=120)
upcoming_tree.place(x=13, y=50, width=505, height=180)

# ======================================
# INPUT FRAME
# ======================================
input_frame = tk.Frame(root, bg=INPUT_COLOR, bd=10, relief="ridge")
input_frame.place(x=10, y=100, width=300, height=250)

tk.Label(input_frame, text="Add Reminder", bg=INPUT_COLOR, fg="white",
         font=("Segoe UI", 14, "bold")).place(x=80, y=10)

hours = [str(i) for i in range(1, 13)]
minutes = [f"{i:02d}" for i in range(60)]

hour_combo = ttk.Combobox(input_frame, values=hours, width=5)
hour_combo.set("12")
hour_combo.place(x=15, y=60)

minute_combo = ttk.Combobox(input_frame, values=minutes, width=5)
minute_combo.set("00")
minute_combo.place(x=110, y=60)

period_combo = ttk.Combobox(input_frame, values=["AM", "PM"], width=5)
period_combo.set("PM")
period_combo.place(x=210, y=60)

message_entry = tk.Entry(input_frame, width=40)
message_entry.insert(0, "Kumain kana love?")
message_entry.place(x=15, y=110)


def add_reminder():
    hour = hour_combo.get()
    minute = minute_combo.get()
    period = period_combo.get()
    message = message_entry.get().strip()

    if not message:
        messagebox.showwarning("Warning", "Please enter a message")
        return

    time_string = f"{hour}:{minute} {period}"
    notifications.append({
        "time": time_string,
        "message": message,
        "notified": False
    })
    refresh_lists()


tk.Button(input_frame, text="Add Reminder", command=add_reminder, bg="#4CAF50", fg="white").place(x=15, y=160)

# ======================================
# ALL REMINDERS (TABLE)
# ======================================
reminder_frame = tk.Frame(root, bg=REMINDER_COLOR, bd=10, relief="ridge")
reminder_frame.place(x=100, y=360, width=665, height=330)

tk.Label(reminder_frame, text="All Reminders", bg=REMINDER_COLOR, fg="white",
         font=("Segoe UI", 14, "bold")).place(x=250, y=10)

# Treeview as table
reminder_tree = ttk.Treeview(reminder_frame, columns=("time", "message"), show="headings", height=12)
reminder_tree.heading("time", text="Time")
reminder_tree.heading("message", text="Message")
reminder_tree.column("time", width=100)
reminder_tree.column("message", width=500)
reminder_tree.place(x=12, y=50, width=630, height=230)


def refresh_lists():
    # Clear both trees
    for item in reminder_tree.get_children():
        reminder_tree.delete(item)
    for item in upcoming_tree.get_children():
        upcoming_tree.delete(item)

    # Sort notifications by time
    notifications.sort(key=lambda r: get_reminder_datetime(r["time"]))

    # Populate All Reminders
    for reminder in notifications:
        reminder_tree.insert("", tk.END, values=(reminder["time"], reminder["message"]))

    # Populate Upcoming
    now = datetime.now()
    upcoming = []
    for reminder in notifications:
        target = get_reminder_datetime(reminder["time"])
        diff = target - now
        if diff.total_seconds() > 0:  # Only future reminders
            hours_left = int(diff.total_seconds() // 3600)
            mins_left = int((diff.total_seconds() % 3600) // 60)
            time_left = f"{hours_left}h {mins_left}m"
            upcoming.append((diff, reminder, time_left))

    upcoming.sort(key=lambda x: x[0])
    for _, reminder, time_left in upcoming[:5]:
        upcoming_tree.insert("", tk.END, values=(
            reminder["time"],
            reminder["message"],
            time_left,
            root.after(1000, refresh_lists)
        ))


# Delete Reminder
def delete_reminder():
    selected = reminder_tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a reminder to delete")
        return
    index = reminder_tree.index(selected[0])
    notifications.pop(index)
    refresh_lists()


tk.Button(reminder_frame, text="Delete", command=delete_reminder, bg="#f44336", fg="white").place(x=550, y=10)


# Edit Reminder
def edit_reminder(event):
    selected = reminder_tree.selection()
    if not selected:
        return
    index = reminder_tree.index(selected[0])
    reminder = notifications[index]

    edit = tk.Toplevel(root)
    edit.title("Edit Reminder")
    edit.geometry("280x280")
    edit.configure(bg="#879EC6")

    h = ttk.Combobox(edit, values=hours, width=8)
    m = ttk.Combobox(edit, values=minutes, width=8)
    p = ttk.Combobox(edit, values=["AM", "PM"], width=8)
    msg = tk.Entry(edit, width=35)

    current = datetime.strptime(reminder["time"], "%I:%M %p")
    h.set(str(current.hour % 12 or 12))
    m.set(f"{current.minute:02d}")
    p.set(reminder["time"].split()[-1])
    msg.insert(0, reminder["message"])

    tk.Label(edit, text="Time:", bg="#879EC6").pack(pady=5)
    h.pack()
    m.pack(pady=5)
    p.pack()

    tk.Label(edit, text="Message:", bg="#879EC6").pack(pady=5)
    msg.pack()

    def save():
        reminder["time"] = f"{h.get()}:{m.get()} {p.get()}"
        reminder["message"] = msg.get().strip()
        refresh_lists()
        edit.destroy()

    tk.Button(edit, text="Save Changes", command=save, bg="#4CAF50", fg="white").pack(pady=10)


reminder_tree.bind("<Double-Button-1>", edit_reminder)


# ======================================
# NOTIFICATIONS
# ======================================
def check_notifications():
    current_time = datetime.now().strftime("%I:%M %p")

    for reminder in notifications:
        if reminder["time"] == current_time and not reminder["notified"]:
            reminder["notified"] = True
            messagebox.showinfo("🔔 Reminder",
                                f"Time: {reminder['time']}\n\n{reminder['message']}",
                                parent=root)

    root.after(1000, check_notifications)


# ======================================
# START
# ======================================
refresh_lists()
check_notifications()
root.mainloop()
