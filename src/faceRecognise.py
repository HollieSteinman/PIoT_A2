import cv2

# Loads cv2 cascade and trainer
faceCascade = cv2.CascadeClassifier('src/data/cascades/haarcascade_frontalface_default.xml')
recogniser = cv2.face.LBPHFaceRecognizer_create()
recogniser.read("src/data/trainer.yml")

# Uses default device camera
cap = cv2.VideoCapture(0)

# Minimum sizes for face
minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4)
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
        # DEBUGGING - Displays rectangle around face
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(
            frame,
            (x, y),
            (end_cord_x, end_cord_y),
            (0, 0, 255), 2
        )

        # Crop a rectangle of interest for a face
        roi_grey = grey[y:y + h, x:x + w]

        # Gets confidence of similarity to an id
        id, confidence = recogniser.predict(roi_grey)

        # If high enough confidence - converts confidence to confidence percentage
        if confidence < confidenceCap:
            # TODO unlock car
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            # DEBUGGING - Sets id to unknown
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        # DEBUGGING - Puts the id and confidence percentage around the square
        font = cv2.FONT_HERSHEY_SIMPLEX
        colour_text = (0, 0, 255)
        stroke_text = 1

        cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, colour_text, stroke_text)
        cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, colour_text, stroke_text)

        # DEBUGGING - Displays video frame
        cv2.imshow('frame', frame)

    # Quits if 'Q' pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Cleaning up
cap.release()
cv2.destroyAllWindows()
