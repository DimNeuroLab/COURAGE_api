import numpy as np
import cv2
from path_setup import get_working_dir


def object_detection_algorithm(image, input_confidence=0.5, input_threshold=0.3, swap_rb=False):
    labels = open(get_working_dir() + '/courage_algorithms/models/object_detector/coco.names').read().strip().split("\n")
    net = cv2.dnn.readNetFromDarknet(get_working_dir() + '/courage_algorithms/models/object_detector/yolov3.cfg',
                                     get_working_dir() + '/courage_algorithms/models/object_detector/yolov3.weights')
    (H, W) = image.shape[:2]
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=swap_rb, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(ln)

    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > input_confidence:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idc = cv2.dnn.NMSBoxes(boxes, confidences, input_confidence, input_threshold)

    output = {'objects': []}

    if len(idc) > 0:
        for i in idc.flatten():
            x = boxes[i][0]
            y = boxes[i][1]
            w = boxes[i][2]
            h = boxes[i][3]
            single_object = {'label': str(labels[class_ids[i]]),
                             'x': str(x),
                             'y': str(y),
                             'w': str(w),
                             'h': str(h)}
            output['objects'].append(single_object)

    return output
