import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from utils import int2hex


def warn_change(hex_c):
    # show warning when the value of color picker widget was changed
    if st.session_state['picker_clr'] != hex_c:
        st.warning("WARNING: you have changed the color in your color picker widget.\n" +
                   "To show the original color selected from your image, copy the RGB/HEX code on the right "
                   "into the color picker widget.",
                   icon="🤖")


col1, col2 = st.columns(2)
with col1:
    st.title("Color Picker")
    st.caption("This tool helps you find the exact RGB and HEX code of the exact pixel! "
               "Just upload your photo and click wherever you want on the image. "
               "You can also adjust the size of the picture from 1 to 100% of the original image size. "
               "In case you want to change the chosen color a little bit, you can experiment with the color "
               "picker widget! "
               "Click on the little color box that appears on the left to the color codes and see what happens.")
with col2:
    file = st.file_uploader("Browse image", key="img_file", type=['png', 'jpg'])

col3, col4, col5 = st.columns([1, 2, 3])
with col5:
    # show image
    if file is not None:
        with st.expander("Your picture", expanded=True):
            percent = st.slider(label="Set image size to:", min_value=1, max_value=100, value=50, key="img_size") / 100
            img = Image.open(file)
            img = img.resize((round(img.width * percent), round(img.height * percent)))
            img_xy = streamlit_image_coordinates(img, key="img_xy")
if st.session_state['img_file'] is not None and 'img_xy' in st.session_state and st.session_state['img_xy'] is not None:
    try:
        rgb_clr = img.getpixel((img_xy['x'], img_xy['y']))
        with col3:
            # show selected color
            hex_clr = "#"+int2hex(rgb_clr[0])+int2hex(rgb_clr[1])+int2hex(rgb_clr[2])
            st.color_picker(label='p', value=hex_clr, key="picker_clr",
                            label_visibility='hidden', on_change=warn_change, args=(hex_clr,))
        with col4:
            # show rgb, hex of selected color
            with st.container():
                st.write("RGB:  " + ','.join(map(str, rgb_clr)))
            with st.container():
                st.write("HEX:  " + hex_clr)
    # err raises when making image size to smaller range than coordinates of previously selected color
    except IndexError:
        pass
