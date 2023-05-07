# main.py
from personal_color_analysis import personal_color
import argparse
import os


def analyze_image(imgpath):
    personal_color.analysis(imgpath)


def main():
    imgpath = "1.jpg"
    analyze_image(imgpath)


if __name__ == "__main__":
    main()
