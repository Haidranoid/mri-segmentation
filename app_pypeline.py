import os
import numpy as np
import nibabel as nib
import matplotlib
import math

matplotlib.use("Agg")
import matplotlib.pyplot as plt

def rotate_image(img, angle_deg):
    h, w = img.shape
    cx = (w - 1) / 2.0
    cy = (h - 1) / 2.0

    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    y, x = np.indices((h, w))

    x_shift = x - cx
    y_shift = y - cy

    x_src = cos_t * x_shift + sin_t * y_shift + cx
    y_src = -sin_t * x_shift + cos_t * y_shift + cy

    x_src = np.rint(x_src).astype(int)
    y_src = np.rint(y_src).astype(int)

    result = np.zeros_like(img)

    mask = (
        (x_src >= 0) & (x_src < w) &
        (y_src >= 0) & (y_src < h)
    )

    result[mask] = img[y_src[mask], x_src[mask]]

    return result


def scale_image(img, scale):
    h, w = img.shape
    new_h = int(h * scale)
    new_w = int(w * scale)

    y, x = np.indices((new_h, new_w))
    x_src = (x / scale).astype(int)
    y_src = (y / scale).astype(int)

    x_src = np.clip(x_src, 0, w - 1)
    y_src = np.clip(y_src, 0, h - 1)

    return img[y_src, x_src]


def translate_image(img, tx, ty):
    h, w = img.shape
    result = np.zeros_like(img)

    y, x = np.indices((h, w))

    x_src = x - tx
    y_src = y - ty

    mask = (
        (x_src >= 0) & (x_src < w) &
        (y_src >= 0) & (y_src < h)
    )

    result[mask] = img[y_src[mask], x_src[mask]]

    return result


def crop_image(img, x, y, width, height):
    return img[y:y + height, x:x + width]


def to_grayscale(img):
    return img


def main():
    input_path = "/input/image.nii"
    output_path = "/output/result.png"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró la imagen en {input_path}")

    nii = nib.load(input_path)
    vol = nii.get_fdata()

    img = vol[:, :, 74]

    # PIPELINE 🔥
    img = rotate_image(img, angle_deg=30)
    img = scale_image(img, scale=0.5)
    img = translate_image(img, tx=20, ty=20)
    img = to_grayscale(img)
    img = crop_image(img, 30, 30, 200, 200)

    # Guardar resultado
    plt.imshow(img, cmap="gray")
    plt.axis("off")

    os.makedirs("/output", exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

    print(f"Imagen procesada guardada en: {output_path}")


if __name__ == "__main__":
    main()