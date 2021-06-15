from django import forms

class MitgliedForm(forms.Form):
    vorname = forms.CharField(required=True)
    name = forms.CharField(required=True, label='nachname')
    spitzname = forms.CharField(required=False)
    strasse = forms.CharField(required=False)
    hausnr = forms.CharField(required=False)
    plz = forms.CharField(required=False)
    ort = forms.CharField(required=False)
    tel_mobil = forms.CharField(required=False)