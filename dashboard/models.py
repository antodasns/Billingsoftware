from django.db import models

# Create your models here.
class notification(models.Model):
	product_stock=models.CharField(max_length=50)
	product_low_stock_limit=models.CharField(max_length=50,blank=True)
	product_name=models.CharField(max_length=50)
	