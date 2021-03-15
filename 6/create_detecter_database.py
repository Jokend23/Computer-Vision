import dlib
import os
import cv2 as cv
import xml.etree.ElementTree as parser

images = []
annots = []

images_name_list = os.listdir('images')
print(images_name_list)

for file_name in images_name_list:
    image = cv.imread(f'images/{file_name}')
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    only_file_name = file_name.split('.')[0]

    tree = parser.parse(f'images_xml/{only_file_name}.xml')

    root = tree.getroot()

    for item in root.findall('object'):
        object_ = item.find('bndbox')

        x = int(object_.find('xmin').text)
        x2 = int(object_.find('xmax').text)
        y = int(object_.find('ymin').text)
        y2 = int(object_.find('ymax').text)

        images.append(image)
        annots.append([dlib.rectangle(left=x, top=y, right=x2, bottom=y2)])

options = dlib.simple_object_detector_training_options()
options.be_verbose = True

print(images)
print(annots)

detector = dlib.train_simple_object_detector(images, annots, options)
detector.save('t1d.svm')
print('Detected saved')
