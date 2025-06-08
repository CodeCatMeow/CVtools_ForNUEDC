import cv2
import os

import sys

sys.path.append(sys.path[0] + "\\..\\")

from lib import FastestDet

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    det = FastestDet.FastestDet(512, 512, path, ifDrawOutput=True)
    image = cv2.imread("example/test/7.jpg", cv2.IMREAD_COLOR)
    detOut = det.putout(image)
    cv2.imshow("output", image)
    print(detOut)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
