import os
import time
import datetime
import sounddevice as sd
import soundfile as sf
import numpy as np
from pynput import keyboard
from pynput.keyboard import Key, Listener
import threading
import queue
import speech_recognition as sr
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

class LectureRecorder:
    def __init__(self, output_dir="lecture_recordings"):
        self.output_dir = output_dir
        self.recording = False
        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
        self.audio_frames = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Google Classroom setup (you'll need to set up credentials)
        self.setup_google_classroom()
    
    def setup_google_classroom(self):
        # This is a placeholder - you'll need to set up Google Cloud credentials
        self.SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
                      'https://www.googleapis.com/auth/classroom.coursework.students']
        self.creds = None
        
    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_frames = []
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            print("Recording started...")
    
    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.recording_thread.join()
            self.save_recording()
            print("Recording stopped and saved.")
    
    def _record_audio(self):
        sample_rate = 44100  # Sample rate in Hz
        channels = 2  # Stereo
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_frames.append(indata.copy())
        
        with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
            while self.recording:
                sd.sleep(1000)  # Check every second if we should stop
    
    def save_recording(self):
        if not self.audio_frames:
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"lecture_{timestamp}.wav")
        
        # Combine all audio frames
        audio_data = np.concatenate(self.audio_frames, axis=0)
        
        # Save as WAV file
        sf.write(filename, audio_data, 44100)
        print(f"Audio saved as {filename}")
        
        # Process the recording (transcribe, etc.)
        self.process_recording(filename)
    
    def process_recording(self, audio_file):
        # This is where you would add speech-to-text processing
        # and other post-processing of the recording
        print(f"Processing recording: {audio_file}")
        # TODO: Add speech recognition and note generation
    
    def upload_to_classroom(self, file_path, course_id):
        # This is a placeholder - you'll need to implement Google Classroom API integration
        print(f"Would upload {file_path} to Google Classroom course {course_id}")

def on_press(key):
    # Start/stop recording with F9 key
    if key == keyboard.Key.f9:
        if not recorder.recording:
            recorder.start_recording()
        else:
            recorder.stop_recording()
    # Exit with ESC key
    elif key == keyboard.Key.esc:
        if recorder.recording:
            recorder.stop_recording()
        return False  # Stop listener

if __name__ == "__main__":
    print("Starting Lecture Recorder Agent")
    print("Press F9 to start/stop recording")
    print("Press ESC to exit")
    
    recorder = LectureRecorder()
    
    # Start keyboard listener in a separate thread
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
