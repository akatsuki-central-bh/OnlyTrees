import os
import cv2

class FingerPrint():
    def __init__(self, file):
        self.input_image = cv2.imread(file)

        self.best_score = 0

        self.filename = None
        self.image = None
        self.keypoints_1 = None
        self.keypoints_2 = None
        self.match_points = None

    def call(self):
        file_names = os.listdir('SOCOFing/Real')
        for filename in file_names:
            fingerprint_image = cv2.imread(f'SOCOFing/Real/{filename}')
            sift = cv2.SIFT_create()

            keypoints_1, descriptors_1 = sift.detectAndCompute(self.input_image, None)
            keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

            matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},
                                            {}).knnMatch(descriptors_1, descriptors_2, k=2)

            match_points = []

            for p, q in matches:
                if p.distance < 0.1 * q.distance:
                    match_points.append(p)

            keypoints = 0
            if len(keypoints_1) < len(keypoints_2):
                keypoints = len(keypoints_1)
            else:
                keypoints = len(keypoints_2)

            score = len(match_points) / keypoints * 100

            if score > self.best_score:
                self.best_score = score
                self.filename = filename
                self.image = fingerprint_image
                self.keypoints_1 = keypoints_1
                self.keypoints_2 = keypoints_2
                self.match_points = match_points
