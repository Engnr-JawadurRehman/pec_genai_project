# app.py
import streamlit as st
import cv2
from utils.detection import detect_objects
from utils.speech import speak
from utils.listen import listen_command
import numpy as np
import time

st.set_page_config(page_title="Object Detector for Visually Impaired", layout="centered")
st.title("🎥 Live Camera Preview + Voice Activated Detection")

FRAME_WINDOW = st.image([])

# Start camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("❌ Cannot access webcam")
    speak("Cannot access webcam")
else:
    st.success("👁️ Live preview started. Say 'capture image' anytime to take a snapshot.")
    speak("Live camera preview started. Say 'capture image' to detect objects.")

    while True:
        # Capture a frame
        ret, frame = cap.read()
        if not ret:
            st.error("⚠️ Failed to read from webcam.")
            speak("Camera error.")
            break

        # Convert BGR to RGB and display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame_rgb, channels="RGB")

        # Short delay so Streamlit UI updates
        time.sleep(1)

        # Listen for command in the background
        st.info("🎤 Listening for command...")
        command = listen_command()

        if "capture" in command or "detect" in command:
            st.info("📸 Capturing image and detecting objects...")
            image_path = "assets/captured.jpg"
            cv2.imwrite(image_path, frame)
            FRAME_WINDOW.image(frame_rgb, caption="Captured Image", use_column_width=True)

            # Object detection
            labels = detect_objects(image_path)
            if labels:
                result = f"Detected objects: {', '.join(labels)}"
                st.success(result)
                speak(result)
            else:
                st.warning("No objects detected.")
                speak("No objects detected.")

        # Optionally stop with a keyword
        if "stop" in command or "exit" in command:
            st.warning("🛑 Stopping the app.")
            speak("Stopping the app.")
            break

cap.release()
