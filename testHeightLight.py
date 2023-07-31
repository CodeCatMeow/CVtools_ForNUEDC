import cv2
import numpy as np


def CaptureInit(index: int = 0,
                width: int = 64,
                height: int = 48,
                PI_MODE=True) -> cv2.VideoCapture:
    "摄像头配置和打开"
    if PI_MODE:
        capture = cv2.VideoCapture(index)
    else:
        capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return capture


def Adaptive_light_correction(img: np.ndarray):
    height = img.shape[0]
    width = img.shape[1]

    HSV_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    V = HSV_img[:, :, 2]

    kernel_size = min(height, width)
    if kernel_size % 2 == 0:
        kernel_size -= 1

    SIGMA1 = 15
    SIGMA2 = 80
    SIGMA3 = 250
    q = np.sqrt(2.0)
    F = np.zeros((height, width, 3), dtype=np.float64)
    F[:, :, 0] = cv2.GaussianBlur(V, (kernel_size, kernel_size), SIGMA1 / q)
    F[:, :, 1] = cv2.GaussianBlur(V, (kernel_size, kernel_size), SIGMA2 / q)
    F[:, :, 2] = cv2.GaussianBlur(V, (kernel_size, kernel_size), SIGMA3 / q)
    F_mean = np.mean(F, axis=2)
    average = np.mean(F_mean)
    gamma = np.power(0.5, np.divide(np.subtract(average, F_mean), average))
    out = np.power(V / 255.0, gamma) * 255.0
    HSV_img[:, :, 2] = out
    img = cv2.cvtColor(HSV_img, cv2.COLOR_HSV2BGR)
    return img



def highlight_remove(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)#一定要转换成float32，否则会出错
    # img = cv2.resize(img, (512, 512)).astype(np.float32)#如图片分辨率较大，直接resize到512会比较快
    dst = img.copy()
    h, w = img.shape[:2]
    for i in range(h):
        for j in range(w):
            R = img[i, j, 0]
            G = img[i, j, 1]
            B = img[i, j, 2]
            alpha_r = R/(R+G+B)
            alpha_g = G/(R+G+B)
            alpha_b = B/(R+G+B)
            # alpha = max(max(alpha_r, alpha_g), alpha_b)
            MaxC = max(max(R, G), B)
            minalpha = min(min(alpha_r, alpha_g), alpha_b)
            gama_r = (alpha_r - minalpha) / (1 - 3 * minalpha)
            gama_g = (alpha_g - minalpha) / (1 - 3 * minalpha)
            gama_b = (alpha_b - minalpha) / (1 - 3 * minalpha)
            gama = max(max(gama_r, gama_g), gama_b)
 
            temp = (gama * (R + G + B) - MaxC) / (3 * gama - 1)
            dst[i, j, 0] = np.clip(R-(temp+0.5), 0, 255)
            dst[i, j, 1] = np.clip(G-(temp+0.5), 0, 255)
            dst[i, j, 2] = np.clip(B-(temp+0.5), 0, 255)
    return np.clip(dst[:, :, ::-1], 0, 255)





if __name__ == "__main__":
    cap = CaptureInit(0)

    while True:
        ret, frame = cap.read()
        print('in')

        cv2.imshow('frame', frame)

        # dst = Adaptive_light_correction(frame)
        dst = highlight_remove(frame)
        cv2.imshow('dst', dst)

        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # mv = cv2.split(hsv)
        # channelV = mv[2]  # 提取得到V通道

        # gammaT = sqrt(2)
        # sigma1 = 15
        # sigma2 = 80
        # sigma3 = 250

        # V_1 = cv2.GaussianBlur(channelV, (333, 333), sigma1 / gammaT)
        # V_2 = cv2.GaussianBlur(channelV, (333, 333), sigma2 / gammaT)
        # V_3 = cv2.GaussianBlur(channelV, (333, 333), sigma3 / gammaT)

        # sumV = cv2.addWeighted(V_1, 1/2, V_2, 1/2, 0)
        # sumV = cv2.addWeighted(sumV, 2/3, V_3, 1/3, 0)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()