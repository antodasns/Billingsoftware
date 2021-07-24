from django.db import models
import datetime
from datetime import datetime
from datetime import date


class store_details(models.Model):
	store_name=models.CharField(max_length=50)
	store_phone=models.CharField(max_length=15)
	store_gst=models.CharField(max_length=50)
	store_code=models.CharField(max_length=10)
	store_website=models.CharField(max_length=50)
	store_email=models.CharField(max_length=50)
	store_adress=models.CharField(max_length=200)
	store_state=models.CharField(max_length=50)
	cess_status=models.CharField(max_length=5)
	store_logo= models.ImageField(upload_to = 'logo')
