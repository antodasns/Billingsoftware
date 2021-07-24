from django import forms
import datetime
from datetime import time,date
sale_type=(
	('1','Retail'),
('2','Whole_sale'),
	)
transaction_mode=(
	('Cash','Cash'),


	) 
cash_account=(
	('General','General'),
)



class create_sale(forms.Form):
	sale_type=forms.ChoiceField(choices=sale_type,widget=forms.Select(attrs={'class':'form-control','id':'sale_type_id','name':'sale_type'}))
	sale_date=forms.DateTimeField(widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':'startDate'}))
	# sale_time=forms.DateTimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time','id':'startTime','step':"1"}))
	sale_sub_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_subtotal",'readonly':"readonly","type":"hidden"}))
	sale_tax_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_taxtotal",'readonly':"readonly","type":"hidden"}))
	sale_discount_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_disctotal",'readonly':"readonly","type":"hidden"}))
	# qtysale_sub_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"qtyfinal_subtotal",'readonly':"readonly","type":"hidden"}))
	edit_tot=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"edit_tot",'readonly':"readonly","type":"hidden"}))
	sp_discount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"sp_discount",'readonly':"readonly","type":"hidden"}))

	
	sale_special_discount=forms.CharField(required=True,widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"special_discount_id",'onclick':"this.select();",'required':'required'}))
	sale_total=forms.CharField(required=True,widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"sale_tot","step":"0.01",'required':'required','readonly':"readonly"}))
	sale_payment_received=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	sale_total_tax_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"total_tax_id",'readonly':"readonly"}))
	sale_total_discount_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"total_discount_id",'readonly':"readonly"}))
	sale_round_off=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	sale_transaction_mode=forms.ChoiceField(choices=transaction_mode,widget=forms.Select(attrs={'class':'form-control',}))
	sale_cash_account=forms.ChoiceField(choices=cash_account,widget=forms.Select(attrs={'class':'form-control',}))
	cust_sale_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"cust_sale_total","step":"0.01","type":"hidden"}))
	# cust_deb=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"cus_deb","type":"hidden","step":"0.01"}))
	# cust_cre=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"cus_cre","type":"hidden","step":"0.01"}))
	# sale_payment_remainder_date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':"remDate"})) 


class create_estimates(forms.Form):
	estimate_type=forms.ChoiceField(choices=sale_type,widget=forms.Select(attrs={'class':'form-control','id':'sale_type_id'}))
	estimate_date=forms.DateTimeField(widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':'startDate'}))
	# sale_time=forms.DateTimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time','id':'startTime','step':"1"}))
	estimate_sub_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_subtotal",'readonly':"readonly","type":"hidden"}))
	estimate_tax_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_taxtotal",'readonly':"readonly","type":"hidden"}))
	estimate_discount_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"final_disctotal",'readonly':"readonly","type":"hidden"}))
	# qtysale_sub_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"qtyfinal_subtotal",'readonly':"readonly","type":"hidden"}))
	edit_tot=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"edit_tot",'readonly':"readonly","type":"hidden"}))
	sp_discount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"sp_discount",'readonly':"readonly","type":"hidden"}))

	estimate_credit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	estimate_debit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	estimate_special_discount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"special_discount_id",'onclick':"this.select();" }))
	estimate_total=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"sale_tot","step":"0.01"}))
	estimate_payment_received=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	estimate_total_tax_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0","step":"0.01",'id':"total_tax_id"}))
	estimate_total_discount_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"total_discount_id"}))
	estimate_round_off=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	estimate_transaction_mode=forms.ChoiceField(choices=transaction_mode,widget=forms.Select(attrs={'class':'form-control',}))
	estimate_cash_account=forms.ChoiceField(choices=cash_account,widget=forms.Select(attrs={'class':'form-control',}))