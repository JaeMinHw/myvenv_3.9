import time
import tkinter as tk
from pylsl import StreamInlet, resolve_stream
import csv
import random
import subprocess
import playsound


# 라이브러리 import
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file

from Google import Create_Service





# API 연결 및 사전정보 입력
# store = file.Storage('dri.json') #위에서 받은 OAuth ID Json 파일
# creds = store.get()

# service = build('drive', 'v3', http=creds.authorize(Http()))

# folder_id = "12kKEvWAug2nr9bPTCM_u8XcvP16krWP0" #위에서 복사한 구글드라이브 폴더의 id


CLIENT_SECRET_FILE = 'client_secret_1038881507694-qe7l5u3h68ukd5nirniu7mqqv36goehp.apps.googleusercontent.com.json' # 초기설정 json파일 이름
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


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
    file_paths = file_name # 업로드하고자 하는 파일
    wr = csv.writer(f)
    wr.writerow(['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4','Label'])
    f.close()
    for _ in range(3):  # Repeat the process 10 times
        eeg_data_instance = eeg_data()
        selected_value = random.choice(checkbox_labels)
        print("Selected Value:", selected_value)
        
        run_audio(selected_value)
        time.sleep(2)  # Wait for 5 seconds
        run_audio("start")
        time.sleep(1)
        
        eeg_data_instance.start(selected_value,file_name)
        time.sleep(2)  # Wait for 5 seconds
        
    run_audio("end")
    
    # 파일을 구글드라이브에 업로드하기
    # 원하는 폴더에 파일 업로드
    request_body = {'name': file_paths, 'parents': [folder_id], 'uploadType': 'multipart'} # 업로드할 파일의 정보 정의
    media = MediaFileUpload(file_paths, mimetype='text/csv') # 업로드할 파일
    file_info = service.files().create(body=request_body,media_body=media, fields='id,webViewLink').execute()
    
    
        

name = input("폴더 명을 입력해주세요")
print("T",name)
if name == "" :
    name = time.strftime("%Y-%m-%d_%H-%M-%S")
    


# Create the main Tkinter window
root = tk.Tk()
root.title("EEG 데이터 수집")
root.geometry("250x300")


# Create checkbox variables and labels
checkbox_vars = [tk.IntVar() for _ in range(6)]
checkbox_labels = ["7.56", "8.5", "10", "12", "16", "14"]



    
parent_folder_id = "12kKEvWAug2nr9bPTCM_u8XcvP16krWP0"

file_metadata = {
        'name': name,
         'parents': [parent_folder_id],
        'mimeType': 'application/vnd.google-apps.folder'
    }

folder_info = service.files().create(body=file_metadata).execute()

print(folder_info.get('id'))

folder_id = folder_info.get('id')
    
    
# 구글 드라이브에 폴더 생성하기 
    
    





# Start the automation process with a button click
start_button = tk.Button(root, text="자동화 시작", command=automate_eeg_data_collection)
start_button.pack()

# Start the Tkinter main loop
root.mainloop()
