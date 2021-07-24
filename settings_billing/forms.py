from django import forms
state=(
	('Kerala','Kerala'),
	('TamilNadu','TamilNadu'),
	('AndraPradesh','AndraPradesh'),
	('Gujarath','Gujarath'),
	('UP','UP')
	)
class create_setting(forms.Form):
	name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	code=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...',"minlength":"2","maxlength":'4','value':"PN"}))
	states=forms.ChoiceField(choices=state,widget=forms.Select(attrs={'class':'form-control',}))
	mail=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'E-mail.'}))
	phoneno=forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control','maxlength': '10','id':"example-number-input",'placeholder':'Enter ...'}))
	gstno=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	site=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter ...'}))
	photos=forms.FileField()