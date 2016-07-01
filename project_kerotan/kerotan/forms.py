from django import forms

class AdressForm(forms.Form):
	adress = forms.CharField(min_length=2, max_length=100, label='adress')

	# latitude = forms.FloatField(label='latitude')
	# longitude = forms.FloatField(label='longitude')
	# keyword = forms.CharField(min_length=2, max_length=100, label='keyword')
	# date = forms.DateField(required=False)