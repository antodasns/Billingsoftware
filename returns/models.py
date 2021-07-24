from django.db import models
import datetime
from datetime import datetime
from datetime import date 
# Create your models here. 
class sales_returned(models.Model):
	
	sale_amount_return=models.CharField(max_length=50)
	sale_return_date=models.DateField(default=datetime.now(), blank=True)
	sale_return_transaction_mode=models.CharField(max_length=50)
	sale_return_cash_account=models.CharField(max_length=50)
	sales_returned_invoice=models.IntegerField()
	sales_invoice_ref=models.IntegerField()
	class Meta:
		verbose_name_plural="sales_returned"
	def __str__(self):
		return str(self.id)

class returned_sales_prod(models.Model):
	sales_product_id=models.IntegerField()
	sales_returned_invoice_id_ref=models.IntegerField()


