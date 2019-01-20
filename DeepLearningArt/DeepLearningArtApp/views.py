''' DeepLearningArtApp/views.py '''
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic import TemplateView
from DeepLearningArtApp.forms import ImageUploadForm
from DeepLearningArtApp.services.CV2Service import CV2Service
from DeepLearningArtApp.services.s3_service import S3Service

# Create your views here.
class HomePageView(TemplateView):
    ''' Class for handling home '''
    def get(self, request, *args, **kwargs):
        ''' Handle get home request '''
        return render(request, 'index.html', {'form' : ImageUploadForm()})

class UploadImageView(TemplateView):
    ''' Class for handling uploaded image '''
    @classmethod
    def post(cls, request):
        ''' Handle image upload post '''
        MAX_FILE_SIZE = 2000 #2Mb

        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['file']

            # Ensure file size
            if image_file.size > MAX_FILE_SIZE  * 1024:
                form.add_error("file", "File size is limited to %sKB" % MAX_FILE_SIZE)
            else:
                # File is good, save
                file_system = FileSystemStorage()
                image_file_name = file_system.save(image_file.name, image_file)
                file_system.url(image_file_name)

                # save to aws s3
                uploaded_file_url = S3Service().upload_file(os.path.join(settings.MEDIA_ROOT,
                                                                         image_file_name))

                return JsonResponse({"status":"true", "filePath":uploaded_file_url})

        # File content is invlalid or size exceeded
        return JsonResponse({"status": "false", 
                             "errors": [(k, v[0]) for k, v in form.errors.items()]})

class GetModelsView(TemplateView):
    ''' Class for retrieving info for available CV2 models '''
    def get(self, request, *args, **kwargs):
        ''' Handle get model info request '''
        return JsonResponse({"status": "true", 
                             "modelThumbnailDir" : static('/images/modelThumbnail'), 
                             "models" : CV2Service().getModels()})

class DoMergeView(TemplateView):
    ''' Class for performing info for available CV2 models '''
    def post(self, request):
        ''' Handle merge post request '''
        try:
            image = request.POST.get("image", "")
            image_file_name = os.path.join(settings.MEDIA_ROOT, os.path.basename(image))

            model_name = request.POST.get("model", "")
            styled_image = CV2Service.styleTransfer(image_file_name, model_name)

            # save to aws s3
            styled_image_url = S3Service().upload_file(os.path.join(settings.MEDIA_ROOT,
                                                                    styled_image))

            return JsonResponse({"status" : "true", "filePath" : styled_image_url})
        except Exception as exception:
            return JsonResponse({"status" : "false", "error" : str(exception)})

class DownloadImageView(TemplateView):
    ''' Class for retrieving an image '''
    def post(self, request):
        ''' Handle request image post request '''

        try:
            image = request.POST.get("image", "")
            image_file_name = os.path.join(settings.MEDIA_ROOT, os.path.basename(image))
            with open(image_file_name, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except Exception as exception:
            return JsonResponse({"status" : "false", "error" : str(exception)})
