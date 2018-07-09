from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^Home/$', views.loadHome, name='loadHome'),
    url(r'^Demo_page_load_cls/$', views.Demo_page_load_cls, name='Demo_page_load_cls'),
    url(r'^predict_file/$', views.predict_file, name='predict_file'),
    url(r'^predict_file1/$', views.predict_file1, name='predict_file1'),
    url(r'^Classification_page_load_cls/$', views.Classification_page_load_cls, name='Classification_page_load_cls'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
