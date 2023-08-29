from ultralytics import YOLO
from PIL import Image
import cv2
import math
import os

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

users = []


def PersonDetection():
    '''
    :return: detects people in the image, returns a tuple of image
    and dictionary with number of bounding box and their coordinattes
    '''
    # start webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # create a folder for all the images
    path = "images"
    if not os.path.exists(path):
        # Create a new directory because it does not exist
        os.makedirs(path)

    images = []

    # while True:
    # getting one image from he webcam
    success, img = cap.read()
    results = model(img, stream=True)
    counter = 0
    dict = {}
    # coordinates
    for r in results:
        images = []
        boxes = r.boxes
        counter = 1

        for box in boxes:
            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            if (classNames[cls] == "person"):
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
                coordinates = (x1, y1, x2, y2)
                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                print("{}  {}  {}  {}".format(x1, y1, x2, y2))
                dict[counter] = ((x1, y1, x2, y2))
                # pose_estimator_dim.append([(x1, y1), (x2, y2)])
                cropped_img = img[y1:y2, x1:x2]

                cv2.line(cropped_img, (0, 0), (511, 511), (255, 0, 0), 5)
                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                label = str(counter)
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, (255, 0, 255), 3)
                #cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
                cv2.putText(img, label, (x1, y1 - 2), font, fontScale, color, thickness)

                cv2.imshow(("Cropped Image{}".format(counter)), cropped_img)
                counter += 1
                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                cv2.imshow('Webcam', img)
                # Save Frame by Frame into disk using imwrite method
                cv2.imwrite(f'{path}/Bounded_image' + str(counter) + '.jpg', img)
                imagepath = f'{path}/Bounded_image' + str(counter) + '.jpg'
                cap.release()
                cv2.destroyAllWindows()
    return (imagepath, dict)
