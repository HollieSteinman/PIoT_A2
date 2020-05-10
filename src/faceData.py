import cv2
import os
import csv

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Loads cv2 cascade
faceCascade = cv2.CascadeClassifier('src/data/cascades/haarcascade_frontalface_default.xml')


# Loads IDs from csv, creates new ID
def loadIDs():
    ids = []
    currentID = 1
    if os.path.exists("src/data/ids.csv"):
        with open("src/data/ids.csv", 'r') as f:
            csvFile = csv.reader(f, delimiter=',')
            for row in csvFile:
                for column in row:
                    currentID += 1
                    ids.append(int(column))
    ids.append(currentID)
    return ids, currentID


# Saves IDs into a csv file
def saveIDs(ids):
    with open("src/data/ids.csv", 'w') as f:
        csvWriter = csv.writer(f, delimiter=',')
        csvWriter.writerow(ids)


def gatherData():
    ids, currentID = loadIDs()

    # Directory for the pictures being taken
    user_dir = os.path.join(BASE_DIR,
                            "data/faces/" + str(currentID) + "/")
    os.mkdir(user_dir)

    # Uses default device camera
    cap = cv2.VideoCapture(0)

    # Count for each image file
    count = 0
    while True:
        ret, frame = cap.read()

        # Turns the camera's input to grey - easier for cv2 to analyse
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Finds faces according to the cascade
        minW = 0.1 * cap.get(3)
        minH = 0.1 * cap.get(4)
        faces = faceCascade.detectMultiScale(
            grey,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            # Crop a rectangle of interest for a face
            roi_grey = grey[y:y + h, x:x + w]

            # DEBUGGING - Displays rectangle around face
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(
                frame,
                (x, y),
                (end_cord_x, end_cord_y),
                (0, 0, 255), 2
            )

            count += 1

            # Writes the cropped image to file
            cv2.imwrite(user_dir + str(count) + ".jpg", roi_grey)

        # DEBUGGING - Displays video frame
        cv2.imshow('frame', frame)

        # Quits if 'Q' pressed
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        # Or if 30 images have been taken
        elif count >= 30:
            break

    saveIDs(ids)

    # Cleaning up
    cap.release()
    cv2.destroyAllWindows()
