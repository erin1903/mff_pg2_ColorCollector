import colorsys

import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import csv
import cv2


def int2hex(n):
    """Convert decimal to hex

    :param n: decimal number
    :type n: int

    :return: hexadecimal number
    :rtype: str
    """

    res = ""
    hex_nums = "0123456789ABCDEF"
    while n > 0:
        res = hex_nums[n % 16] + res
        n //= 16
    if len(res) == 1:
        return "0" + res
    return res


def rgb2hsv(rgb_list):
    """Convert pixels representation from RGB code to HSV

    :param rgb_list: list of pixels in RGB code (list of lists with 3 integers from 0 to 255 as red, green, blue values)
    :type rgb_list: list

    :return: list of pixels in HSV code (list of lists with 3 integers)
    :rtype: list
    """

    hsv_list = []
    for r, g, b in rgb_list:
        (r, g, b) = (round(r) / 255, round(g) / 255, round(b) / 255)
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        (h, s, v) = (int(h * 360), int(s * 255), int(v * 255))
        hsv_list.append((h, s, v))
    return hsv_list


def hsv2rgb(hsv_list):
    """Convert pixels representation from HSV to RGB

    :param hsv_list: list of pixels in HSV code (list of lists with 3 integers)
    :type hsv_list: list

    :return: list of pixels in RGB code (list of lists with 3 integers from 0 to 255 as red, green, blue values)
    :rtype: list
    """

    rgb_list = []
    for h, s, v in hsv_list:
        (h, s, v) = (h / 360, s / 255, v / 255)
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        (r, g, b) = (round(r * 255), round(g * 255), round(b * 255))
        rgb_list.append((r, g, b))
    return rgb_list


def get_category(hue):
    """Get global color category from hue value

    :param hue: hue value from 0 to 360
    :type hue: int

    :return: one of the color categories from red, orange, yellow, lime, green, green-cyan, cyan, blue-cyan,
    blue, violet, magenta and rose
    :rtype: str
    """

    hues = ['red', 'orange', 'yellow', 'lime', 'green', 'G-C',
            'cyan', 'B-C', 'blue', 'violet', 'magenta', 'rose']
    if hue > 345:
        return 'red'
    for i, cat in enumerate(range(15, 346, 30)):
        if hue <= cat:
            return hues[i]


def final_colors(hsv_list):
    """Handles 24 colors calculated by KMeans for Model 2 in Color Palette page

    :param hsv_list: list of colors in HSV (list of lists with 3 integers)
    :type hsv_list: list

    :return: list of selected colors in HSV
    :rtype: list
    """

    final = []
    hue_categories = {}

    # categorize HSV colors into global color categories by hue
    for hsv in hsv_list:
        hue_cat = get_category(hsv[0])
        if hue_cat in hue_categories:
            hue_categories[hue_cat].append(hsv)
            continue
        hue_categories[hue_cat] = [hsv]

    for category in hue_categories.values():
        l = sorted(category, key=lambda x: x[1])[-2:]  # pick 2 most saturated within same color category
        if len(l) == 1:
            final.append(l[0])
        elif l[0][2] >= l[1][2]:  # from these 2 pick the brightest (value in HSV)
            final.append(l[0])
        else:
            final.append(l[1])
    return final


@st.cache_data(show_spinner="Loading...")
def pick_colors(img_vec, clr_nums):
    """Model 1 for Color Palette page

    Creates color palette from an image with basic KMeans algorithm that clusters pixels' RGB values.

    :param img_vec: list of pixels in RGB code (list of lists with 3 integers from 0 to 255 as red, green, blue values)
    :type img_vec: list
    :param clr_nums: number of colors in palette
    :type clr_nums: int

    :return: list of RGB colors in palette
    :rtype: list
    """

    model = KMeans(n_clusters=clr_nums).fit(img_vec)
    clrs = model.cluster_centers_.tolist()
    return clrs


@st.cache_data(show_spinner="Loading...")
def pick_colors2(img_vec):
    """Model 2 for Color Palette page

    Creates color palette from an image with basic KMeans algorithm and final_colors
    function that further handles 24 cluster centers

    :param img_vec: list of pixels in RGB code (list of lists with 3 integers from 0 to 255 as red, green, blue values)
    :type img_vec: list

    :return: list of RGB colors in palette
    :rtype: list
    """

    model = KMeans(n_clusters=24).fit(img_vec)
    clrs = hsv2rgb(final_colors(rgb2hsv(model.cluster_centers_)))
    return clrs


@st.cache_resource
def load_model():
    """Model for Color Detector page

    Loads KNeighborsClassifier model and trains it with the data from training.csv file

    :return: trained model
    """

    x_train = []
    y_train = []
    with open('models/training.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            x_train.append([float(row[0]), float(row[1]), float(row[2])])
            y_train.append(row[3])

    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(x_train, y_train)
    return model


def get_rgb(img):
    """Feature extraction from an image using color histogram

    :param img: ndarray of an image

    :return: extracted feature in RGB that reflects color content of an image
    :rtype: list
    """

    rgb = [[]]
    channels = cv2.split(img)
    for chan in channels:
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        peak = np.argmax(hist)
        rgb[0].insert(0, peak)
    return rgb
