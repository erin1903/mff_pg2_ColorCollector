import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import av
from utils import load_model, get_rgb


st.title("Color Detector")
st.caption("This is a real-time color detection tool. Similarly to the color palette tool, "
           "this is also implemented by a machine learning technique called KNN algorithm. Show any object you "
           "have at hand and the program will try to classify the object's color into one of these: black, "
           "blue, green, yellow, orange, red, violet and white. To start the video stream, click on START button "
           "and allow camera usage. Bring any object close to the camera and you will see the program's guess "
           "on the object's color!")


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    rgb = get_rgb(img)

    model = load_model()
    prediction = model.predict(rgb)

    img = cv2.putText(img=img, text='prediction: '+prediction[0], org=(15,35), color=(255, 31, 154),
                      fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, thickness=2)
    return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(key='video_stream', video_frame_callback=video_frame_callback,
                media_stream_constraints={"video": True, "audio": False},
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
