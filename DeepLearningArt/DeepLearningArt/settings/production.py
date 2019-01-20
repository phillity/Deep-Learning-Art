""" DeepLearningArt/production.py settings and globals."""

from __future__ import absolute_import
from DeepLearningArt.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']
