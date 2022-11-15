import os
import glob
import cv2
import re

class FingerPrint():
    def __init__(self, file):
        self.input_image = cv2.imread(file)

        self.best_score = 0
        self.filename = None

    def call(self):
        file_names = glob.glob('app/database/images/user/fingerprints/*.BMP')

        for filename in file_names:
            try:
                fingerprint_image = cv2.imread(filename)
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
            except Exception as e:
                print(str(e))

        return re.findall('\d+', self.filename)[-1]
