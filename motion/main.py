from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "Resnet.h5"))
detector.loadModel("fast")

video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "./video/NEED.mp4"),
                                output_file_path=os.path.join(execution_path, "traffic_detected")
                                , frames_per_second=1, log_progress=True)
print(video_path)
