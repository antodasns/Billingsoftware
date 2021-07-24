from django.db import models
import datetime
from datetime import datetime
from datetime import date
from django.utils import timezone
# Create your models here. 
 
product_tax_category = (
            ('Admin','Admin'),
            ('Doctor','Doctor'),
            ('Laboratory','Laboratory'),
            ('Patient','Patient'),
            )

transaction_mode = (
            ('Cash','Cash'),
            ('Bank','Bank') 
            )
cash_account = (
            ('General','General'),
            ('General','General'),
            ('General','General')
            )

class categorisation(models.Model):
	product_category=models.CharField(max_length=50)
	product_brand=models.CharField(max_length=50,blank=True)
	product_unit_type=models.CharField(max_length=50)
	product_default_unit=models.CharField(max_length=50)
	product_default_unit_prefix=models.CharField(max_length=50)
	class Meta:
		verbose_name_plural="categorisation"
	def __str__(self):
		return str(self.id)


class alternate_units(models.Model):
	unit_ref_id=models.CharField(max_length=50)
	product_alternate_unit=models.CharField(max_length=50)
	product_alternate_code=models.CharField(max_length=10)
	product_alternate_unit_prifix=models.CharField(max_length=10)

	class Meta:
		verbose_name_plural="alternate_units"
	def __str__(self):
		return str(self.id) 

class alternate_cost_price(models.Model):
	product_ref_id=models.IntegerField()
	unit_type_id=models.IntegerField()
	product_price=models.CharField(max_length=50)
	product_cost=models.IntegerField()
	taxable_price=models.CharField(max_length=50)
	price_without_tax=models.CharField(max_length=50)
	class Meta:
		verbose_name_plural="alternate_cost_price"
	def __str__(self):
		return str(self.id) 

class products(models.Model):
	product_name=models.CharField(max_length=50)
	product_code=models.CharField(max_length=20)
	product_integer_code=models.IntegerField()
	product_hsn=models.IntegerField(null=True)
	category_ref=models.CharField(max_length=50,null=True)
	sub_category=models.CharField(max_length=50,null=True)
	brand_ref=models.CharField(max_length=50,null=True)
	unit_type_ref=models.CharField(max_length=50)
	product_stock=models.CharField(max_length=50)
	product_low_stock_limit=models.IntegerField()
	product_cost=models.IntegerField()
	product_price=models.CharField(max_length=50)
	product_wholesale_price=models.IntegerField(null=True)
	product_tax_category=models.IntegerField(null=True)
	product_tax_amount=models.CharField(max_length=50)
	wholesale_product_tax_amount=models.CharField(max_length=50)
	product_discount=models.IntegerField()
	alternate_unit_ref=models.CharField(max_length=50,null=True)
	product_tax_satus=models.CharField(max_length=10,null=True)
	product_alternate_cost=models.CharField(max_length=10,null=True)
	product_alternate_price=models.CharField(max_length=10,null=True)
	price_tax=models.CharField(max_length=50)
	final_price=models.CharField(max_length=50)
	final_wholesale_price=models.CharField(max_length=50)
	taxable_price=models.CharField(max_length=50)
	wholesale_taxable_price=models.CharField(max_length=50)
	wholesaleprice_without_tax=models.CharField(max_length=50)
	class Meta:
		verbose_name_plural="products"
	def __str__(self):
		return str(self.product_name)


class sub_products(models.Model):
	product_name=models.CharField(max_length=50)
	product_code=models.CharField(max_length=20)
	product_integer_code=models.IntegerField()
	product_hsn=models.IntegerField(null=True)
	category_ref=models.CharField(max_length=50,null=True)
	sub_category=models.CharField(max_length=50,null=True)
	brand_ref=models.CharField(max_length=50,null=True)
	unit_type_ref=models.CharField(max_length=50)
	product_stock=models.CharField(max_length=50)
	product_low_stock_limit=models.IntegerField()
	product_cost=models.IntegerField()
	product_price=models.CharField(max_length=50)
	product_wholesale_price=models.IntegerField(null=True)
	product_tax_category=models.IntegerField(null=True)
	product_tax_amount=models.CharField(max_length=50)
	wholesale_product_tax_amount=models.CharField(max_length=50)
	product_discount=models.IntegerField()
	alternate_unit_ref=models.CharField(max_length=50,null=True)
	product_tax_satus=models.CharField(max_length=10,null=True)
	product_alternate_cost=models.CharField(max_length=10,null=True)
	product_alternate_price=models.CharField(max_length=10,null=True)
	price_tax=models.CharField(max_length=50)
	final_price=models.CharField(max_length=50)
	final_wholesale_price=models.CharField(max_length=50)
	taxable_price=models.CharField(max_length=50)
	wholesale_taxable_price=models.CharField(max_length=50)
	wholesaleprice_without_tax=models.CharField(max_length=50)

 