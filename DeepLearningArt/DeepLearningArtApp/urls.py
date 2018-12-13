# DeepLearningArt/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from DeepLearningArtApp import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^upload/image/$', views.UploadImageView.as_view(), name='upload_image'),
    url(r'^models/$', views.GetModelsView.as_view(), name='get_models'),
    url(r'^merge/$', views.DoMergeView.as_view(), name='do_merge'),
    url(r'^download/image/$', views.DownloadImageView.as_view(), name='download_image'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)