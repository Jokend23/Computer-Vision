import cv2
import numpy
import glob
import os


class MainProcess:

    def __init__(self, path, color_list):
        self.path = path
        self.color_list = color_list

    def run(self):
        for clr in self.color_list:
            clr_path = os.path.join(self.path, clr)
            files_list = glob.glob(os.path.join(clr_path, '*.jpg'))

            for filename in files_list:
                raw_frame = cv2.imread(filename)

                flag = self.find_traffic_light(raw_frame=raw_frame)

                if flag == 'continue':
                    continue
                elif flag == 'exit':
                    exit()

    def find_traffic_light(self, raw_frame):
        while True:
            frame = cv2.resize(raw_frame, (60, 120))
            cv2.imshow(str(raw_frame), frame)

            cutedFrame = frame[20:101, 8:52]

            hsv = cv2.cvtColor(cutedFrame, cv2.COLOR_BGR2HSV)
            v = hsv[:, :, 2]
            cv2.imshow('v ' + str(frame), v)

            red_sum = numpy.sum(v[0:27, 0:44])
            yellow_sum = numpy.sum(v[28:54, 0:44])
            green_sum = numpy.sum(v[55:81, 0:44])

            cv2.rectangle(cutedFrame, (0, 0), (44, 27), (0, 0, 255), 2)
            cv2.rectangle(cutedFrame, (0, 28), (44, 54), (0, 255, 255), 3)
            cv2.rectangle(cutedFrame, (0, 55), (44, 81), (0, 255, 0), 3)
            cv2.imshow('cutedFrame ' + str(frame), cutedFrame)

            print(str(red_sum) + ' : ' + str(yellow_sum) + ' : ' + str(green_sum))

            if green_sum > yellow_sum and green_sum > red_sum:
                print('green')
            elif yellow_sum > green_sum and yellow_sum > red_sum:
                print('yellow')
            elif red_sum > green_sum and red_sum > yellow_sum:
                print('red')
            else:
                print('red')

            key = cv2.waitKey(1)
            if key == ord('n'):
                cv2.destroyAllWindows()
                return 'continue'

            if key == ord('q'):
                return 'exit'

        cv2.destroyAllWindows()


def run() -> None:
    """Запуск программы"""

    path = '/home/jokend/PycharmProjects/trafficLightComputerVision/1/traffic_light_images/training'
    color_list = ['red', 'green', 'yellow']

    MainProcess(path=path, color_list=color_list).run()


if __name__ == '__main__':
    run()
