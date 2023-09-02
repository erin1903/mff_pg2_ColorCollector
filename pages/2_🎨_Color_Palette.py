import streamlit as st
from PIL import Image, ImageDraw
from utils import pick_colors, pick_colors2, int2hex


def display_palette(palette):
    size = len(palette)
    canvas = Image.new(mode='RGB', size=(100*size, 100))
    draw = ImageDraw.Draw(canvas)
    rgb_str, hex_str = "", ""
    for i, color in enumerate(palette):
        color = tuple(map(round,color))
        rgb_str += str(color) + ", "
        hex_str += "#"+int2hex(color[0])+int2hex(color[1])+int2hex(color[2]) + ", "
        draw.rectangle(xy=((100*i,0),(100*(i+1),100)), fill=color)
    st.write("RGB values:  " + rgb_str[:-2])
    st.write("HEX values:  " + hex_str[:-2])
    return canvas


def adjust_palette(palette):
    columns = st.columns(len(palette))
    for i, color in enumerate(palette):
        with columns[i]:
            hex_clr = "#" + int2hex(round(color[0])) + int2hex(round(color[1])) + int2hex(round(color[2]))
            st.color_picker(label='p', value=hex_clr, key=f"pal_clr_{i}", label_visibility='hidden')


col1, col2 = st.columns(2)
with col1:
    st.title("Color Palette")
    st.caption("Want to make a presentation inspired by the theme of a famous painting? "
               "Or just curious to see how Wes Anderson assembles beautiful colors for his immortal movies? "
               "Then this tool is just right for you! It creates color palettes from any image "
               "by using machine learning. You can choose from two models, both of which implement KMeans algorithm "
               "but create different palettes. By selecting the first model, you can/have to choose how many "
               "colors you want to see in your palette. Meanwhile, the second model does even that part for you, "
               "so you can skip choosing the number of colors and click on <Make palette> button right away!")
with col2:
    with st.form("Cookbook:"):
        file2 = st.file_uploader("Browse image", key="img_file2", type=['png', 'jpg'])
        model_option = st.selectbox("Choose model:", ("1", "2"))
        clr_nums = st.number_input("Choose number of colors in palette (only 1st model):", min_value=2, max_value=10, step=1)
        st.form_submit_button("Make palette")
if file2 is not None:
    with st.expander("Your picture", expanded=True):
        # show image
        img = Image.open(file2)
        img.thumbnail((500, 500))
        st.image(img)

    rgb_list = list(img.getdata())
    # get rid of 4th element in each pixel if present (0 or 255 indicating too much/no color in deprecated image)
    if len(rgb_list[0]) == 4:
        rgb_list = [pixel[:3] for pixel in rgb_list]

    if model_option == "1":
        palette = pick_colors(rgb_list, clr_nums)
    elif model_option == "2":
        palette = pick_colors2(rgb_list)
    st.image(display_palette(palette))

    with st.expander("Adjust my palette", expanded=False):
        st.caption("In case you want to change some of the colors a little bit, "
                   "you can experiment with the color picker widget! "
                   "Click on any of the following colors you want to adjust.")
        adjust_palette(palette)
