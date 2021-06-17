from PIL import Image
import os

input_path = os.getenv("HOME") + "/Downloads/batch-061121/batch-061121/"
output_path = os.getenv("HOME") + "/Documents/cards-img/batch-061121/"

img_list = os.listdir(input_path)

for i in range(len(img_list)):
	print(i, img_list[i])
	foo = Image.open(input_path + img_list[i])
	if foo.size[0] < foo.size[1]:
		foo = foo.transpose(Image.ROTATE_90)
	foo = foo.resize((1280,720), Image.ANTIALIAS)	
	foo.save(output_path + img_list[i], optimize=True, quality=70)

