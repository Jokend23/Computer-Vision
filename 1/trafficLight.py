import cv2
import os
import glob


PATH = '/home/jokend/PycharmProjects/trafficLightComputerVision/traffic_light_images/training'

color = ['red', 'green', 'yellow']

for clr in color:
    clr_path = os.path.join(PATH, clr)
    file_list = glob.glob(os.path.join(clr_path, '*.jpg'))

    for filename in file_list:
        print(filename)
# cv2.imread('.jpg')
