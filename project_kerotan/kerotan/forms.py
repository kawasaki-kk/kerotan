from django import forms

class AddressForm(forms.Form):
	start_address = forms.CharField(min_length=2, max_length=100, label='start_address')
	arriv_address = forms.CharField(min_length=2, max_length=100, label='arriv_address')

	# latitude = forms.FloatField(label='latitude')
	# longitude = forms.FloatField(label='longitude')
	# keyword = forms.CharField(min_length=2, max_length=100, label='keyword')
	# date = forms.DateField(required=False)