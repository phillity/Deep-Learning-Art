from django import forms

class ImageUploadForm(forms.Form):
    file = forms.ImageField(widget=forms.FileInput(attrs={'accept':'.jpg,.jpeg,.png'}))
