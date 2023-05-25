from cv2 import CascadeClassifier, CASCADE_SCALE_IMAGE, COLOR_BGR2GRAY, cvtColor, imread, imwrite, rectangle
from os.path import join, abspath, dirname

class FaceDetector:

    DETECTOR_PATH = join(abspath(dirname(__name__)), 'src/static/haarcascade_frontalface_default.xml')

    def __init__(self) -> None:
        self.__faceCascade = CascadeClassifier(self.DETECTOR_PATH)

    def getDetectedFaces(self, image):
        return self.__faceCascade.detectMultiScale(
            cvtColor(image, COLOR_BGR2GRAY),
            scaleFactor = 1.3,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = CASCADE_SCALE_IMAGE
        )

    def drawRectangleOnImage(self, imagePath, image, faces):
        if (0 == len(faces)): return
        
        for (x, y, w, h) in faces:
            rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 5)

            imwrite(imagePath, image)

    def detect(self, imagePath: str):

        image = imread(imagePath)

        faces = self.getDetectedFaces(image)

        self.drawRectangleOnImage(imagePath, image, faces)
