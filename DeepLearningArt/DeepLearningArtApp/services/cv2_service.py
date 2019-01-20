''' DeepLearningArtApp/services/cv2_service.py '''
import os
import asyncio
import pathlib
import time
import cv2
from django.conf import settings
from django.templatetags.static import static

# To avoid E1101 warning on cv2
# pylint: disable=no-member

class CV2Service(object):
    ''' Singleton pattern class used for interacting with OpenCV '''
    __instance = None

    class __CV2Service:
        ''' Internal private class used to implement singleton pattern '''
        def __init__(self):
            return

    def __init__(self):
        if not CV2Service.__instance:
            CV2Service.__instance = CV2Service.__CV2Service()
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.background())

    @staticmethod
    def get_models():
        ''' Get the transformation model info '''

        models = pathlib.Path(settings.MODEL_DIR).glob("*.t7")
        return [model.stem for model in models]

    @classmethod
    def resize(cls, image, width=None, height=None, inter=cv2.INTER_AREA):
        """ Resize the given image """

        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (image_height, image_width) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the dimensions
            ratio = height / float(image_height)
            dim = (int(image_width * ratio), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the dimensions
            ratio = width / float(image_width)
            dim = (width, int(image_height * ratio))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    @classmethod
    def style_transfer(cls, image_file, model):
        """ Apply the model's style transfer on the given image """

        model_file = os.path.join(settings.MODEL_DIR, model + ".t7")

        net = cv2.dnn.readNetFromTorch(model_file)

        # load the input image, resize it to have a width of 600 pixels, and
        # then grab the image dimensions
        image = cv2.imread(image_file)

        image = cls.resize(image, width=600)
        (height, width) = image.shape[:2]  

        # construct a blob from the image, set the input, and then perform a
        # forward pass of the network
        blob = cv2.dnn.blobFromImage(image, 1.0, (width, height),
                                     (103.939, 116.779, 123.680), swapRB=False, crop=False)
        net.setInput(blob)
        output = net.forward()

        # reshape the output tensor, add back in the mean subtraction, and
        # then swap the channel ordering
        output = output.reshape((3, output.shape[2], output.shape[3]))
        output[0] += 103.939
        output[1] += 116.779
        output[2] += 123.680
        output /= 255.0
        output = output.transpose(1, 2, 0)

        output = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX)
        output_file = image_file[:-4] + "_ouput_" + time.strftime("%Y%m%d%H%M%S") + ".jpg"
        cv2.imwrite(output_file, output)
        return output_file

    @staticmethod
    async def init_cl_runtime():
        ''' Async method to load CL Runtime '''
        image_file = os.path.join(settings.STATICFILES_DIR,
                                  'images', 'modelThumbnail', 'candy.jpg')
        model_file = os.path.join(settings.MODEL_DIR, "candy.t7")

        net = cv2.dnn.readNetFromTorch(model_file)

        image = cv2.imread(image_file)
        image = cv2.resize(image, (100, 100))
        (height, width) = image.shape[:2]

        blob = cv2.dnn.blobFromImage(image, 1.0, (width, height),
                                     (103.939, 116.779, 123.680), swapRB=False, crop=False)
        net.setInput(blob)
        net.forward()
        return

    @classmethod
    async def background(cls):
        ''' Async method to initialize class in background '''
        asyncio.ensure_future(cls.init_cl_runtime())
        return
