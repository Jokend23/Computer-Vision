import cv2 as cv
import dlib

cam = cv.VideoCapture(0)

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

while True:
    ret, frame = cam.read()
    if not ret:
        break
    frame = cv.resize(frame, (300, 225))
    rects, weights = hog.detectMultiScale(frame, winStride=(4, 4))

    for x, y, w, h in rects:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
    	break

cv.destroyAllWindows()
cam.release()    