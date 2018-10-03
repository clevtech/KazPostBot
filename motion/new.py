from imageai.Detection import ObjectDetection
import os
import freenect, cv2
import numpy as np


execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()
depth,_ = freenect.sync_get_depth()
np.clip(depth, 0, 2**10 - 1, depth)
depth >>= 2
depth = depth.astype(np.uint8)
array = cv2.GaussianBlur(depth, (5, 5), 0)
cv2.imwrite("image2.png", array);
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "image2.png"), output_image_path=os.path.join(execution_path , "image2new.png"), minimum_percentage_probability=30)

for eachObject in detections:
    print(str(eachObject["name"]) + " : " + str(eachObject["percentage_probability"]) + " : " + str(eachObject["box_points"]))
    print("--------------------------------")
