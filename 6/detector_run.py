import cv2 as cv
import dlib

model_detector = dlib.simple_object_detector('t1d.svm')

cam = cv.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    boxes = model_detector(frame)
    for box in boxes:
        print(box)
        x, y, xb, yb = box.left(), box.top(), box.right(), box.bottom()
        cv.rectangle(frame, (x, y), (xb, yb), (0, 0, 255), 2)

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
    	break

cv.destroyAllWindows()
cam.release()    