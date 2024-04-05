import threading
import time
import os
import big_chars
import extractor
from datetime import datetime

# Global variables
row = "◾◾◾◾◾◾◾◾◾◾◾◾◾◾◾◾◾◾◾"
is_running = False
elapsed_seconds = 0  # Tracks the total elapsed time in seconds
times = []
is_waiting_name = False
current_chron_name = 'default'

def print_big_number(number):
    lines = [""] * 5
    for digit in number:
        for i, line in enumerate(big_chars.big_numbers.get(digit, ['?'*5]*5)):
            lines[i] += line + "  "
    for line in lines:
        print(line)

def print_header():
    lines = [""] * 6

    for i in range(6): 
        for chara in "chrono":
            lines[i] += big_chars.big_letters.get(chara)[i] + "  "
    for line in lines:
        print(line)
    
    print('s: start counting | d: to stop counting | q: to quit | e: to extract data to csv')
    print('Press Enter to submit commands.\n')

def average_minute_second(time_list):
    total_seconds = 0
    
    # Convert each time string to total seconds and sum them up
    for item in time_list:
        hours, minutes = map(int, item['time'].split(':'))
        total_seconds += hours * 3600 + minutes * 60
    
    # Calculate the average
    average_seconds = total_seconds / len(time_list)
    
    # Convert the average back to hour:minute format
    average_hours = int(average_seconds // 3600)
    average_minutes = int((average_seconds % 3600) // 60)
    
    return f"{average_hours:02d}:{average_minutes:02d}"

def timer():
    global is_running, elapsed_seconds
    while True:
        if is_running:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for clean display
            mins, secs = divmod(elapsed_seconds, 60)
            print_big_number(f"{mins:02}:{secs:02}")
            time.sleep(1)  # Update every second
            elapsed_seconds += 1
        else:
            time.sleep(0.1)

def handle_input():
    global is_running, times, elapsed_seconds, is_waiting_name
    while True:
        inp = input().lower()
        
        if len(inp) > 0 and is_waiting_name and not is_running:
            current_chron_name = inp
            print("Starting...")

            is_waiting_name = False
            is_running = True
        elif inp == 's' and not is_running:
            print("Provide a name: ")
            is_waiting_name = True
        
        elif inp == 'c' and not is_running:
            extractor.export_to_csv(times, datetime.now().isoformat())
        elif inp == 'd' and is_running:
            print("Stopping...")
            
            is_running = False
            current_time = f"{elapsed_seconds // 60:02}:{elapsed_seconds % 60:02}"
            times.append({'name': current_chron_name, 'time': current_time})
            
            # Reset the counter
            elapsed_seconds = 0  # Reset the timer for next run
            
            # Keep only the last 35 times
            times = times[-35:]
            
            print(row)
            print("Last 35 times:")
            
            for t in times:
                print(t['name'] + ": " + t['time'])
            
            print(row)
            
            print("            Average: " + average_minute_second(times))

        elif inp == 'q':  # Adding a way to quit the program
            print("Quitting...")
            
            break

# Run the components
threading.Thread(target=timer, daemon=True).start()



print_header()
handle_input()