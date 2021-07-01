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


class FilesForm(BootstrapForm, forms.Form):
    media = forms.FileField(widget=forms.ClearableFileInput(
                            attrs={'multiple': True}), required=False)
    folder = forms.ModelChoiceField(label='Folder',
                                    queryset=Folder.objects.all(),
                                    required=True)

    def __init__(self, request, folder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(
            user=request.user)
        self.fields['folder'].initial = folder
