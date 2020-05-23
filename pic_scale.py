# scaling picture

from PIL import Image

def picscale(pic_in, pic_out, height):

	im = Image.open(pic_in)
	(x,y) = im.size                                 # get the size of original picture
	y_scale = int(height)
	x_scale = int(x * y_scale / y)                  # calculate width
	out = im.resize((x_scale,y_scale),Image.ANTIALIAS)
	out.save(pic_out)

	return [x, y, x_scale, y_scale]