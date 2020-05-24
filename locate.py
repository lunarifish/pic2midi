# locate the picture

import os

def locate():
	loc_program = os.getcwd()

	if os.path.exists("picture.jpg"):
		loc_pic_orig = loc_program + r"\picture.jpg"
		loc_pic_scaled = loc_program + r"\picture_scaled.jpg"
		return [loc_pic_orig, loc_pic_scaled]

	elif os.path.exists("picture.png"):
		loc_pic_orig = loc_program + r"\picture.png"
		loc_pic_scaled = loc_program + r"\picture_scaled.png"
		return [loc_pic_orig, loc_pic_scaled]

	elif os.path.exists("picture.jpeg"):
		loc_pic_orig = loc_program + r"\picture.jpeg"
		loc_pic_scaled = loc_program + r"\picture_scaled.jpeg"
		return [loc_pic_orig, loc_pic_scaled]

	else:
		print("picture does not exist!")
		os.system("pause >> nul")


def locate_gui(path):
	if str(path).split(".")[-1] == "jpg":
		return "_scaled.jpg"

	elif str(path).split(".")[-1] == "png":
		return "_scaled.jpg"

	elif str(path).split(".")[-1] == "jpeg":
		return "_scaled.jpeg"

	else:
		print("unsupported format/picture does not exist")
		os.system("pause >> nul")