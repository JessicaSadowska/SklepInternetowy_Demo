from django import forms

from Zamówienia.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'is_address_company', 'company_name', 'nip',
                  'street_and_house_nr', 'zipcode', 'city', 'country', 'other_shipping_address',
                  'is_shipping_address_company', 'company_name_shipment', 'nip_shipment', 'street_shipment',
                  'zipcode_shipment', 'city_shipment', 'country_shipment', 'order_note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['first_name'].widget.attrs['required'] = True

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['last_name'].widget.attrs['required'] = True

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['required'] = True

        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = 'Telefon'
        self.fields['phone'].widget.attrs['required'] = True

        self.fields['is_address_company'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_address_company'].widget.attrs['id'] = 'is_address_company'
        self.fields['is_address_company'].widget.attrs['type'] = 'checkbox'

        self.fields['company_name'].widget.attrs['class'] = 'form-control'
        self.fields['company_name'].widget.attrs['placeholder'] = 'Nazwa firmy'

        self.fields['nip'].widget.attrs['class'] = 'form-control'
        self.fields['nip'].widget.attrs['placeholder'] = 'NIP'

        self.fields['street_and_house_nr'].widget.attrs['class'] = 'form-control'
        self.fields['street_and_house_nr'].widget.attrs['placeholder'] = 'Ulica i nr domu'
        self.fields['street_and_house_nr'].widget.attrs['required'] = True

        self.fields['zipcode'].widget.attrs['class'] = 'form-control'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Kod pocztowy'
        self.fields['zipcode'].widget.attrs['required'] = True

        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'Miasto'
        self.fields['city'].widget.attrs['required'] = True

        self.fields['other_shipping_address'].widget.attrs['class'] = 'form-check-input'
        self.fields['other_shipping_address'].widget.attrs['id'] = 'show-shipping-address'
        self.fields['other_shipping_address'].widget.attrs['type'] = 'checkbox'

        self.fields['is_shipping_address_company'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_shipping_address_company'].widget.attrs['id'] = 'is_shipping_address_company'
        self.fields['is_shipping_address_company'].widget.attrs['type'] = 'checkbox'

        self.fields['company_name_shipment'].widget.attrs['class'] = 'form-control'
        self.fields['company_name_shipment'].widget.attrs['placeholder'] = 'Nazwa firmy'
        self.fields['company_name_shipment'].widget.attrs['id'] = 'company_name_shipment'

        self.fields['nip_shipment'].widget.attrs['class'] = 'form-control'
        self.fields['nip_shipment'].widget.attrs['placeholder'] = 'NIP'
        self.fields['nip_shipment'].widget.attrs['id'] = 'nip_shipment'

        self.fields['street_shipment'].widget.attrs['class'] = 'form-control'
        self.fields['street_shipment'].widget.attrs['placeholder'] = 'Ulica i nr domu'
        self.fields['street_shipment'].widget.attrs['id'] = 'street_shipment'

        self.fields['zipcode_shipment'].widget.attrs['class'] = 'form-control'
        self.fields['zipcode_shipment'].widget.attrs['placeholder'] = 'Kod pocztowy'
        self.fields['zipcode_shipment'].widget.attrs['id'] = 'zipcode_shipment'

        self.fields['city_shipment'].widget.attrs['class'] = 'form-control'
        self.fields['city_shipment'].widget.attrs['placeholder'] = 'Miasto'
        self.fields['city_shipment'].widget.attrs['id'] = 'city_shipment'

        # if self.fields['other_shipping_address']:
        #     self.fields['street_shipment'].required = True
        #     self.fields['zipcode_shipment'].required = True
        #     self.fields['city_shipment'].required = True
        # else:
        #     self.fields['street_shipment'].required = False
        #     self.fields['zipcode_shipment'].required = False
        #     self.fields['city_shipment'].required = False

    # def clean(self):
    #     cleaned_data = super(OrderForm, self).clean()
    #
    #     street_shipment = cleaned_data.get('street_shipment')
    #
    #     if street_shipment == 'lala':
    #         raise forms.ValidationError(
    #             'Wprowadzone hasła są różne.'
    #         )
    #
    # def clean(self):
    #     cleaned_data = super(OrderForm, self).clean()
    #     other_shipping_address = cleaned_data.get('other_shipping_address')
    #     street_shipment = cleaned_data.get('street_shipment')
    #     zipcode_shipment = cleaned_data.get('zipcode_shipment')
    #     city_shipment = cleaned_data.get('city_shipment')
    #
    #     if other_shipping_address:
    #         if not street_shipment:
    #             raise forms.ValidationError(
    #                 'Wprowadź poprawny adres wysyłki.'
    #             )
    #         if not zipcode_shipment:
    #             raise forms.ValidationError(
    #                 'Wprowadź poprawny adres wysyłki.'
    #             )
    #         if not city_shipment:
    #             raise forms.ValidationError(
    #                 'Wprowadź poprawny adres wysyłki.'
    #             )
