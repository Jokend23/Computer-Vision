import cv2 as cv


cap = cv.VideoCapture(0)

settings = cv.namedWindow('Settings')

cv.createTrackbar('minb', 'Settings', 0, 255, lambda x: x)
cv.createTrackbar('ming', 'Settings', 0, 255, lambda x: x)
cv.createTrackbar('minr', 'Settings', 0, 255, lambda x: x)

cv.createTrackbar('maxb', 'Settings', 255, 255, lambda x: x)
cv.createTrackbar('maxg', 'Settings', 255, 255, lambda x: x)
cv.createTrackbar('maxr', 'Settings', 255, 255, lambda x: x)

while True:
    rat, frame = cap.read()
    frame_clear = frame.copy()
    if not rat:
        break

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (5, 5))

    minb = cv.getTrackbarPos('minb', 'Settings')
    ming = cv.getTrackbarPos('ming', 'Settings')
    minr = cv.getTrackbarPos('minr', 'Settings')

    maxb = cv.getTrackbarPos('maxb', 'Settings')
    maxg = cv.getTrackbarPos('maxg', 'Settings')
    maxr = cv.getTrackbarPos('maxr', 'Settings')

    mask = cv.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=4)

    settings = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('Settings', settings)

    contours = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[0]
    if contours:
        sorted_contours = sorted(
            contours,
            key=cv.contourArea,
            reverse=True
        )
        cv.drawContours(frame, sorted_contours, 0, (255, 0, 255), 3)

        x, y, w, h = cv.boundingRect(sorted_contours[0])
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roImg = frame_clear[y:y + h, x:x + w]
        cv.imshow('Detect', roImg)

        roImg = cv.inRange(cv.resize(roImg, (64, 64)), (89, 124, 73), (255, 255, 255))
        cv.imshow('Detect mask', roImg)

    if cv.waitKey(1) == ord('q'):
        break
