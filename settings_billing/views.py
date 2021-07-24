from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from dashboard.views import error_page
from settings_billing.models import store_details
from settings_billing.forms import create_setting
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
@login_required(login_url='/login')

def create_settings(request):
	
	if request.FILES.get('photos')==None:
		if request.method == 'POST':
			store_info=store_details.objects.latest('id')
			store_update=store_details.objects.get(pk=store_info.id)
			store_update.store_name=request.POST['name']
			store_update.store_code=request.POST['code']
			store_update.store_adress=request.POST['address']
			store_update.store_state=request.POST['states']
			store_update.store_email=request.POST['mail']
			store_update.store_phone=request.POST['phoneno']
			store_update.store_gst=request.POST['gstno']
			store_update.store_website=request.POST['site']
			store_update.cess_status=request.POST['cess_stat']
			store_update.save()
			
			return HttpResponseRedirect('/create_settings/')
		
	else:
		if request.method == 'POST' and request.FILES['photos']:
			
				
			store_info=store_details.objects.latest('id')
			store_update=store_details.objects.get(pk=store_info.id)
			store_update.store_name=request.POST['name']
			store_update.store_code=request.POST['code']
			store_update.store_adress=request.POST['address']
			store_update.store_state=request.POST['states']
			store_update.store_email=request.POST['mail']
			store_update.store_phone=request.POST['phoneno']
			store_update.store_gst=request.POST['gstno']
			store_update.store_website=request.POST['site']
			store_update.cess_status=request.POST['cess_stat']
			store_update.store_logo=request.FILES['photos']
			store_update.save()

			return HttpResponseRedirect('/create_settings/')

	store_info=store_details.objects.latest('id')
	forms=create_setting()
	active_sidebar7=1
	return render(request,'settings_billing/create_settings.html',{'forms':forms,'active_sidebar7':active_sidebar7,'store_info':store_info})
