
import sys
import os
import cv2
import mido
import numpy as np


def data_standardization(data_max, data_min, current_data):
    return (current_data - data_min) / (data_max - data_min)




args = sys.argv[1:]
if len(args) != 2:
    print("Usage: main.py picture_path midi_height")
    os._exit(1)

PICTURE_PATH, MIDI_PIC_HEIGHT = args[0], int(args[1])




## Scaling picture ##
try:
    img = cv2.imread(PICTURE_PATH)
except Exception:
    os._exit(1)

x_original, y_original = img.shape[1::-1]
resize_multiplier = MIDI_PIC_HEIGHT / y_original

img_scaled = cv2.resize(img, (round(x_original * resize_multiplier), MIDI_PIC_HEIGHT))
x_scaled, y_scaled = round(x_original * resize_multiplier), MIDI_PIC_HEIGHT

img_scaled_grayscale = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2GRAY)

img_flattened = img_scaled_grayscale.flatten()
min_gray, max_gray = min(img_flattened), max(img_flattened)

img_scaled_grayscale_rotated = np.array(list(reversed(np.rot90(img_scaled_grayscale))))

######################



mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)


for line in img_scaled_grayscale_rotated:
    for index, pixel in enumerate(line):
        velocity = int(data_standardization(max_gray, min_gray, pixel) * 127)
        track.append(mido.Message("note_on", note=MIDI_PIC_HEIGHT - index, velocity=velocity, time=0))
    for index, pixel in enumerate(line):
        velocity = int(data_standardization(max_gray, min_gray, pixel) * 127)
        if index == 0:
            track.append(mido.Message("note_off", note=MIDI_PIC_HEIGHT - index, velocity=velocity, time=200))
        else:
            track.append(mido.Message("note_off", note=MIDI_PIC_HEIGHT - index, velocity=velocity, time=0))


output_filename = "".join(PICTURE_PATH.split(".")[:-1]) + ".mid"
mid.save(output_filename)
