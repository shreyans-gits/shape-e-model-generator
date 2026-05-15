import io
import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

PENDING_FOLDER_ID = "1ZGTtXVY-zXiDuzFV6XEJvdBLxKHmzyM0"
JOBS_FOLDER_ID    = "1aftkNW5e2DSMxHtHgGsUguMNouDZHzIf"
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service(key_path=SERVICE_ACCOUNT_FILE):
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)
    return service

def upload_job(service, job_id, prompt, format="obj"):
    payload = {
        "job_id": job_id,
        "prompt": prompt,
        "format": format
    }    
    json_data = json.dumps(payload).encode('utf-8')
    fh = io.BytesIO(json_data)
    
    file_metadata = {
        'name': f"{job_id}.json",
        'parents': [PENDING_FOLDER_ID]
    }
    media = MediaIoBaseUpload(fh, mimetype='application/json', resumable=True)
    
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()
    
    print(f"[Laptop] Uploaded job request: {uploaded_file.get('name')} (ID: {uploaded_file.get('id')})")
    return uploaded_file

def list_files(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(
        q=query,
        fields="nextPageToken, files(id, name)"
    ).execute()
    return results.get('files', [])

def poll_for_result(service, job_id, timeout=300, interval=10, format="obj"):
    target_filename = f"{job_id}.{format}"
    start_time = time.time()
    
    print(f"[Laptop] Started polling for {target_filename}...")
    
    while True:
        files = list_files(service, PENDING_FOLDER_ID)
        
        for file in files:
            if file.get('name') == target_filename:
                print(f"\n[Laptop] Success! Found output file: {target_filename}")
                return file
        
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(
                f"Polling timed out after {timeout} seconds. "
                f"Colab session may be offline or processing crashed."
            )
            
        print(f"Waiting for {target_filename}... ({int(elapsed)}s elapsed)", end='\r')
        time.sleep(interval)

def download_file(service, file_id, local_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download Progress: {int(status.progress() * 100)}%", end='\r')
            
    fh.seek(0)
    with open(local_path, 'wb') as f:
        f.write(fh.read())
    print(f"\n[Laptop] Successfully downloaded file to: {local_path}")

def delete_file(service, file_id):
    service.files().delete(fileId=file_id).execute()
    print(f"[Cleanup] Deleted remote file ID: {file_id} from Google Drive.")