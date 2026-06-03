import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# ======================================
# CUSTOMIZATION SECTION
# ======================================

WINDOW_WIDTH = 865
WINDOW_HEIGHT = 700

HEADER_COLOR = "#363955"
UPCOMING_COLOR = "#59598E"
INPUT_COLOR = "#54668E"
REMINDER_COLOR = "#363955"

BACKGROUND_COLOR = "#879EC6"

HEADER_X = 190
HEADER_Y = 10
HEADER_W = 485
HEADER_H = 80

UPCOMING_X = 320
UPCOMING_Y = 100
UPCOMING_W = 535
UPCOMING_H = 250

INPUT_X = 10 
INPUT_Y = 100
INPUT_W = 300 
INPUT_H = 250

REMINDER_X = 100
REMINDER_Y = 360
REMINDER_W = 665
REMINDER_H = 330

# ======================================
# MAIN WINDOW
# ======================================

root = tk.Tk()
root.title("Reminder System")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=BACKGROUND_COLOR)

notifications = []

# ======================================
# HELPER FUNCTIONS
# ======================================

def reminder_datetime(time_str):
    now = datetime.now()

    reminder_time = datetime.strptime(
        time_str,
        "%I:%M %p"
    )

    reminder = now.replace(
        hour=reminder_time.hour,
        minute=reminder_time.minute,
        second=0,
        microsecond=0
    )

    if reminder < now:
        reminder += timedelta(days=1)

    return reminder

# ======================================
# HEADER FRAME
# ======================================

header_frame = tk.Frame(
    root,
    bg=HEADER_COLOR,
    bd=15,
    relief="ridge"
)

header_frame.place(
    x=HEADER_X,
    y=HEADER_Y,
    width=HEADER_W,
    height=HEADER_H,
)

clock_label = tk.Label(
    header_frame,
    text="",
    bg=HEADER_COLOR,
    fg="white",
    font=("Segoe UI", 22, "bold")
)

clock_label.pack(expand=True)

def update_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    clock_label.config(text=f"Current Time: {now}")

    root.after(
        1000,
        update_clock
    )

update_clock()

# ======================================
# UPCOMING FRAME
# ======================================

upcoming_frame = tk.Frame(
    root,
    bg=UPCOMING_COLOR,
    bd=10,
    relief="ridge"
)

upcoming_frame.place(
    x=UPCOMING_X,
    y=UPCOMING_Y,
    width=UPCOMING_W,
    height=UPCOMING_H
)

tk.Label(
    upcoming_frame,
    text="Upcoming Reminders",
    bg=UPCOMING_COLOR,
    fg="white",
    font=("Segoe UI", 14, "bold")
).place(x=160, y=10)

upcoming_list = tk.Listbox(
    upcoming_frame,
    width=78,
    height=9,
    bd=10,
    relief="ridge"
)

upcoming_list.place(
    x=13,
    y=50
)

# ======================================
# INPUT FRAME
# ======================================

input_frame = tk.Frame(
    root,
    bg=INPUT_COLOR,
    bd=10,
    relief="ridge"
)

input_frame.place(
    x=INPUT_X,
    y=INPUT_Y,
    width=INPUT_W,
    height=INPUT_H
)

tk.Label(
    input_frame,
    text="Add Reminder",
    bg=INPUT_COLOR,
    fg="white",
    font=("Segoe UI", 14, "bold")
).place(x=80, y=10)

hours = [str(i) for i in range(1, 13)]
minutes = [f"{i:02d}" for i in range(60)]

hour_combo = ttk.Combobox(
    input_frame,
    values=hours,
    width=5
)
hour_combo.insert(0, "12")
hour_combo.place(x=15, y=60)

minute_combo = ttk.Combobox(
    input_frame,
    values=minutes,
    width=5
)
minute_combo.insert(0,"00")
minute_combo.place(x=110, y=60)

period_combo = ttk.Combobox(
    input_frame,
    values=["AM", "PM"],
    width=5
)
period_combo.insert(0,"PM")
period_combo.place(x=210, y=60)

message_entry = tk.Entry(
    input_frame,
    width=40
)
message_entry.insert(0,"Kumain kana love?")
message_entry.place(
    x=15,
    y=110
)

# ======================================
# REMINDER LIST FRAME
# ======================================

reminder_frame = tk.Frame(
    root,
    bg=REMINDER_COLOR,
    bd=10,
    relief="ridge"
)

reminder_frame.place(
    x=REMINDER_X,
    y=REMINDER_Y,
    width=REMINDER_W,
    height=REMINDER_H
)

tk.Label(
    reminder_frame,
    text="All Reminders",
    bg=REMINDER_COLOR,
    fg="white",
    font=("Segoe UI", 14, "bold"),
).place(x=250, y=10)

