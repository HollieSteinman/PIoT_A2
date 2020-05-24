import cv2
import os


def run():
    """Attempt to recognise the face submitted by the user.
    :return: bool - True or False value for success of recognition
    """
    
    # Loads cv2 cascade and trainer
    faceCascade = cv2.CascadeClassifier(
        './data/cascades/haarcascade_frontalface_default.xml')
    recogniser = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists("./data/trainer.yml"):
        recogniser.read("./data/trainer.yml")
    else:
        return False

    # Uses default device camera
    cap = cv2.VideoCapture(0)

    # Minimum sizes for face
    minW = 0.1 * cap.get(3)
    minH = 0.1 * cap.get(4)
    # Confidence needed to be recognised
    # Roughly confidence percent = 100 - confidence
    confidenceCap = 35

    while True:
        ret, frame = cap.read()

        # Turns the camera's input to grey - easier for cv2 to analyse
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Finds faces according to the cascade
        faces = faceCascade.detectMultiScale(
            grey,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            # Crop a rectangle of interest for a face
            roi_grey = grey[y:y + h, x:x + w]

            # Gets confidence of similarity to an id
            id, confidence = recogniser.predict(roi_grey)

            # If high enough confidence - converts confidence to confidence
            # percentage
            if confidence < confidenceCap:
                return True
            else:
                return False

    cap.release()
    cv2.destroyAllWindows()
