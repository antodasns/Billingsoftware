from django import forms
sale=(
	('sales','sales'),

	)
transaction_mode=(
	('Cash','Cash'),


	)
cash_account=(
	('General','General'),

)



class create_sales_returns(forms.Form):

	return_credit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	return_debit=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	return_returnable_amount=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"returnable"}))
	return_amount_retuned=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	return_time=forms.DateField (widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':'example-date-input'}))
	return_transaction_mode=forms.ChoiceField(choices=transaction_mode,widget=forms.Select(attrs={'class':'form-control',}))
	return_cash_account=forms.ChoiceField(choices=cash_account,widget=forms.Select(attrs={'class':'form-control',}))
	return_fin=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"final_wla"}))


class create_damaged_products(forms.Form):
	damaged_products_time=forms.DateField (widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':'example-date-input'}))


class create_product_returns(forms.Form):
	
	product_returns_time=forms.DateField (widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':'example-date-input'}))
	product_returns_subtotal=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	product_returns_amount_returned=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','value':"0",'id':"example-number-input"}))
	product_returns_transaction_mode=forms.ChoiceField(choices=transaction_mode,widget=forms.Select(attrs={'class':'form-control',}))
	product_returns_cash_account=forms.ChoiceField(choices=cash_account,widget=forms.Select(attrs={'class':'form-control',}))
