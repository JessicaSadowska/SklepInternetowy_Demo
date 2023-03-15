from django import forms
from .models import Uzytkownik, Adres


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    newsletter = forms.CheckboxInput()

    class Meta:
        model = Uzytkownik
        fields = ['email', 'name', 'password', 'newsletter']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['newsletter'].widget.attrs['type'] = 'checkbox'
        self.fields['newsletter'].widget.attrs['class'] = 'form-check-input'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Wprowadzone hasła są różne.'
            )
        if len(password) < 8:
            raise forms.ValidationError(
                'Hasło jest za krótkie.'
            )


class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = Uzytkownik
        fields = ['name', 'last_name', 'phone']

    def __init__(self, *args, **kwargs):
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = ['company_name', 'nip', 'street_and_house_nr', 'zipcode', 'city']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs['class'] = 'form-control'
        self.fields['nip'].widget.attrs['class'] = 'form-control'
        self.fields['street_and_house_nr'].widget.attrs['class'] = 'form-control'
        self.fields['zipcode'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
