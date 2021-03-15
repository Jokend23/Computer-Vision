import cv2  as cv


def main():
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame_clear = frame.copy()
        if not ret:
            break

        # cv.imshow('frame', frame)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        hsv = cv.blur(hsv, (5, 5))

        mask = cv.inRange(hsv, (83, 123, 73), (255, 255, 255))
        # cv.imshow('Mask 1', mask)

        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=4)
        cv.imshow('Mask 2', mask)

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
            cv.imshow('frame 2', frame)

            roImg = frame_clear[y:y+h, x:x+w]
            cv.imshow('Detect', roImg)

        if cv.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
