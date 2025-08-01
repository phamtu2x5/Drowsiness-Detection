from PIL import Image
import numpy as np

img = Image.open("data/images/001_glasses_nonsleepyCombination_0_notdrowsy copy.jpg")
print("Mode:", img.mode)
np_img = np.array(img)
print("Shape:", np_img.shape)
print("Unique channels:", np.unique(np_img[..., 0]), np.unique(np_img[..., 1]), np.unique(np_img[..., 2]))
