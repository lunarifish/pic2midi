from textsaveload import *
from pic_scale import picscale
from locate import locate_gui
import os
import cv2
import mido


def main(infile, height):
    # scaling picture

    outfile = infile + locate_gui(infile)
    stat_pic = picscale(infile, outfile, height)


    # main

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    img = cv2.imread(outfile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)




    # initialize counters
    scan_x = 1                                         # colomns
    scan_y = 1                                         # rows
    pixel_count = 0                                    # scaned pixels
    x = stat_pic[0]                                    # original picture width
    y = stat_pic[1]                                    # original picture height
    x_scale = stat_pic[2]                              # scaled picture width
    y_scale = stat_pic[3]                              # scaled picture height
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
            text_save(gray_variable,"grayscale_value.txt")     ##
            ###
            scan_y = scan_y + 1    # rows + 1
        scan_x = scan_x + 1 

    gray_all_str = text_read("grayscale_value.txt")
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
        track.append(mido.Message("note_on", note=note, velocity=velocity, time=0))          # NOTE_ON

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

            track.append(mido.Message("note_on", note=note, velocity=velocity, time=0))        # NOTE_ON
            scan_y = scan_y + 1    # rows + 1
        scan_y = 1                 # reset rows
        gray_current = gray[scan_y, scan_x]
        gray_calculated = (gray_current - gray_min) / (gray_max - gray_min)       # greyscale values dispersion standardization
        velocity = int(gray_calculated * 127)              # velocity
        note = int(127 - scan_y)                           # pitch
        time = 0                                           # time
        track.append(mido.Message("note_off", note=note, velocity=velocity, time=480))        # NOTE_OFF

        while scan_y<= y_scale - 1:
            # counting
            pixel_count = pixel_count + 1
            gray_current = gray[scan_y, scan_x]
            gray_calculated = (gray_current - gray_min) / (gray_max - gray_min)       # greyscale values dispersion standardization
            velocity = int(gray_calculated * 127)              # velocity
            note = int(127 - scan_y)                           # pitch
            time = 0                                           # time
            ###

            track.append(mido.Message("note_off", note=note, velocity=velocity, time=0))        # NOTE_OFF
            scan_y = scan_y + 1    # rows + 1
        scan_x = scan_x + 1

    mid.save("output.mid")
    print("completed")