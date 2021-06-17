import os
import xml.etree.ElementTree as ET
from PIL import Image

xml_path = os.getenv("HOME") + "/Documents/cards-2/Annotations/"
xml_list = os.listdir(xml_path)
xml_output_path = os.getenv("HOME") + "/Documents/sub-img-annotation/"

img_input_path = os.getenv("HOME") + "/Documents/cards-2/JPEGImages/"
img_output_path = os.getenv("HOME") + "/Documents/sub-img/"

for i in range(len(xml_list)):
	# print(i, xml_list[i])
	tree = ET.parse(xml_path + xml_list[i])
	root = tree.getroot()
	
	names = [x.text for x in root.findall('./object/name')]
	
	if "four" in names:
		if xml_list[i][:3] == "IMG":
			foo = Image.open(img_input_path + xml_list[i][:-4] + ".JPG")
		else:
			foo = Image.open(img_input_path + xml_list[i][:-4] + ".jpg")
		foo.save(img_output_path + xml_list[i][:-4] + ".jpg")
	
