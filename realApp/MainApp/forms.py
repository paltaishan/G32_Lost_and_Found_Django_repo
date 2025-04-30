from django import forms
from .models import Item, ClaimRequest

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image', 'category', 'location', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['message', 'contact_info']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
