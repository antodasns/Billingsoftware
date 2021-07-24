from product import views
from django.conf.urls import url

app_name='product'
urlpatterns = [
    url(r'^product_details/$', views.product_details,name='product_details'),   
    url(r'^create_barcode/$', views.create_barcode,name='create_barcode'),
    url(r'^create_barcode_id/(?P<id>\d+)$', views.create_barcode_id,name='create_barcode_id'),
    url(r'^barcode_generator/$', views.barcode_generator,name='barcode_generator'),
    url(r'^product_upload/$', views.product_upload,name='product_upload'),
    url(r'^create_products/$', views.create_products,name='create_products'),
    # url(r'^create_update_products/$', views.create_update_products,name='create_update_products'),
    url(r'^create_product_ajax/$', views.create_product_ajax,name='create_product_ajax'),
    url(r'^generate_code_ajax/$', views.generate_code_ajax,name='generate_code_ajax'),
    url(r'^update_product_ajax/$', views.update_product_ajax,name='update_product_ajax'),
    url(r'^product/edit_products/(?P<id>\d+)$',views.edit_products,name='edit_products'),
    url(r'^product/update_products/$',views.update_products,name='update_products'),
    url(r'^update_stock/$', views.update_stock,name='update_stock'),
    url(r'^del_products/(?P<id>\d+)$',views.del_products,name='del_products'),
    url(r'^delete_all_product/', views.delete_all_product,name='delete_all_product'),
]