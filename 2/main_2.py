import cv2 as cv


def main() -> None:
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if ret:
            cv.imshow('Frame', frame)
        else:
            break

        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
