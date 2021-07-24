from returns import views
from django.conf.urls import url
 
app_name='returns'
urlpatterns = [
    url(r'^sales_return/$', views.sales_return,name='sales_return'),
    url(r'^create_sales_return/$', views.create_sales_return,name='create_sales_return'),
   
    url(r'^create_sales_return2/$', views.create_sales_return2,name='create_sales_return2'),
    url(r'^save_sales_return/$', views.save_sales_return,name='save_sales_return'),
    url(r'^create_sales_return_ajax/$', views.create_sales_return_ajax,name='create_sales_return_ajax'),
    url(r'^create_sales_return_ajax2/$', views.create_sales_return_ajax2,name='create_sales_return_ajax2'),
    url(r'^delete_all_return/$', views.delete_all_return,name='delete_all_return'),
   
    url(r'^returns/delete_sales_return/(?P<id>\d+)$', views.delete_sales_return,name='delete_sales_return'),
   
]