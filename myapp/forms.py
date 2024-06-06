from django import forms

class UploadFileForm(forms.Form):
    usuario = forms.CharField(
        label='Usuario', max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    fecha = forms.DateField(
        label='Fecha', 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    laboratorio = forms.CharField(
        label='Laboratorio', max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del laboratorio'})
    )
    cuit = forms.CharField(
        label='CUIT', max_length=11, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CUIT'})
    )
    file = forms.FileField(
        label='Seleccionar archivo', 
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
