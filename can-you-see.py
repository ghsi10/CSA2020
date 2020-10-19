import cv2
import numpy as np
from PIL import Image

pixels = []
cam = cv2.VideoCapture("Can_You_See_It.mp4")
ret, frame = cam.read()
counter = 0
while ret:
    pixels.append(frame[0][0])
    ret, frame = cam.read()
    counter += 1

for i in range(1440, 1450, 1):
    tmp_array = pixels
    while len(tmp_array) % i != 0:
        tmp_array.append(pixels[0])
    array2d = np.reshape(np.asarray(tmp_array), (-1, i, 3))
    new_image = Image.fromarray(array2d)
    new_image.save(f"data/{i}.png")

cam.release()
cv2.destroyAllWindows()
