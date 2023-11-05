import tkinter as tk
from tkinter import messagebox
import time
import pygame
from pygame import mixer

pygame.mixer.init()
mixer.music.load('./beep.wav')  # Replace with the actual path to your sound file


def digital_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, digital_clock)

def start_stopwatch():
    global start_time, stopwatch_running, elapsed_time, pause_time
    if not stopwatch_running:
        if pause_time is not None:
            elapsed_time += time.time() - pause_time
            pause_time = None
        else:
            start_time = time.time() - elapsed_time
        stopwatch_running = True
        update_stopwatch()

def stop_stopwatch():
    global stopwatch_running, pause_time
    if stopwatch_running:
        pause_time = time.time()
        stopwatch_running = False
        update_stopwatch()

def reset_stopwatch():
    global elapsed_time, pause_time
    elapsed_time = 0
    pause_time = None
    stopwatch_running = False
    stopwatch_label.config(text=format_time(elapsed_time))

def update_stopwatch():
    global elapsed_time
    if stopwatch_running:
        elapsed_time = time.time() - start_time
    stopwatch_label.config(text=format_time(elapsed_time))
    stopwatch_label.after(10, update_stopwatch)

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    milliseconds = int((seconds - int(seconds)) * 100)
    return f"{minutes:02d}:{int(seconds):02d}.{milliseconds:02d}"

def set_timer():
    try:
        timer_duration = int(timer_entry.get())
        timer_label.config(text=format_time(timer_duration))
        update_timer(timer_duration)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid time in seconds")

def update_timer(seconds):
    if seconds >= 0:
        timer_label.config(text=format_time(seconds))
        timer_label.after(10, update_timer, seconds - 0.01)

def show_clock():
    clock_frame.pack()
    stopwatch_frame.pack_forget()
    timer_frame.pack_forget()
    alarm_frame.pack_forget()
    animate_button(clock_button)

def show_stopwatch():
    clock_frame.pack_forget()
    stopwatch_frame.pack()
    timer_frame.pack_forget()
    alarm_frame.pack_forget()
    animate_button(stopwatch_button)

def show_timer():
    clock_frame.pack_forget()
    stopwatch_frame.pack_forget()
    timer_frame.pack()
    alarm_frame.pack_forget()
    animate_button(timer_button)

def show_alarm():
    clock_frame.pack_forget()
    stopwatch_frame.pack_forget()
    timer_frame.pack_forget()
    alarm_frame.pack()
    animate_button(alarm_button)

def animate_button(button):
    button.config(bg="lightblue")
    button.after(100, lambda: button.config(bg="white"))

def add_alarm():
    hour = alarm_hour_entry.get()
    minute = alarm_minute_entry.get()
    try:
        hours = int(hour)
        minutes = int(minute)
        total_minutes = hours * 60 + minutes
        alarms.append(total_minutes)
        alarm_listbox.insert(tk.END, f"{hours:02d}:{minutes:02d}")
        alarm_hour_entry.delete(0, tk.END)
        alarm_minute_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid hours and minutes")

def check_alarms():
    current_time = time.strftime("%H:%M")
    for alarm_minutes in list(alarms):  # Convert alarms to a list to avoid modifying it while iterating
        alarm_time = time.gmtime(alarm_minutes * 60)
        if time.strftime("%H:%M", alarm_time) == current_time:
            ring_alarm()
            alarms.remove(alarm_minutes)  # Remove the alarm from the list

    root.after(1000, check_alarms)  # Check alarms every second (1000 milliseconds)



def ring_alarm():
    mixer.music.play(-1)  # Play the sound continuously
    alarm_popup = tk.Toplevel(root)
    alarm_popup.title("Alarm")
    alarm_popup.geometry("300x100")
    alarm_label = tk.Label(alarm_popup, text="Your alarm is ringing!", font=("Helvetica", 16))
    alarm_label.pack(pady=20)
    close_button = tk.Button(alarm_popup, text="Close", command=stop_alarm)
    close_button.pack()

def stop_alarm():
    mixer.music.stop()
    root.after(0, check_alarms)  # Restart the alarm checking


