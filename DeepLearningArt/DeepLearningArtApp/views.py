 # DeepLearningArt/views.py
import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from DeepLearningArtApp.forms import ImageUploadForm
from django.forms import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from DeepLearningArtApp.services.CV2Service import CV2Service
from django.templatetags.static import static
from django.conf import settings
from django.http.response import HttpResponse

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', {'form' : ImageUploadForm()})

class UploadImageView(TemplateView):
    def post(self, request, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['file']

            # Ensure file size
            MAX_FILE_SIZE = 500
            if image_file.size > MAX_FILE_SIZE  * 1024:
                form.add_error("file", "File size is limited to %sKB" % MAX_FILE_SIZE)
            else:
                # File is good, save
                fs = FileSystemStorage()
                image_file_name = fs.save(image_file.name, image_file)
                uploaded_file_url = fs.url(image_file_name)
                return JsonResponse({"status":"true", "filePath": uploaded_file_url})
        # File content is invlalid or size exceeded
        return JsonResponse({"status": "false", "errors": [(k, v[0]) for k, v in form.errors.items()]})

class GetModelsView(TemplateView):
    def get(self, request, **kwargs):
        return JsonResponse({"status": "true", "modelThumbnailDir" : static('/images/modelThumbnail'), "models" : CV2Service().getModels()})

class DoMergeView(TemplateView):
    def post(self, request, **kwargs):
        try:
            image = request.POST.get("image", "")
            image_file_name = os.path.join(settings.MEDIA_ROOT, os.path.basename(image))
            model_name = request.POST.get("model", "")
            styled_image = CV2Service.styleTransfer(image_file_name, model_name)
            fs = FileSystemStorage()
            styled_image_url = fs.url(os.path.basename(styled_image))
            return JsonResponse({"status" : "true", "filePath" : styled_image_url})
        except Exception as e:
            return JsonResponse({"status" : "false", "error" : str(e)})

class DownloadImageView(TemplateView):
    def post(self, request, **kwargs):
        try:
            image = request.POST.get("image", "")
            image_file_name = os.path.join(settings.MEDIA_ROOT, os.path.basename(image))
            with open(image_file_name, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except Exception as e:
            return JsonResponse({"status" : "false", "error" : str(e)})