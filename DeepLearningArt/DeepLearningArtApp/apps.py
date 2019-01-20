''' DeepLearningArtApp/apps.py '''
from django.apps import AppConfig
from DeepLearningArtApp.services.cv2_service import CV2Service

class DeeplearningartappConfig(AppConfig):
    ''' Override AppConfig to hook into app startup '''
    name = 'DeepLearningArtApp'

    def ready(self):
        ''' Override AppConfig.ready to hook into app startup and perform one time initialization'''
        # Initialize singletons
        CV2Service()
