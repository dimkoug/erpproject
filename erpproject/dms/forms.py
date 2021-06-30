from django import forms

from core.forms import BootstrapForm

from .models import Folder


class FolderForm(BootstrapForm, forms.ModelForm):
    media = forms.FileField(widget=forms.ClearableFileInput(
                            attrs={'multiple': True}), required=False)

    class Meta:
        model = Folder
        fields = ('name', 'parent')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
