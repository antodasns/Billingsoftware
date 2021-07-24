from django import forms
month=(
	('1','January'),
	('2','February'),
	('3','March'),
	('4','April'),
	('5','May'),
	('6','June'),
	('7','July'),
	('8','August'),
	('9','September'),
	('10','October'),
	('11','November'),
	('12','December')
	)
category=(
	('all','all'),
	('b2b','B TO B'),
	('b2c','B TO C'),
	)



class create_sales_report(forms.Form):
	# create_sales_report_month=forms.ChoiceField(choices=month,widget=forms.Select(attrs={'class':'form-control',}))
	create_sales_report_year=forms.CharField (widget=forms.NumberInput(attrs={'class':'form-control','type':'number'}))
	create_sales_report_category=forms.ChoiceField(choices=category,widget=forms.Select(attrs={'class':'form-control',}))



class create_gst_report(forms.Form):
	create_gst_report_month_and_year=forms.DateField (widget=forms.DateInput(attrs={'class':'form-control','type':'date','id':'example-date-input'}))
	create_gst_report_category=forms.ChoiceField(choices=category,widget=forms.Select(attrs={'class':'form-control',}))
