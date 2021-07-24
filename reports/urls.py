from reports import views
from django.conf.urls import url

app_name='reports'
urlpatterns = [
    url(r'^create_sales_reports/$', views.create_sales_reports,name='create_sales_reports'),
    url(r'^create_monthly_reports/$', views.create_monthly_reports,name='create_monthly_reports'),
    url(r'^view_sales_reports/$', views.view_sales_reports,name='view_sales_reports'),
    url(r'^create_gst_reports/$', views.create_gst_reports,name='create_gst_reports'),
    url(r'^view_monthly_sales_reports/$', views.view_monthly_sales_reports,name='view_monthly_sales_reports'),
]