from PIL import Image
import numpy as np

img = Image.open("data/test_gray/images/awake.4a67650a-630e-11f0-9680-586c258032ce.jpg")
print("Mode:", img.mode)
np_img = np.array(img)
print("Shape:", np_img.shape)
print("Unique channels:", np.unique(np_img[..., 0]), np.unique(np_img[..., 1]), np.unique(np_img[..., 2]))
