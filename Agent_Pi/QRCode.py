import cv2


def scan():
    cap = cv2.VideoCapture(0)

    # QR code should have engineer's id
    # id from agent pi to master pi
    # where are MAC addresses stored? new table?
    # what does identification of MAC do?
    # place on admin page to use google assistant
    # result of assistant shows one database entry

    qrDecoder = cv2.QRCodeDetector()
    font = cv2.FONT_HERSHEY_PLAIN

    while True:
        _, frame = cap.read()

        decoded, points, _ = qrDecoder.detectAndDecode(frame)

        if points is not None:
            cv2.putText(frame, decoded, (50, 50), font, 2,
                        (255, 0, 0), 3)

        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


