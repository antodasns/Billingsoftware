from django.db import models
import datetime
from datetime import datetime
from datetime import date
from django.utils import timezone
 

category_type= (
            ('Cash','Cash'),
            ('Bank','Bank')
            )
# Create your models here.
class create_sales_report_table(models.Model):
	create_sales_report_month_and_year=models.DateTimeField(default=datetime.now(),blank=True)
	create_sales_report_category=models.CharField(choices=category_type,max_length=10)






class create_Gst_report_table(models.Model):
	create_gst_report_month_and_year=models.DateTimeField(default=datetime.now(),blank=True)
	create_gst_report_category=models.CharField(choices=category_type,max_length=10)