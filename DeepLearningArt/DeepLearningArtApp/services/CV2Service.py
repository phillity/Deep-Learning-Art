import asyncio
import cv2
import os
import pathlib
import time
from django.conf import settings

# Class defined using Singleton Pattern - https://gist.github.com/lalzada/3938daf1470a3b7ed7d167976a329638
class CV2Service(object):
    instance = None
    initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            cls.initialized = False
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'initialized') or not self.initialized:
            self.initialized = True
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.background())

    @staticmethod
    def getModels() :
        models = pathlib.Path(settings.MODEL_DIR).glob("*.t7")
        return [model.stem for model in models]
    
    @classmethod
    def resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        """Resize the given image"""
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    @classmethod
    def styleTransfer(self, image_file, model):
        """Apply the model's style transfer on the given image"""

        model_file = os.path.join(settings.MODEL_DIR, model + ".t7")

        net = cv2.dnn.readNetFromTorch(model_file)

        # load the input image, resize it to have a width of 600 pixels, and
        # then grab the image dimensions
        image = cv2.imread(image_file)

        image = self.resize(image, width=600)
        (h, w) = image.shape[:2]
    

        # construct a blob from the image, set the input, and then perform a
        # forward pass of the network
        blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
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
    async def initClRuntime():
        image_file = os.path.join(settings.BASE_DIR, 'DeepLearningArtApp/static/images/modelThumbnail/candy.jpg')
        model_file = os.path.join(settings.MODEL_DIR, "candy.t7")
        net = cv2.dnn.readNetFromTorch(model_file)
        
        image = cv2.imread(image_file)
        image = cv2.resize(image,(100,100))
        (h, w) = image.shape[:2]

        blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
            (103.939, 116.779, 123.680), swapRB=False, crop=False)
        net.setInput(blob)
        net.forward()
        return
    
    @classmethod
    async def background(self):
        asyncio.ensure_future(self.initClRuntime())
        return