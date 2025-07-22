# ProctorVisionAI
# 🎯 ProctorVisionAI

**ProctorVisionAI** is an advanced AI-powered video surveillance system developed for **online exam proctoring** and **face violation detection**. It monitors real-time webcam input to identify scenarios where **more than one person appears** in the frame, marking such events with timestamps, video evidence, and violation scores. All flagged clips are automatically **uploaded to Google Drive** for secure storage.

---

## 🚀 Features

- 🎥 Real-time webcam surveillance using OpenCV
- 🧠 Face detection using MediaPipe
- 🛑 Detects **multiple person presence** violations
- ⏱️ **Records violation video only if more than one person is detected for more than 3 seconds**, reducing false positives from accidental appearances  
- 📁 Saves violation clips locally  
- 📁 Records violation clips locally
- ☁️ Auto-uploads violation videos to **Cloud**(Here I used Google drive for storage)
- 📊 Logs violation metadata in JSON format (name, duration, score, video link)
- 🔐 Google OAuth integration for secure Drive uploads

---

## 🛠️ Tech Stack

| Category       | Tools/Tech Used |
|----------------|-----------------|
| Programming    | `Python 3.x`    |
| Computer Vision| `OpenCV`, `MediaPipe` |
| Cloud Storage  | `Google Drive API` |
| Auth & Config  | `OAuth2`, `.env`, `JSON` |
| Others         | `PyAutoGUI`, `Math`, `Shutil`, `Random`, `Datetime` |

---

## 🧪 Use Cases

- 🧑‍💻 Online exam monitoring with violation detection  
- 🏫 School/college exam security  
- 🧠 Training dataset collection for surveillance ML models  
- 🎥 Real-time detection and logging for crowd analysis

---

## 📦 Folder Structure

```bash
ProctorVisionAI/
├── main.py                         # Main app logic
├── credentials.json               # Google Drive API client credentials
├── google_drive_credentials.json  # Saved OAuth token
├── violation.json                 # Violation metadata logs
├── *.avi                          # Recorded video files
└── README.md                      # Project documentation
```
### ⚙️ Setup & Installation
✅ 1. Clone the Repository
```bash
git clone https://github.com/Rakesh-honawad/ProctorVisionAI.git
cd ProctorVisionAI
```
### 🔐 2. Setup Google Drive API
Go to Google Developer Console
Create a new project → Enable Google Drive API
Download credentials.json and place it in the root folder
The first time you run the project, an OAuth browser prompt will appear
### 🧪 3. Install Required Libraries
```bash
pip install opencv-python mediapipe google-api-python-client google-auth google-auth-oauthlib
```
### ▶️ Running the Application
```bash
python main.py
```
Press q or Esc to stop the video stream.
🔎 Sample Output in violation.json
```json
{
  "Name": "More than one person detected",
  "Time": "2025-07-21 14:32:10",
  "Duration": "7 seconds",
  "Mark": 8,
  "Link": "12345MTOPViolation.avi"
}
```
### 📃 License
This project is for educational and personal use only. Not licensed for commercial proctoring services.


