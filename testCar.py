from lib import Car

import cv2

sam = [Car.Sample(0.3, 0.3), Car.Sample(0.5, 0.4), Car.Sample(0.7, 0.3)]

if __name__ == '__main__':
    image = cv2.imread('test\\4.png', cv2.IMREAD_GRAYSCALE)

    Car.getDistance(image, sam, 0, Car.Sample.SAMPLE_COLUMN, ifDraw=True, ifPrint=True)

    Car.getLineSlope(image, sam, Car.Sample.SAMPLE_COLUMN, ifPrint=True, ifDraw=True)

    # sample: Car.Sample
    # for sample in sam:
    #     x, y = sample.centerPoint(image, Car.Sample.COLUMN_MODE)
    #     cv2.circle(image, (x, y), 5, (0, 180, 0), -1)

    cv2.imshow('img', image)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()