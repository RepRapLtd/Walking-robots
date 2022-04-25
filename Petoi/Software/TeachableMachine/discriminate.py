
# Supress warnings about no GPU libraries
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

import time


def GetImage(name):
    image = Image.open(name)
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image.show()
    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    return normalized_image_array

# Load the model
model = load_model('keras_model.h5', compile=False)
#model.compile()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image

# Load the image into the array
data[0] = GetImage('ab-test2.jpg')

start_time = time.time()
# run the inference
prediction = model.predict(data)
end_time = time.time()

print(prediction)
print("--- %s seconds ---" % (end_time - start_time))
