import mediapipe as mp
import cv2
import time
import math
import random
import os
import json
import shutil
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDS_FILE = 'google_drive_credentials.json'

def get_credentials():
    if os.path.exists(CREDS_FILE):
        creds = Credentials.from_authorized_user_file(CREDS_FILE, SCOPES)
        return creds
    else:
        return None

def save_credentials(creds):
    with open(CREDS_FILE, 'w') as f:
        f.write(creds.to_json())

def authenticate_google_drive():
    existing_creds = get_credentials()
    if existing_creds and existing_creds.valid:
        return existing_creds
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        save_credentials(creds)
        return creds

def upload_to_google_drive(file_path):
    credentials = authenticate_google_drive()
    drive_service = build('drive', 'v3', credentials=credentials)

    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': ['1_AcXHJjg91IFDb8mABQNKbic-Jq672Fp']  # ID of the folder in your Google Drive
    }

    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

# Initialize variables
start_time = 0
end_time = 0
prev_state = "Only one person is detected"
flag = False

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)

cap = cv2.VideoCapture(0)
video = str(random.randint(1, 50000)) + "MTOPViolation.avi"
writer = cv2.VideoWriter(video, cv2.VideoWriter_fourcc(*"XVID"), 20, (640, 480))

def MTOP_record_duration(text, img):
    global start_time, end_time, prev_state, flag, writer, video
    if text != 'Only one person is detected' and prev_state == 'Only one person is detected':
        start_time = time.time()
        writer.write(img)
    elif text != 'Only one person is detected' and str(text) == prev_state and (time.time() - start_time) > 3:
        flag = True
        writer.write(img)
    elif text != 'Only one person is detected' and str(text) == prev_state and (time.time() - start_time) <= 3:
        flag = False
        writer.write(img)
    else:
        if prev_state != "Only one person is detected":
            writer.release()
            end_time = time.time()
            duration = math.ceil(end_time - start_time)
            HeadViolation = {
                "Name": prev_state,
                "Time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
                "Duration": str(duration) + " seconds",
                "Mark": (2 * (duration - 3)),
                "Link": video
            }
            if flag:
                write_json(HeadViolation)
                upload_to_google_drive(video)  # Upload the video to Google Drive
            else:
                os.remove(video)
            video = str(random.randint(1, 50000)) + "MTOPViolation.avi"
            writer = cv2.VideoWriter(video, cv2.VideoWriter_fourcc(*"XVID"), 20, (640, 480))
            flag = False
    prev_state = text

def write_json(new_data, filename='violation.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                int(bboxC.width * iw), int(bboxC.height * ih)

            cv2.rectangle(img, bbox, (255, 0, 255), 2)

        if id > 0:
            text = "More than one person is detected."
        else:
            text = "Only one person is detected"

    MTOP_record_duration(text, img)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) == ord("q") or cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()
