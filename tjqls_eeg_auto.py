import time
import tkinter as tk
from pylsl import StreamInlet, resolve_stream
import csv
import random
import subprocess
import playsound

# Create a CSV file for storing data
# f = open('test.csv', 'a', encoding='utf-8')

class eeg_data:
    def __init__(self):
        self.inlet = None
        self.is_running = False
        self.selected_value = None  # Store the selected value

    def start(self, selected_value,file_name):
        # 현재 시간을 기반으로 파일 이름 생성
        
        f = open(file_name, 'a', encoding='utf-8')
        if self.is_running:
            return

        self.selected_value = selected_value  # Store the selected value

        print("start")
        self.is_running = True
        start_time = time.time()  # Record the start time

        print("looking for a stream...")
        streams = resolve_stream('type', 'EEG')  # You can try other stream types such as: EEG, EEG-Quality, Contact-Quality, Performance-Metrics, Band-Power
        print(selected_value)

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
                row_data = sample[3:17] + [self.selected_value]

                wr = csv.writer(f)
                
                print(i , "i value")
                wr.writerow(row_data)
                i = i + 1 
def run_audio(selected_value):
    # Replace with the command to play the audio based on the selected_value
    # For example, you can use subprocess.Popen to play an audio file
    audio_command = "./au_file/" + selected_value + ".mp3"
    # print(audio_command)
    # subprocess.Popen(audio_command, shell=True).wait()
    playsound.playsound(audio_command)

def automate_eeg_data_collection():
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output_{current_time}.csv"
    f = open(file_name, 'w', encoding='utf-8')
    wr = csv.writer(f)
    wr.writerow(['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4','Label'])
    f.close()
    for _ in range(10):  # Repeat the process 10 times
        eeg_data_instance = eeg_data()
        selected_value = random.choice(checkbox_labels)
        print("Selected Value:", selected_value)
        
        run_audio(selected_value)
        time.sleep(3)  # Wait for 5 seconds
        run_audio("start")
        time.sleep(1)
        
        eeg_data_instance.start(selected_value,file_name)
        time.sleep(3)  # Wait for 5 seconds
        


    


# Create the main Tkinter window
root = tk.Tk()
root.title("EEG 데이터 수집")
root.geometry("250x300")

# Create checkbox variables and labels
checkbox_vars = [tk.IntVar() for _ in range(7)]
checkbox_labels = ["7.56", "8.5", "10", "12", "14", "16", "20"]

# for i, checkbox_var in enumerate(checkbox_vars):
#     checkbox_var.set(0)

# # Create checkboxes and pack them
# for i, label_text in enumerate(checkbox_labels):
#     checkbox = tk.Checkbutton(root, text=label_text, variable=checkbox_vars[i])
#     checkbox.pack()

# Start the automation process with a button click
start_button = tk.Button(root, text="자동화 시작", command=automate_eeg_data_collection)
start_button.pack()

# Start the Tkinter main loop
root.mainloop()
