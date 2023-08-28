from ultralytics import YOLO
import cv2
import math


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

users=[]

def PersonDetection():
    # start webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    images = []

    # while True:
    #getting one image from he webcam
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        images = []
        boxes = r.boxes
        counter = 0

        for box in boxes:
            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            if (classNames[cls] == "person"):
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
                users.append((x1, y1, x2, y2))

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                print("{}  {}  {}  {}".format(x1, y1, x2, y2))
                # pose_estimator_dim.append([(x1, y1), (x2, y2)])
                cropped_img = img[y1:y2, x1:x2]

                cv2.line(cropped_img, (0, 0), (511, 511), (255, 0, 0), 5)
                cv2.imshow(("Cropped Image{}".format(counter)), cropped_img)
                counter += 1

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                cv2.imshow('Webcam', img)
                cv2.waitKey()
                # if cv2.waitKey(1) == ord('q'):
                #     break
                cap.release()

                cv2.destroyAllWindows()
    return users

print(PersonDetection())





