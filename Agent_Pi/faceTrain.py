import os
import numpy as np
import cv2
from PIL import Image
import csv

# Directory for face images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_dir = os.path.join(BASE_DIR, "data/faces/")


def loadIDs():
    """Load IDs from CSV file
    :return: ids(list) - a list of ids taken from the csv file
    """

    ids = []
    with open("src/data/ids.csv", 'r') as f:
        csvFile = csv.reader(f, delimiter=',')
        for row in csvFile:
            for column in row:
                ids.append(int(column))
    return ids


def train():
    """Train the recogniser using the samples
    """
    # Loads cv2 cascade
    faceCascade = cv2.CascadeClassifier(
        './data/cascades/haarcascade_frontalface_default.xml')
    # Creates new LBPH recogniser
    recogniser = cv2.face.LBPHFaceRecognizer_create()

    ids = loadIDs()
    faceSamples = []
    labels = []

    # For each ID
    for id in ids:
        # Walk through the directory
        for root, dirs, files in os.walk(user_dir + str(id) + "/"):
            # For each file
            for file in files:
                # If the file is a JPG
                if file.endswith(".jpg"):
                    # Directory of image
                    path = os.path.join(root, file)
                    # Converts image to greyscale
                    pilImage = Image.open(path).convert("L")
                    # Converts image to numpy array
                    imageNumpy = np.array(pilImage, "uint8")
                    # Searches for faces in array
                    faces = faceCascade.detectMultiScale(imageNumpy)

                    for (x, y, w, h) in faces:
                        # Crop a rectangle of interest for a face
                        roi = imageNumpy[y:y + h, x:x + w]
                        # Add rectangle of interest and label to relevant lists
                        faceSamples.append(roi)
                        labels.append(id)

    # Trains and saves trainer - .save() may not work on Pi
    recogniser.train(faceSamples, np.array(labels))
    recogniser.save("src/data/trainer.yml")
