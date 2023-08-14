
import sys
import os
import cv2
import mido
import numpy as np


def data_standardization(data_max, data_min, current_data):
    return (current_data - data_min) / (data_max - data_min)


# Process user input
args = sys.argv[1:]
try:
    if len(args) != 2:
        print("Usage: main.py picture_path midi_height")
        os._exit(1)
    if int(args[1]) not in range(1, 128):
        print("MIDI pic height too big/small(range 1~127)")

    PICTURE_PATH, MIDI_PIC_HEIGHT = args[0], int(args[1])
except Exception:
    os._exit(1)

######################


# Scaling picture
try:
    img = cv2.imread(PICTURE_PATH)
except Exception:
    os._exit(1)

x_original, y_original = img.shape[1::-1]
resize_multiplier = MIDI_PIC_HEIGHT / y_original

img_scaled = cv2.resize(
    img, (round(x_original * resize_multiplier), MIDI_PIC_HEIGHT))
x_scaled, y_scaled = round(x_original * resize_multiplier), MIDI_PIC_HEIGHT

img_scaled_grayscale = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2GRAY)

img_flattened = img_scaled_grayscale.flatten()
min_gray, max_gray = min(img_flattened), max(img_flattened)

img_scaled_grayscale_rotated = np.rot90(img_scaled_grayscale)

######################


# Pre-compute grey value to velocity table
velocity_gray_table = [None] * min_gray
for i in range(min_gray, max_gray + 1):
    velocity_gray_table.append(
        int(data_standardization(max_gray, min_gray, i) * 127))

######################


# Generate .mid file
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)


for line in img_scaled_grayscale_rotated:
    for index, pixel in enumerate(line):
        track.append(mido.Message("note_on", note=index,
                     velocity=velocity_gray_table[pixel], time=0))
    for index, pixel in enumerate(line):
        if index == 0:
            track.append(mido.Message("note_off", note=index,
                         velocity=velocity_gray_table[pixel], time=200))
        else:
            track.append(mido.Message("note_off", note=index,
                         velocity=velocity_gray_table[pixel], time=0))


output_filename = "".join(PICTURE_PATH.split(".")[:-1]) + ".mid"
mid.save(output_filename)
