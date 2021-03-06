import cv2
import os
import csv

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Loads cv2 cascade
faceCascade = cv2.CascadeClassifier(
    './data/cascades/haarcascade_frontalface_default.xml')


def loadIDs():
    """Load IDs from CSV and creates a new ID
    
    :return: ids - a list of ids
    :return: currentID: the new ID created at the end of the list
    """

    ids = []
    currentID = 1
    if os.path.exists("./data/ids.csv"):
        with open("./data/ids.csv", 'r') as f:
            csvFile = csv.reader(f, delimiter=',')
            for row in csvFile:
                for column in row:
                    currentID += 1
                    ids.append(int(column))
    ids.append(currentID)
    return ids, currentID


def saveIDs(ids):
    """Saves IDs into a CSV file
    """
    
    with open("./data/ids.csv", 'w') as f:
        csvWriter = csv.writer(f, delimiter=',')
        csvWriter.writerow(ids)


def gatherData():
    """Use the default device camera to capture images of the users face
    """
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

            count += 1

            # Writes the cropped image to file
            cv2.imwrite(user_dir + str(count) + ".jpg", roi_grey)

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