reminder_list = tk.Listbox(
    reminder_frame,
    width=100,
    height=14,
    bd=10,
    relief="ridge"
)

reminder_list.place(
    x=12,
    y=50
)

# ======================================
# REFRESH DISPLAY
# ======================================

def refresh_lists():

    reminder_list.delete(
        0,
        tk.END
    )

    upcoming_list.delete(
        0,
        tk.END
    )

    notifications.sort(
        key=lambda r:
        datetime.strptime(
            r["time"],
            "%I:%M %p"
        )
    )

    for reminder in notifications:

        reminder_list.insert(
            tk.END,
            f'{reminder["time"]} - {reminder["message"]}'
        )

    now = datetime.now()

    upcoming = []

    for reminder in notifications:

        target = reminder_datetime(
            reminder["time"]
        )

        diff = target - now

        upcoming.append(
            (diff, reminder)
        )

    upcoming.sort(
        key=lambda x: x[0]
    )

    for diff, reminder in upcoming[:3]:

        hours_left = int(
            diff.total_seconds() // 3600
        )

        mins_left = int(
            (diff.total_seconds() % 3600) // 60
        )

        upcoming_list.insert(
            tk.END,
            f'{reminder["time"]} | '
            f'{reminder["message"]} '
            f'({hours_left}h {mins_left}m)'
        )
        root.after(1000, refresh_lists)

# ======================================
# ADD REMINDER
# ======================================

def add_reminder():

    hour = hour_combo.get()
    minute = minute_combo.get()
    period = period_combo.get()

    message = message_entry.get()

    if not message:
        return

    time_string = (
        f"{hour}:{minute} {period}"
    )

    notifications.append({
        "time": time_string,
        "message": message,
        "notified": False
    })

    refresh_lists()

tk.Button(
    input_frame,
    text="Add Reminder",
    command=add_reminder
).place(
    x=15,
    y=160
)

# ======================================
# DELETE BUTTON
# ======================================

def delete_reminder():

    selected = reminder_list.curselection()

    if not selected:
        return

    index = selected[0]

    notifications.pop(index)

    refresh_lists()

tk.Button(
    reminder_frame,
    text="Delete",
    command=delete_reminder
).place(
    x=590,
    y=10
)

# ======================================
# EDIT WINDOW
# ======================================

def edit_reminder(event):

    selected = reminder_list.curselection()

    if not selected:
        return

    index = selected[0]

    reminder = notifications[index]

    edit = tk.Toplevel(root)

    edit.title("Edit Reminder")
    edit.geometry("240x200")
    edit.configure(bg="#879EC6")

    h = ttk.Combobox(
        edit,
        values=hours
    )

    m = ttk.Combobox(
        edit,
        values=minutes
    )

    p = ttk.Combobox(
        edit,
        values=["AM", "PM"]
    )

    msg = tk.Entry(
        edit,
        width=30
    )

    current = datetime.strptime(
        reminder["time"],
        "%I:%M %p"
    )

    h.set(str(current.hour % 12 or 12))
    m.set(f"{current.minute:02d}")
    p.set(reminder["time"].split()[-1])

    msg.insert(
        0,
        reminder["message"]
    )

    h.pack(pady=10)
    m.pack(pady=10)
    p.pack(pady=10)
    msg.pack(pady=10)

    def save():

        reminder["time"] = (
            f"{h.get()}:{m.get()} {p.get()}"
        )

        reminder["message"] = msg.get()

        refresh_lists()

        edit.destroy()

    tk.Button(
        edit,
        text="Save",
        command=save
    ).pack()

reminder_list.bind(
    "<Double-Button-1>",
    edit_reminder
)

# ======================================
# NOTIFICATIONS
# ======================================

def show_notification(reminder):

    popup = tk.Toplevel(root)

    popup.geometry(
        "240x180"
    )
    popup.configure(bg="#363955")

    popup.title("Reminder")

    tk.Label(
        popup,
        text="🔔 Reminder",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=10)

    tk.Label(
        popup,
        text=f'Time: {reminder["time"]}'
    ).pack()

    tk.Label(
        popup,
        text=reminder["message"]
    ).pack(pady=10)

    tk.Button(
        popup,
        text="Dismiss",
        command=popup.destroy
    ).pack()

def check_notifications():

    current_time = datetime.now().strftime(
        "%I:%M %p"
    )

    for reminder in notifications:

        if (
            reminder["time"] == current_time
            and not reminder["notified"]
        ):

            show_notification(
                reminder
            )

            reminder["notified"] = True

    root.after(
        1000,
        check_notifications
    )

check_notifications()

# ======================================
# START
# ======================================

refresh_lists()

root.mainloop()