# Later in the code:
alarms = set()  # Use a set to store alarm times
alarms_rung = set()  # Keep track of alarms that have rung

root = tk.Tk()
root.title("Clock App")
root.geometry("400x400")

stopwatch_running = False
elapsed_time = 0
pause_time = None
alarms = []

# Footer with buttons to switch between sections
footer = tk.Frame(root)
footer.pack(side=tk.BOTTOM, fill=tk.X)
alarm_button = tk.Button(footer, text="Alarm", command=show_alarm)
clock_button = tk.Button(footer, text="Clock", command=show_clock)
stopwatch_button = tk.Button(footer, text="Stopwatch", command=show_stopwatch)
timer_button = tk.Button(footer, text="Timer", command=show_timer)
alarm_button.pack(side=tk.LEFT, padx=10)  # Add padding (e.g., 10 pixels) between buttons
clock_button.pack(side=tk.LEFT, padx=10)  # Add padding (e.g., 10 pixels) between buttons
stopwatch_button.pack(side=tk.LEFT, padx=10)  # Add padding (e.g., 10 pixels) between buttons
timer_button.pack(side=tk.LEFT, padx=10)  # Add padding (e.g., 10 pixels) between buttons


# Styling
for button in (alarm_button, clock_button, stopwatch_button, timer_button):
    button.config(relief=tk.FLAT, bg="white", activebackground="lightblue")

# Clock frame
clock_frame = tk.Frame(root)
clock_label = tk.Label(clock_frame, text="", font=("Helvetica", 36))
clock_label.pack(pady=20)

# Stopwatch frame
stopwatch_frame = tk.Frame(root)
stopwatch_label = tk.Label(stopwatch_frame, text="", font=("Helvetica", 24))
start_button = tk.Button(stopwatch_frame, text="Start", command=start_stopwatch)
pause_button = tk.Button(stopwatch_frame, text="Pause", command=stop_stopwatch)
reset_button = tk.Button(stopwatch_frame, text="Reset", command=reset_stopwatch)
stopwatch_label.pack(pady=20)
start_button.pack(side=tk.LEFT, padx=5)
pause_button.pack(side=tk.LEFT, padx=5)
reset_button.pack(side=tk.LEFT, padx=5)



# Timer frame
timer_frame = tk.Frame(root)
timer_label = tk.Label(timer_frame, text="", font=("Helvetica", 24))
timer_minutes_label = tk.Label(timer_frame, text="Timer (seconds):")  # Add this label
timer_entry = tk.Entry(timer_frame)
set_timer_button = tk.Button(timer_frame, text="Set Timer", command=set_timer)
timer_label.pack(pady=20)
timer_minutes_label.pack()  # Add the label to display "Timer (minutes):"
timer_entry.pack()
set_timer_button.pack()




# Alarm frame
alarm_frame = tk.Frame(root)
alarm_label = tk.Label(alarm_frame, text="Alarms", font=("Helvetica", 24))
alarm_hour_label = tk.Label(alarm_frame, text="Hours:")
alarm_minute_label = tk.Label(alarm_frame, text="Minutes:")
alarm_hour_entry = tk.Entry(alarm_frame)
alarm_minute_entry = tk.Entry(alarm_frame)
add_alarm_button = tk.Button(alarm_frame, text="Add Alarm", command=add_alarm)
alarm_listbox = tk.Listbox(alarm_frame, height=5)
check_alarm_button = tk.Button(alarm_frame, text="Check Alarms", command=check_alarms)
alarm_label.pack(pady=20)
alarm_hour_label.pack()
alarm_hour_entry.pack()
alarm_minute_label.pack()
alarm_minute_entry.pack()
add_alarm_button.pack()
alarm_listbox.pack()
check_alarm_button.pack()

# Styling for buttons in stopwatch and timer frames
for button in (start_button, pause_button, reset_button, set_timer_button, add_alarm_button, check_alarm_button):
    button.config(bg="lightblue", activebackground="blue")

# Initialize the clock section as the default
show_clock()
digital_clock()  # Start the digital clock

root.after(0, check_alarms)  # Start checking alarms immediately
root.mainloop()
