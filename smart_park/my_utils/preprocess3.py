import os

import cv2
import numpy as np


def pre_process(PREPROCESSING_CONFIG, fetched_image, filename):
    original_image_dir_path = PREPROCESSING_CONFIG["original-image"]
    preprocess_image_dir_path = PREPROCESSING_CONFIG["preprocessed-image-dir-save-path"]
    x_coordinate = PREPROCESSING_CONFIG["x-coordinate"]
    y_coordinate = PREPROCESSING_CONFIG["y-coordinate"]
    height = PREPROCESSING_CONFIG["height"]
    width = PREPROCESSING_CONFIG["width"]

    # Convert the original image to gray scale and crop it later
    downscaled_image = cv2.cvtColor(fetched_image, cv2.COLOR_BGR2GRAY)
    pre_processed_image = downscaled_image[int(y_coordinate): int(y_coordinate) + int(height),
                          int(x_coordinate): int(x_coordinate) + int(width)]

    # Crop the original image and save it under pre_processed_image directory
    fetched_image = fetched_image[int(y_coordinate): int(y_coordinate) + int(height),
                    int(x_coordinate): int(x_coordinate) + int(width)]
    cv2.imwrite(os.path.join(original_image_dir_path, filename), fetched_image)

    pts = np.array(
        [[0, 73], [208, 71], [138, 188], [260, 190], [359, 194], [453, 197], [547, 202], [645, 206], [739, 206],
         [837, 210], [937, 214], [1000, 214], [1000, 312], [971, 254],
         [954, 237], [841, 235], [718, 235], [578, 228], [508, 225], [434, 220], [318, 222], [109, 217], [39, 367],
         [0, 367]], np.int32)
    pts = pts.reshape((-1, 1, 2))

    pts2 = np.array(
        [[0, 63], [226, 63], [319, 67], [397, 73], [479, 77], [558, 81], [639, 82], [721, 84], [800, 85], [882, 87],
         [1000, 89], [1000, 252], [973, 252], [934, 214],
         [911, 110], [916, 103], [772, 103], [631, 99], [530, 95], [383, 92], [195, 79], [0, 79]],
        np.int32)
    pts2 = pts2.reshape((-1, 1, 2))

    pts3 = np.array(
        [[0, 0], [1000, 0], [1000, 34], [811, 34], [702, 32], [575, 29], [468, 27], [241, 24], [231, 24], [226, 63],
         [0, 63]], np.int32)
    pts3 = pts3.reshape((-1, 1, 2))

    cv2.fillPoly(pre_processed_image, [pts3], (255, 255, 255))

    cv2.fillPoly(pre_processed_image, [pts2], (255, 255, 255))
    poly_image = cv2.fillPoly(pre_processed_image, [pts], (255, 255, 255))
    cv2.imwrite(os.path.join(preprocess_image_dir_path, filename), pre_processed_image)
    print(f"the preprocessed image is stored at {preprocess_image_dir_path}")
