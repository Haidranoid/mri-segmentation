import numpy as np
import math

def rotate_image(img, angle_deg):
    """
    Rota una imagen 2D (grayscale) alrededor de su centro usando
    inverse mapping y NumPy vectorizado (sin loops Python).
    """
    h, w = img.shape
    cx = (w - 1) / 2.0
    cy = (h - 1) / 2.0

    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    # Grid de coordenadas destino
    y, x = np.indices((h, w))

    # Trasladar al centro
    x_shift = x - cx
    y_shift = y - cy

    # Inverse rotation (destino -> origen)
    x_src =  cos_t * x_shift + sin_t * y_shift + cx
    y_src = -sin_t * x_shift + cos_t * y_shift + cy

    # Redondeo al vecino más cercano
    x_src = np.rint(x_src).astype(int)
    y_src = np.rint(y_src).astype(int)

    # Imagen destino
    rot = np.zeros_like(img)

    # Máscara de coordenadas válidas
    mask = (
        (x_src >= 0) & (x_src < w) &
        (y_src >= 0) & (y_src < h)
    )

    # Asignación vectorizada
    rot[mask] = img[y_src[mask], x_src[mask]]

    return rot