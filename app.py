import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import random
import cv2

# Dummy emotion detection function
def detect_emotion(_image):
    return random.choice(["happy", "sad", "angry", "neutral"])

# Song recommendations
emotion_songs = {
    "happy": ["https://www.youtube.com/watch?v=ZbZSe6N_BXs"],
    "sad": ["https://www.youtube.com/watch?v=lBvbNxiVmZA"],
    "angry": ["https://www.youtube.com/watch?v=VAJK04HOLd0"],
    "neutral": ["https://www.youtube.com/watch?v=zXAjcZ-ncZg"]
}

# Set page configuration
st.set_page_config(page_title="🎥 Emotion-Based Music Recommender")
st.title("🎥 Emotion-Based Music Recommender")
st.write("Enable your webcam, and detect your emotion to get a song!")

# Create a custom video transformer
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Start the webcam stream
ctx = webrtc_streamer(
    key="emotion-detect",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True
)

# Detect emotion and recommend music
if st.button("📸 Detect Emotion"):
    if ctx.video_transformer and ctx.video_transformer.frame is not None:
        image = ctx.video_transformer.frame
        emotion = detect_emotion(image)
        song = random.choice(emotion_songs[emotion])
        st.success(f"Emotion Detected: {emotion.upper()}")
        st.video(song)
    else:
        st.warning("Please wait until the webcam loads or try again.")
