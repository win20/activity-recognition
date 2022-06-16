import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
import pandas as pd
import tensorflow as tf
import numpy as np    # for mathematical operations
from skimage.transform import resize   # for resizing images
from PIL import Image
from scipy.signal import find_peaks
import os
import time
import sys

def extract_frames(vid_path, target_dir):
    start = time.time()
    vidcap = cv2.VideoCapture(vid_path)
    success, image = vidcap.read()
    count = 0
    if success:
        print('Extracting frames...')
    while success:
        cv2.imwrite(target_dir + "/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        count += 1
    end = time.time()
    delta = end - start
    print('Done: extracted', count, 'frames; Took %.2f seconds\n' % delta)

    return count

# Returns a list of frames with every pixel with its BGR values
def get_frames_arr(directory, frame_count):
    frames = []
    for i in range(frame_count):
        frames.append(cv2.imread(directory + '/frame%d.jpg' % i, 1))

    return frames

def get_frames_hsv(frames):
    frames_hsv = []
    for frame in frames:
        frames_hsv.append(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
    return frames_hsv

def calculate_bpm(vid_path):
    frames_dir = 'extracted_frames'

    # Extract frames from video and store them in specified directory, return number of frames
    frame_count = extract_frames(vid_path, frames_dir)

    # Go through frames JPEGs and store pixels in variable
    print('Analysing frames to calculate BPM...')
    imgs_2 = get_frames_arr(frames_dir, frame_count)

    # Slice the array of images, convert to hsv color model
    # Create array of VALUE elements (from HSV), from each image
    sliced_imgs = imgs_2[10:]
    frames_hsv = get_frames_hsv(sliced_imgs)
    frame_values = []
    for frame in frames_hsv:
        frame_values.append(frame[240][100][2])

    # Convert to np array and plot graph
    np_frame_values = np.array(frame_values)

    # Find every trough, create a threshold to filter troughs and plot the filtered_troughs array
    # filter is created by taking the bottom third of the difference from max and min values in array
    from scipy.signal import find_peaks

    troughs, _ = find_peaks(-np_frame_values)

    high, low = max(np_frame_values), min(np_frame_values)
    diff = high - low
    threshold = low + (diff / 3)

    filtered_troughs = []

    for trough in troughs:
        if np_frame_values[trough] < threshold:
            filtered_troughs.append(trough)

    # Calculate bpm
    pulse_count = len(filtered_troughs) - 1
    bpm = pulse_count * 6

    print('Done: BPM is ', bpm, '\n')
    return bpm

def hello(test):
    print(test)


def main():
    test = sys.argv[1]
    # bpm = calculate_bpm('finger-tip-2.mp4')
    # print('BPM is: ', bpm)
    hello(test)

if __name__ == '__main__':
    main()