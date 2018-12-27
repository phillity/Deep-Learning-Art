"""Production settings and globals."""

from __future__ import absolute_import

import os

from DeepLearningArt.settings.base import *

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']