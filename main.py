
import os
loc_program = os.getcwd()
print("程序位置:" + loc_program)
loc_pic_orig = loc_program + r"\picture.jpg"
loc_pic_scaled = loc_program + r"\picture_scaled.jpg"


# scaling picture
from PIL import Image 
infile = loc_pic_orig
outfile = loc_pic_scaled
im = Image.open(infile)
(x,y) = im.size                            # get the size of original picture
height = input("set picture height(1~127):")    # input picture height
y_scale = int(height)
x_scale = int(x * y_scale / y)             # calculate width
out = im.resize((x_scale,y_scale),Image.ANTIALIAS)
out.save(outfile)


# main

import numpy
import cv2
import mido

mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

img = cv2.imread(loc_pic_scaled)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# textsave
def text_save(content,filename,mode = 'a'):
    file = open(filename,mode)
    for i in range(len(content)):
        file.write(str(content[i])+'\n')
    file.close()
###

# textread
def text_read(filename):
    try:
        file = open(filename,'r')
    except IOError:
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]

    file.close()
    return content
###

# initialize counters
scan_x = 1                                         # colomns
scan_y = 1                                         # rows
pixel_count = 0                                    # scaned pixels
###

# find extreme values
while scan_x <= x_scale - 1:
    scan_y = 1               # reset rows

    while scan_y <= y_scale - 1:

        #counting
        pixel_count = pixel_count + 1
        print("scanning", pixel_count, "pixels")
        gray_current = gray[scan_y, scan_x]
        gray_variable = [gray_current]                     # save grayscale value of all pixels
        text_save(gray_variable,'1.txt')                   ##
        ###
        scan_y = scan_y + 1    # rows + 1
    scan_x = scan_x + 1 

gray_all_str = text_read('1.txt')
gray_all = [int(x) for x in gray_all_str]
gray_min = min(gray_all)
gray_max = max(gray_all)
print(gray_max, gray_min)


# output midi file
scan_x = 1                                         # colomns
scan_y = 1                                         # rows
pixel_count = 0                                    # scaned pixels
###

while scan_x <= x_scale - 1:
    scan_y = 1               # reset rows
    gray_current = gray[scan_y, scan_x]
    gray_calculated = (gray_current - gray_min) / (gray_max - gray_min)       # greyscale values dispersion standardization
    velocity = int(gray_calculated * 127)              # velocity
    note = int(127 - scan_y)                           # pitch
    time = 0                                           # time
    track.append(mido.Message('note_on', note=note, velocity=velocity, time=0))          # NOTE_ON

    while scan_y <= y_scale - 1:

        # counting
        pixel_count = pixel_count + 1
        print("outputing", pixel_count, "notes")
        gray_current = gray[scan_y, scan_x]
        gray_calculated = (gray_current - gray_min) / (gray_max - gray_min)       # greyscale values dispersion standardization
        velocity = int(gray_calculated * 127)              # velocity
        note = int(127 - scan_y)                           # pitch
        time = 0                                           # time
        ###

        track.append(mido.Message('note_on', note=note, velocity=velocity, time=0))        # NOTE_ON
        scan_y = scan_y + 1    # rows + 1
    scan_y = 1                 # reset rows
    gray_current = gray[scan_y, scan_x]
    gray_calculated = (gray_current - gray_min) / (gray_max - gray_min)       # greyscale values dispersion standardization
    velocity = int(gray_calculated * 127)              # velocity
    note = int(127 - scan_y)                           # pitch
    time = 0                                           # time
    track.append(mido.Message('note_off', note=note, velocity=velocity, time=480))        # NOTE_OFF

    while scan_y<= y_scale - 1:
        # counting
        pixel_count = pixel_count + 1
        gray_current = gray[scan_y, scan_x]
        gray_calculated = (gray_current - gray_min) / (gray_max - gray_min)       # greyscale values dispersion standardization
        velocity = int(gray_calculated * 127)              # velocity
        note = int(127 - scan_y)                           # pitch
        time = 0                                           # time
        ###

        track.append(mido.Message('note_off', note=note, velocity=velocity, time=0))        # NOTE_OFF
        scan_y = scan_y + 1    # rows + 1
    scan_x = scan_x + 1
mid.save('output.mid')
print("output.mid\n")
os.system("pause")
