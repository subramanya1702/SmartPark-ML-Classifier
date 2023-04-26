import datetime
import random
import string
from datetime import datetime

import cv2
import pafy


def image_fetcher(url):
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    capture = cv2.VideoCapture()
    capture.open(best.url)

    success, fetched_image = capture.read()

    current_date = datetime.now()
    str_date = current_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    # initializing size of string
    string_length = 7

    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=string_length))
    filename = str_date + '_' + res + '.jpg'

    return fetched_image, filename, current_date.timestamp()

    cv2.destroyAllWindows()
    capture.release()
