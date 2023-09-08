import time
import tkinter as tk
from pylsl import StreamInlet, resolve_stream
import csv

# Create a CSV file for storing data
f = open('output.csv', 'a', encoding='utf-8')

class eeg_data:
    def __init__(self):
        self.inlet = None
        self.is_running = False
        self.selected_value = None  # Store the selected value

    def start(self, selected_value):
        if self.is_running:
            return

        self.selected_value = selected_value  # Store the selected value

        print("start")
        self.is_running = True
        start_time = time.time()  # Record the start time

        print("looking for a stream...")
        streams = resolve_stream('type', 'EEG')  # You can try other stream types such as: EEG, EEG-Quality, Contact-Quality, Performance-Metrics, Band-Power
        print(streams)

        self.inlet = StreamInlet(streams[0])  # Create a new inlet to read from the stream
        i = 0
        while self.is_running:
            
            sample, timestamp = self.inlet.pull_sample()
            
            if i == 640 : 
                

                
                self.is_running = False
                break
            if timestamp is not None:
                print(timestamp)
                

                # Include the selected value in the CSV row
                row_data = sample[2:] + self.selected_value

                wr = csv.writer(f)
                
                print(i , "i value")
                wr.writerow(row_data)
                i = i + 1 

            # Check if 5 seconds have passed, and if so, stop recording
            # if time.time() - start_time >= 5 :
            #     self.end()
            
            


def get_checkbox_values(eeg_data_instance):
    selected_values = []
    for i, checkbox_var in enumerate(checkbox_vars):
        if checkbox_var.get() == 1:
            selected_values.append(checkbox_labels[i])

    if selected_values:
        eeg_data_instance.start(selected_values)

# Create the main Tkinter window
root = tk.Tk()
root.title("EEG 데이터 수집")
root.geometry("250x600")

# Create checkbox variables and labels
checkbox_vars = [tk.IntVar() for _ in range(7)]
checkbox_labels = ["7.56", "8.5", "10", "12", "14", "16"]

for i, checkbox_var in enumerate(checkbox_vars):
    checkbox_var.set(0)

# Create checkboxes and pack them
for i, label_text in enumerate(checkbox_labels):
    
    checkbox = tk.Checkbutton(root, text=label_text, variable=checkbox_vars[i])
    checkbox.pack()

# Create an instance of the eeg_data class
eeg_data_instance = eeg_data()

# Create a Start button
start_button = tk.Button(root, text="시작", command=lambda: get_checkbox_values(eeg_data_instance))
start_button.pack()

# Start the Tkinter main loop
root.mainloop()
