from django import forms
from .models import Debtor


class DebtorUpdateForm(forms.ModelForm):
    class Meta():
        model = Debtor
        fields = ['name', 'amount_owed', 'email', 'is_paid', 'due_date', 'last_email_sent', 'created_by']
