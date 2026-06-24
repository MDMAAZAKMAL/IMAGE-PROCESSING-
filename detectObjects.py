import cv2
import numpy as np

# ---------------------------
# 1. Load YOLO model
# ---------------------------
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Read classes
with open("coco.names", "r") as f:
    classes = f.read().splitlines()

def detect_object(paths):
    for path in paths:

        # ---------------------------
        # 2. Load image
        # ---------------------------
        img = cv2.imread(path)
        height, width, _ = img.shape

        # ---------------------------
        # 3. Convert image to YOLO blob
        # ---------------------------
        blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416),
                                    swapRB=True, crop=False)
        net.setInput(blob)

        # ---------------------------
        # 4. Get output layers
        # ---------------------------
        layer_names = net.getLayerNames()
        unconnected = net.getUnconnectedOutLayers()
        output_layers = [layer_names[int(i) - 1] for i in unconnected]

        # ---------------------------
        # 5. Forward pass
        # ---------------------------
        outputs = net.forward(output_layers)

        # ---------------------------
        # 6. Extract bounding boxes
        # ---------------------------
        boxes = []
        confidences = []
        class_ids = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # ---------------------------
        # 7. Apply Non-Max Suppression
        # ---------------------------
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # ---------------------------
        # 8. Draw bounding boxes
        # ---------------------------
        if len(indexes) > 0:
            for idx in indexes:
                idx = int(idx)         # normalize index
                x, y, w, h = boxes[idx]
                label = classes[class_ids[idx]]
                color = (0, 255, 0)

                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        else:
            print("No objects detected.")

        # ---------------------------
        # 9. Show the result
        # ---------------------------
        cv2.imshow("Object Detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
