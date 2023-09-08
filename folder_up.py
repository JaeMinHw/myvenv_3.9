from google.oauth2 import service_account
from googleapiclient.discovery import build

# 서비스 계정 키 파일을 사용하여 인증합니다.
creds = service_account.Credentials.from_service_account_file(
    'tjqls_id.json', # 서비스 계정 키 파일 경로
    scopes=['https://www.googleapis.com/auth/drive']
)

# Google 드라이브 API 클라이언트를 생성합니다.
drive_service = build('drive', 'v3', credentials=creds)

# 부모 폴더 ID를 지정합니다. 폴더를 생성할 위치를 지정합니다.
parent_folder_id = '12kKEvWAug2nr9bPTCM_u8XcvP16krWP0'

# 생성할 폴더의 이름을 지정합니다.
folder_name = 'now'

# 폴더를 생성합니다.
folder_metadata = {
    'name': folder_name,
    'parents': [parent_folder_id],
    'mimeType': 'application/vnd.google-apps.folder'
}

created_folder = drive_service.files().create(body=folder_metadata).execute()

print(f'새로운 폴더가 생성되었습니다. ID: {created_folder["id"]}')
