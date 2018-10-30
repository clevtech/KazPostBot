from imageai.Detection import ObjectDetection
import os
import cv2
import numpy as np
import glob


files = glob.glob("./video/*.png")

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo-tiny.h5"))
detector.loadModel()

for file in files:
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , file), output_image_path=os.path.join(execution_path , file+".2.png"), minimum_percentage_probability=5)

    for eachObject in detections:
        print(str(eachObject["name"]) + " : " + str(eachObject["percentage_probability"]) + " : " + str(eachObject["box_points"]))
        print("--------------------------------")
