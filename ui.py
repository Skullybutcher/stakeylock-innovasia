import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

# Function to load Lottie animations from a URL
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an error for bad responses
        return r.json()
    except Exception:
        return None

# Load animations (ensure these URLs are valid)
lottie_signal = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_7j2gk0gq.json")
lottie_license_plate = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_u0j5qj7j.json")
lottie_speeding = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_2g8l4b3m.json")
lottie_traffic = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_1o3j0v4h.json")

# Title of the app
st.set_page_config(page_title="Traffic Management System", layout="wide")
st.markdown(
    """
    <style>
    .title {
        color: #ff6347;
        font-size: 40px;
        text-align: center;
        margin-bottom: 20px;
    }
    .header {
        color: #4CAF50;
        font-size: 30px;
        text-align: center;
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #888;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Background image
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0") no-repeat center center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="title">Traffic Management System</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose an option:", 
                                ("Signal Changing System", 
                                 "License Plate Detection System", 
                                 "Speeding Detection", 
                                 "Traffic Detection"))  # Added YouTube Live Feed option

# Main content based on the selected option

if option == "Signal Changing System":
    st.markdown('<h2 class="header">Signal Changing System</h2>', unsafe_allow_html=True)
    if lottie_signal:
        st_lottie(lottie_signal, height=300, key="signal")
    else:
        st.warning("Lottie animation could not be loaded. Please check the URL or try again later.")
    
    st.subheader("Upload a Video")
    video_file = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])
    if video_file:
        st.video(video_file)
        st.button("Process Video")

elif option == "License Plate Detection System":
    st.markdown('<h2 class="header">License Plate Detection System</h2>', unsafe_allow_html=True)
    if lottie_license_plate:
        st_lottie(lottie_license_plate, height=300, key="license_plate")
    else:
        st.warning("Lottie animation could not be loaded. Please check the URL or try again later.")
    
    st.subheader("Upload an Image")
    image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if image_file:
        st.image(image_file, caption='Uploaded Image', use_column_width=True)
        st.button("Detect License Plate")

elif option == "Speeding Detection":
    st.markdown('<h2 class="header">Speeding Detection</h2>', unsafe_allow_html=True)
    if lottie_speeding:
        st_lottie(lottie_speeding, height=300, key="speeding")
    else:
        st.warning("Lottie animation could not be loaded. Please check the URL or try again later.")
    
    st.subheader("Upload a Video")
    speeding_video_file = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])
    if speeding_video_file:
        st.video(speeding_video_file)
        st.button("Process Speeding Video")

elif option == "Traffic Detection":
    st.markdown('<h2 class="header">Traffic Detection</h2>', unsafe_allow_html=True)
    if lottie_traffic:
        st_lottie(lottie_traffic, height=300, key="traffic")
    else:
        st.warning("Lottie animation could not be loaded. Please check the URL or try again later.")
    
    st.subheader("Traffic Analytics")
    st.write("Provide analytics of a traffic detection algorithm here.")
    st.button("Generate Traffic Report")