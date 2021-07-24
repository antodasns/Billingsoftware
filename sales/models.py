
from django.db import models
import datetime

from datetime import date
from django.utils import timezone
 
 

# Create your models here.
sale_type = (
            ('retail','retail'),
            ('wholesale','wholesale'),
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
 

class create_sales_table(models.Model):
	sales_product_ref_id=models.IntegerField()
	
	sales_invoice_no=models.IntegerField()
	sales_qty=models.IntegerField()

class create_sales_final(models.Model):
	sale_type=models.CharField(choices=sale_type,max_length=10)
	sales_date=models.DateField(null=True)
	sales_time=models.TimeField(null=True)
	subtotal=models.CharField(max_length=50)
	sale_invoice_ref=models.IntegerField()
	sales_special_discount=models.IntegerField()
	sales_total=models.CharField(max_length=50)
	sales_payment_received=models.IntegerField()
	sales_total_tax_amount=models.CharField(max_length=50)
	sales_total_discount_amount=models.IntegerField()
	sales_round_off=models.IntegerField()
	sales_transaction_mode=models.CharField(choices=transaction_mode,max_length=5)
	sales_cash_account=models.CharField(choices=cash_account,max_length=8)
	sales_payment_remainder_date=models.DateField(null=True)
	sales_payment_balance=models.CharField(max_length=50)
	sale_return_status=models.CharField(max_length=5)
	sales_taxable_amount=models.CharField(max_length=50)
	sales_printing=models.TextField()

class sale_totals(models.Model):
	sales_date=models.DateField(null=True)
	sales_totals=models.CharField(max_length=50)


class taxes(models.Model):
	tax_percent=models.IntegerField()
	sale_date=models.DateField(null=True)
	total_tax_amount=models.CharField(max_length=50)
	price_tax_amount=models.CharField(max_length=50)
	

class create_wholesale_sales_table(models.Model):
	sales_product_ref_id=models.IntegerField()
	
	sales_invoice_no=models.IntegerField()
	sales_qty=models.IntegerField()

class create_wholesale_sales_final(models.Model):
	sale_type=models.CharField(choices=sale_type,max_length=10)
	sales_date=models.DateField(null=True)
	sales_time=models.TimeField(null=True)
	subtotal=models.CharField(max_length=50)
	sale_invoice_ref=models.IntegerField()
	sales_special_discount=models.IntegerField()
	sales_total=models.CharField(max_length=50)
	sales_payment_received=models.IntegerField()
	sales_total_tax_amount=models.CharField(max_length=50)
	sales_total_discount_amount=models.IntegerField()
	sales_round_off=models.IntegerField()
	sales_transaction_mode=models.CharField(choices=transaction_mode,max_length=5)
	sales_cash_account=models.CharField(choices=cash_account,max_length=8)
	sales_payment_remainder_date=models.DateField(null=True)
	sales_payment_balance=models.CharField(max_length=50)
	sales_taxable_amount=models.CharField(max_length=50)
	sales_printing=models.TextField()
	
class sale_wholesale_totals(models.Model):
	sales_date=models.DateField(null=True)
	sales_totals=models.CharField(max_length=50)


class wholesale_taxes(models.Model):
	tax_percent=models.IntegerField()
	sale_date=models.DateField(null=True)
	total_tax_amount=models.CharField(max_length=50)
	price_tax_amount=models.CharField(max_length=50)


class reports(models.Model):
	prod_name=models.CharField(max_length=50)
	qty=models.CharField(max_length=50)
	unit=models.CharField(max_length=50)
	price=models.CharField(max_length=50)
	discount=models.CharField(max_length=50)
	taxable_amount=models.CharField(max_length=50)
	tax_percent=models.CharField(max_length=50)
	cgst=models.CharField(max_length=50)
	sgst=models.CharField(max_length=50)
	invoice_no=models.IntegerField()
