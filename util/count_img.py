import os
import xml.etree.ElementTree as ET

labels = ["one","two","three","four","five","six","seven","eight","nine","ten","j","q","k"]
usb_count = {}
iphone_count = {}

xml_path = os.getenv("HOME") + "/Documents/cards-2/Annotations/"
xml_list = os.listdir(xml_path)

for i in range(len(xml_list)):
	tree = ET.parse(xml_path + xml_list[i])
	root = tree.getroot()
	if xml_list[i][:3] == "IMG":
		for x in root.findall('./object/name'):
			if x.text not in iphone_count:
				iphone_count[x.text] = 0
			else:
				iphone_count[x.text] += 1
	else:
		for x in root.findall('./object/name'):
			if x.text not in usb_count:
				usb_count[x.text] = 0
			else:
				usb_count[x.text] += 1

print("usb / iPhone")			
for i in range(len(labels)):
	print(labels[i], usb_count[labels[i]], iphone_count[labels[i]])

