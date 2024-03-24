from django import forms
from .models import *

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = '__all__'
        
class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['assigned_to', 'created_by',]
