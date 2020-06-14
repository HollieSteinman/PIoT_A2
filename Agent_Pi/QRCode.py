import cv2
import time


def scan():
    # default video capture
    cap = cv2.VideoCapture(0)

    # load QR decoder
    decoder = cv2.QRCodeDetector()

    # testing - font
    font = cv2.FONT_HERSHEY_PLAIN

    # timeout 60 seconds from now
    timeout = time.time() + 60

    while True:
        # if timed out, break
        if time.time() >= timeout:
            break

        # read the capture
        _, frame = cap.read()

        # detect QR and decode
        decoded, points, _ = decoder.detectAndDecode(frame)

        if decoded is not "":
            return decoded
            # testing - output credentials
            # cv2.putText(frame, decoded, (50, 50), font, 2,
            #           (255, 0, 0), 3)

        # testing - show capture
        cv2.imshow("Frame", frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # clean up
    cap.release()
    cv2.destroyAllWindows()

    return False

