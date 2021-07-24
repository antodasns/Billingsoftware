from settings_billing import views
from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *
app_name='settings_billing'
urlpatterns = [
    url(r'^create_settings/$', views.create_settings,name='create_settings'),

    ]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT)  