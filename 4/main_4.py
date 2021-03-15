import cv2  as cv


def compare_detect_with_masks(detect, mask):
    count = 0
    for i in range(64):
        for j in range(64):
            if detect[i][j] == mask[i][j]:
                count += 1
    return count


def main():
    cap = cv.VideoCapture(0)
    no_drive_sign = cv.resize(cv.imread('1.png'), (64, 64))
    crosswalk_sign = cv.resize(cv.imread('2.png'), (64, 64))

    no_drive_mask = cv.inRange(no_drive_sign, (89, 91, 139), (255, 255, 255))
    crosswalk_sign_mask = cv.inRange(crosswalk_sign, (89, 91, 139), (255, 255, 255))

    cv.imshow('No drive', no_drive_mask)
    cv.imshow('Crosswalk', crosswalk_sign_mask)

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

            roImg = cv.inRange(cv.resize(roImg, (64, 64)), (89, 124, 73), (255, 255, 255))
            cv.imshow('Detect mask', roImg)

            no_drive_count = compare_detect_with_masks(detect=roImg, mask=no_drive_mask)
            crosswalk_count = compare_detect_with_masks(detect=roImg, mask=crosswalk_sign_mask)

            print('Запрещено движение:', no_drive_count, '\nПешеходный переход:', crosswalk_count)

            if no_drive_count > 3000:
                print('Это знак "Движение запрещено"')
            elif crosswalk_count > 3000:
                print('Это знак "Пешеходный переход"')
            else:
                print('=>\nЗнак не опознан')

        if cv.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
