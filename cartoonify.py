"""Core cartoon-effect logic using OpenCV.

Idea: Cartoon = (thick black edges) + (smooth, flat colors)
  1. Edges  : grayscale -> median blur -> adaptive threshold
  2. Colors : bilateral filter (smooths colors but keeps edges sharp)
              [optional] K-Means to reduce number of colors ("painted" style)
  3. Combine: bitwise_and(color, color, mask=edges)
"""
import argparse

import cv2
import numpy as np


def resize_max(img, max_side=900):
    """Resize big images so processing stays fast."""
    h, w = img.shape[:2]
    scale = max_side / max(h, w)
    if scale < 1:
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return img


def get_edges(img, line_size=9, blur=7):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, blur)
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, 9
    )


def smooth_colors(img, passes=2):
    for _ in range(passes):
        img = cv2.bilateralFilter(img, d=9, sigmaColor=200, sigmaSpace=200)
    return img


def reduce_colors(img, k=8):
    """K-Means color quantization: keep only k dominant colors."""
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 3, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    return centers[labels.flatten()].reshape(img.shape)


def cartoonify(img, style="classic", colors=8, line_size=9):
    """img: BGR numpy array. style: 'classic' or 'painted'."""
    img = resize_max(img)
    edges = get_edges(img, line_size=line_size)
    color = smooth_colors(img)
    if style == "painted":
        color = reduce_colors(color, k=colors)
    return cv2.bitwise_and(color, color, mask=edges)


def main():
    parser = argparse.ArgumentParser(description="Cartoonify an image")
    parser.add_argument("input", help="path of input image")
    parser.add_argument("-o", "--output", default="cartoon.jpg")
    parser.add_argument("-s", "--style", choices=["classic", "painted"], default="classic")
    parser.add_argument("-k", "--colors", type=int, default=8)
    args = parser.parse_args()

    img = cv2.imread(args.input)
    if img is None:
        raise SystemExit("Image read nahi hui. Path check karo.")
    cv2.imwrite(args.output, cartoonify(img, args.style, args.colors))
    print("Saved:", args.output)


if __name__ == "__main__":
    main()
