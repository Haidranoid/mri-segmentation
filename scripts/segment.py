import os
import io
import base64
import argparse

import numpy as np
import nibabel as nib
import matplotlib

from scripts.rotate_image import rotate_image

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from skimage import filters


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--angle", type=float, default=0)
    parser.add_argument("--slice", type=int, default=74)
    parser.add_argument("--use_otsu", type=str, default="true")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--normalize", type=str, default="true")
    parser.add_argument("--handle_nan", type=str, default="true")
    parser.add_argument("--bins", type=int, default=256)

    return parser.parse_args()


def str_to_bool(value):
    return value.lower() in ["true", "1", "yes"]


def main():
    args = parse_args()

    use_otsu = str_to_bool(args.use_otsu)
    normalize = str_to_bool(args.normalize)
    handle_nan = str_to_bool(args.handle_nan)

    # Ruta NIfTI
    ruta = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "..",
        "static",
        "Brain",
        "img1t1.nii"
    ))

    nii = nib.load(ruta)
    vol = nii.get_fdata()

    img = vol[:, :, args.slice]

    if args.angle != 0:
        img = rotate_image(img, args.angle)

    if handle_nan:
        img = np.nan_to_num(img)

    if normalize:
        min_val = np.min(img)
        max_val = np.max(img)
        if max_val - min_val != 0:
            img = (img - min_val) / (max_val - min_val)

    if use_otsu:
        thresh = filters.threshold_otsu(img)
    else:
        thresh = args.threshold

    binary = img > thresh

    # Figura completa
    fig = plt.figure(figsize=(18, 5))

    # Original
    ax1 = fig.add_subplot(1, 4, 1)
    ax1.imshow(img, cmap="gray")
    ax1.set_title("Original")
    ax1.axis("off")

    # Histograma
    ax2 = fig.add_subplot(1, 4, 2)
    ax2.hist(img.ravel(), bins=args.bins)
    ax2.axvline(thresh, color="red")
    ax2.set_title("Histograma")

    # Segmentación
    ax3 = fig.add_subplot(1, 4, 3)
    ax3.imshow(binary, cmap="gray")
    ax3.set_title("Segmentación")
    ax3.axis("off")

    # Overlay
    ax4 = fig.add_subplot(1, 4, 4)
    ax4.imshow(img, cmap="gray")
    ax4.imshow(binary, cmap="jet", alpha=0.35)
    ax4.set_title("Overlay")
    ax4.axis("off")

    plt.tight_layout()

    # Guardar imagen en memoria
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    print(image_base64)

if __name__ == "__main__":
    main()