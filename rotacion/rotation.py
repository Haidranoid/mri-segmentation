import cv2
import numpy as np
import math
from pathlib import Path

def main():

    ruta = Path("./jeff.png")

    img = cv2.imread(ruta, 0)
    h, w = img.shape

    angulo = 30
    theta = math.radians(angulo)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    cx = w // 2
    cy = h // 2


    rotada = np.zeros_like(img)

    for y in range(h):
        for x in range(w):

            x_shift = x - cx
            y_shift = y - cy

            x_rot = cos_t * x_shift - sin_t * y_shift
            y_rot = sin_t * x_shift + cos_t * y_shift

            x_final = int(round(x_rot + cx))
            y_final = int(round(y_rot + cy))


            if 0 <= x_final < w and 0 <= y_final < h:
                rotada[y_final, x_final] = img[y, x]

    cv2.imshow("Original", img)
    cv2.imshow("Rotated (Matriz Manual)", rotada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()