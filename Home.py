import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="Color Collector",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",)
st.title("Welcome to Color Collector!")
col1, col2 = st.columns(2)
with col1:
    st.write("You've reached the streamlit web application, "
             "where you can extract colors from your favourite photos with the help of machine learning! "
             "There are three different tools available for you. ")
with col2:
    color_picker = st.button("Color Picker ➡️")
    color_palette = st.button("Color Palette ➡️")
    color_detector = st.button("Color Detector ➡️")
    if color_picker:
        switch_page("Color Picker")
    if color_palette:
        switch_page("Color Palette")
    if color_detector:
        switch_page("\u200d color detector")

st.write("dflkjndlfkndlkndlkbdb")
