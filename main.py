import cv2 as cv
import numpy as np
from object_detection import ObjectDetection
import math

#Initialize Object Detection
od = ObjectDetection()

cap = cv.VideoCapture('traffic.mp4')

#Initialize count
count = 0
center_points_prev = []
tracking_object = {}
track_id = 0

while True:
    ret, frame = cap.read()
    count += 1

    center_points_curr = []

    if ret == True:
        (class_ids, scores, boxes) = od.detect(frame)
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w) / 2)
            cy = int((y + y + h) / 2)
            center_points_curr.append((cx, cy))
            print("frame no", count, " ", x, y, w, h)


            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if count <= 2:
            for pt in center_points_curr:
                for pt2 in center_points_prev:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                    if distance < 10:
                        tracking_object[track_id] = pt
                        track_id += 1
        else:

            tracking_object_copy = tracking_object.copy()
            center_points_curr_copy = center_points_curr.copy()

            for object_id, pt2 in tracking_object_copy.items():

                object_exists = False

                for pt2 in center_points_curr_copy:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    #update object position
                    if distance < 10:
                        tracking_object[object_id] = pt
                        object_exists = True

                        # if center_points_curr:
                        #   center_points_curr.remove(pt)
                        #   continue

                if not object_exists:
                    tracking_object.pop(object_id)

            for pt in center_points_curr:
                tracking_object[track_id] = pt
                track_id += 1


        for object_id, pt in tracking_object.items():
            cv.circle(frame, pt, 5, (0, 0, 255), -1)
            cv.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 255, 0), 1)




        cv.imshow("Video", frame)

     # keep a copy of center point of curr points for next frame
    center_points_prev = center_points_curr.copy()


    if not ret:
        print("can't receive frames furthur")
        break

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()