import configparser
import os

import cv2


def pre_process(fetched_image, preprocess_image_dir_path, filename):
    config_obj = configparser.ConfigParser()
    config_obj.read("/home/ubuntu/mongodb/database/config.ini")
    PREPROCESSING_CONFIG = config_obj["PRE_PROCESSING_BOUNDS"]

    downscaled_image = cv2.cvtColor(fetched_image, cv2.COLOR_BGR2GRAY)

    x_coordinate = PREPROCESSING_CONFIG["x-coordinate"]
    y_coordinate = PREPROCESSING_CONFIG["y-coordinate"]
    height = PREPROCESSING_CONFIG["height"]
    width = PREPROCESSING_CONFIG["width"]

    pre_processed_image = downscaled_image[int(y_coordinate): int(y_coordinate) + int(height),
                          int(x_coordinate): int(x_coordinate) + int(width)]
    cv2.imwrite(os.path.join(preprocess_image_dir_path, filename), pre_processed_image)
    print(f"the preprocessed image is stored at {preprocess_image_dir_path}")
    return pre_processed_image
