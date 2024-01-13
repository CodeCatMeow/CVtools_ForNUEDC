import cv2

import sys

sys.path.append(sys.path[0] + "\\..\\")
from lib.ROI import ROI
from lib import Video

if __name__ == "__main__":
    cap = Video.CaptureInit(0, PI_MODE=False)

    while cap.isOpened():
        ret, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        part1 = cv2.inRange(
            hsv,
            Video.ColorSegHSV.RED_RANGE_1[0],
            Video.ColorSegHSV.RED_RANGE_2[1],
        )
        part2 = cv2.inRange(
            hsv,
            Video.ColorSegHSV.RED_RANGE_2[0],
            Video.ColorSegHSV.RED_RANGE_2[1],
        )
        part = cv2.bitwise_or(part1, part2)

        roi = ROI(part, 0.1, 0.3, 0.4, 0.2)

        roi.draw(part)
        print(
            "ratio:%.3f, point inside: %d"
            % (roi.getRatio(), int(roi.isInside((0.2, 0.4))))
        )

        cv2.imshow("1", frame)
        cv2.imshow("2", part)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
