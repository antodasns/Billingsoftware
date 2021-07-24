from dashboard import views
from django.conf.urls import url
from django.urls import path
app_name='dashboard'
urlpatterns = [
	path('layout', views.layout,name='layout'), 
	path('indexs', views.indexing,name='indexs'),
	path('', views.indexing,name='indexs'),
	path('logout', views.user_logout,name='logout'),
	path('layout', views.layout,name='layout'),
	path('error_page', views.error_page,name='error_page'),
	url(r'^create_table_ajax/$', views.create_table_ajax,name='create_table_ajax'),
	url(r'^create_table_ajaxing/$', views.create_table_ajaxing,name='create_table_ajaxing'),
	url(r'^login/$', views.user_login,name='login'),
	url(r'^searching_product/$', views.searching_product,name='searching_product'),
	url(r'^clearall_ajax/$', views.clearall_ajax,name='clearall_ajax'),
]