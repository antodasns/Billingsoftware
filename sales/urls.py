from sales import views
from django.conf.urls import url

app_name='sales'
urlpatterns = [
    url(r'^sales/$', views.sales_details,name='sales_details'),
    url(r'^sales_wholesale/$', views.sales_details_wholesale,name='sales_details_wholesale'),
    url(r'^dashboard_sales/$', views.dashboard_sales,name='dashboard_sales'),
   
    url(r'^stock_movement/$', views.stock_movement,name='stock_movement'),
    url(r'^create_sales/$', views.create_sales,name='create_sales'),
    url(r'^creating_sales/$', views.creating_sales,name='creating_sales'),
   
    url(r'^create_sales_ajax/$', views.create_sales_ajax,name='create_sales_ajax'),
    url(r'^sales/print_sales/(?P<id>\d+)$', views.print_sales,name='print_sales'),
    url(r'^sales/print_sales_wholesale/(?P<id>\d+)$', views.print_sales_wholesale,name='print_sales'),
    url(r'^sales/view_sales/(?P<id>\d+)$', views.view_sales,name='view_sales'),
   
    url(r'^sales/edit_sales/(?P<id>\d+)$', views.edit_sales,name='edit_sales'),
    url(r'^sales/update_sales/(?P<id>\d+)$', views.update_sales,name='update_sales'),
    url(r'^sales/delete_sales/(?P<id>\d+)$', views.delete_sales,name='delete_sales'),
    url(r'^sales/delete_all_sales/$', views.delete_all_sales,name='delete_all_sales'),
    url(r'^sales/delete_wholesale_sales/(?P<id>\d+)$', views.delete_wholesale_sales,name='delete_wholesale_sales'),
    url(r'^sales/delete_all_wholesale_sales/$', views.delete_all_wholesale_sales,name='delete_all_wholesale_sales'),
    url(r'^sales_dashboard_ajax/$', views.sales_dashboard_ajax,name='sales_dashboard_ajax'),
    
]