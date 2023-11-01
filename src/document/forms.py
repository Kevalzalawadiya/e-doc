from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DocumentShared

class DocumentShareForm(forms.ModelForm):
    shared_doc_view = forms.BooleanField(label="View:",required=False)
    shared_doc_update = forms.BooleanField(label="Update:",required=False)
    shared_doc_download = forms.BooleanField(label="Download:",required=False)
    class Meta:
        model = DocumentShared
        fields = ['shared_user', 'shared_doc_view', 'shared_doc_update', 'shared_doc_download']

# class DocumentSharedForm(forms.ModelForm):
#     shared_doc_view = forms.BooleanField(label="View       :",required=False)
#     shared_doc_update = forms.BooleanField(label="Update       :",required=False)
#     shared_doc_download = forms.BooleanField(label="Download       :",required=False)

#     class Meta:
#         model = DocumentShared
#         fields = [
#             'shared_user',
#             'document',
#             'receiver',
#             'shared_doc_view',
#             'shared_doc_update',
#             'shared_doc_download',
#         ]
#         widgets = {
#             'shared_user': forms.Select(attrs={'class': 'form-control'}),
#             'shared_doc_view': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'shared_doc_update': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'shared_doc_download': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }