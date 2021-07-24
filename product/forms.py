from django import forms
from product.models import products,categorisation

from django.core.validators import FileExtensionValidator

def category():
	cats=[]
	catx=products.objects.values_list('category_ref',flat=True)
	for x in catx:
		cats.append ((x,x))
	y=tuple(cats)
	return y

def brand():
	brats=[]
	bratx=products.objects.values_list('brand_ref',flat=True)
	for x in bratx:
		brats.append ((x,x))
	y=tuple(brats)
	return y

# def unit_type():
# 	cats=[]
# 	catx=products.objects.values_list('unit_type_ref',flat=True)
# 	for x in catx:
# 		cats.append ((x,x))
# 	y=tuple(cats)
# 	return y
def alter_unit():
	cats=[]
	catx=categorisation.objects.values_list('product_unit_type',flat=True)
	for x in catx:
		cats.append ((x,x))
	y=tuple(cats)
	return y

def vendor_name():
	cats=[]
	catx=vendor.objects.values_list('vendor_name',flat=True)
	for x in catx:
		cats.append ((x,x))
	y=tuple(cats)
	return y


unit_type=(
('Admin','Admin'),
('Doctor','Doctor'),
)

tax_categorory=(
('0','No GST Rate'),
('1','5% GST Rate'),
('2','12% GST Rate'),
('3','18% GST Rate'),
('4','28% GST Rate'),
)
tax_status=(
('Admin','Admin'),
('Doctor','Doctor'),
)

purchase_product=(
('Admin','Admin'),
('Doctor','Doctor'),
)
purchase_unit=[
['Admin','Admin'],
['Doctor','Doctor'],
]
purchase_vendor=(
('Admin','Admin'),
('Doctor','Doctor'),
)
purchase_transaction_mode=(
            ('Cash','Cash'),
            ('Bank','Bank')
            )
purchase_cash_account=(
            ('General','General'),
            ('General','General'),
            ('General','General')
            )
invoice_type=(
	('General','General'),
('Vendor','Vendor'),
	)
invoice_create_product=(
	('Admin','Admin'),
('Doctor','Doctor'),
	)
asset=(
	('Admin','Admin'),
('Doctor','Doctor'),
	)
purchase_qty=(
	('Admin','Admin'),
('Doctor','Doctor'),
	)
purchase_vendor=(
	('Admin','Admin'),
('Doctor','Doctor'),
	)
transaction_mode=(
	('Admin','Admin'),
('Doctor','Doctor'),
	)

invoice_create_unit=(
	('Admin','Admin'),
('Doctor','Doctor'),
	)
barcode_product=(
	('Admin','Admin'), 
('Doctor','Doctor'),
	)

class create_product(forms.Form):
	# product_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	# product_code=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'placeholder':'Code ...'}))
	# product_hsn=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'placeholder':'HSN ...'}))
	product_stock=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"stock_idd"}))
	product_low_stocklimit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"low_stock_idd"}))
	# product_cost=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"cost_id"}))
	# product_price=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"mrp_id"}))
	# product_wholesale_price=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",
	# 	'id':"wholesale_id"}))
	# product_tax_included=forms.CharField(widget=forms.CheckboxInput(attrs={'id':'checkbox_123'}),required=False)
	# product_expiration=forms.CharField(widget=forms.CheckboxInput(attrs={'id':'checkbox_234'}),required=False)
	
	# product_discount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"discount_id"}))
	# product_alter_cost=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	# product_alter_price=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))


class create_purchases(forms.Form):
	purchase_time=forms.DateField(widget=forms.DateTimeInput(attrs={'class':'form-control','id':'startDate','type':'date'}))
	purchase_invoice_id=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	purchase_transaction_mode=forms.ChoiceField(choices=purchase_transaction_mode,widget=forms.Select(attrs={'class':'form-control',}))
	purchase_cash_account=forms.ChoiceField(choices=purchase_cash_account,widget=forms.Select(attrs={'class':'form-control',}))
	purchase_payment_subtotal=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"fin_tot",'readonly':"readonly"}))
	purchase_payment_special_discount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"sp_discount_id","onclick":"this.select()"}))
	purchase_credit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input",'readonly':"readonly"}))
	purchase_debit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input",'readonly':"readonly"}))
	purchase_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"totals_id",'readonly':"readonly"}))
	purchase_paid_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"paid_amount_id","onclick":"this.select()"}))
	purchase_balance=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"balance_id",'readonly':"readonly"}))
	fin_tot=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_subtotal",'readonly':"readonly","type":"hidden"}))

class create_purchase_invoices(forms.Form):
	purchase_invoice_invoice_type=forms.ChoiceField(choices=invoice_type,widget=forms.Select(attrs={'class':'form-control',}))
	purchase_invoice_time=forms.DateField(widget=forms.DateTimeInput(attrs={'class':'form-control','id':'example-date-input','type':'date'}))
	


class create_asset_purchases(forms.Form):
	
	purchase_time=forms.DateField(widget=forms.DateTimeInput(attrs={'class':'form-control','id':'startDate','type':'date'}))
	purchase_invoice_id=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	purchase_transaction_mode=forms.ChoiceField(choices=purchase_transaction_mode,widget=forms.Select(attrs={'class':'form-control',}))
	purchase_cash_account=forms.ChoiceField(choices=purchase_cash_account,widget=forms.Select(attrs={'class':'form-control',}))
	purchase_payment_subtotal=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"final_subtotal",'readonly':"readonly"}))
	purchase_payment_special_discount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"sp_discount_id","onclick":"this.select()"}))
	purchase_credit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input",'readonly':"readonly"}))
	purchase_debit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input",'readonly':"readonly"}))
	purchase_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"totals_id",'readonly':"readonly"}))
	purchase_paid_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"paid_amount_id","onclick":"this.select()"}))
	purchase_balance=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"balance_id",'readonly':"readonly"}))
	fin_tot=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"fin_tot",'readonly':"readonly","type":"hidden"}))

class create_asset_invoices(forms.Form):
	purchase_invoice_invoice_type=forms.ChoiceField(choices=invoice_type,widget=forms.Select(attrs={'class':'form-control',}))
	purchase_invoice_time=forms.DateField(widget=forms.DateTimeInput(attrs={'class':'form-control','id':'example-date-input','type':'date'}))
class create_barcodes(forms.Form):
	barcode_product=forms.ChoiceField(choices=barcode_product,widget=forms.Select(attrs={'class':'form-control',}))
	barcode_unit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))

class uploading_products(forms.Form):
	excel_file = forms.FileField()
