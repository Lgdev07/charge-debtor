from django import forms
from .models import Debtor


class DebtorUpdateForm(forms.ModelForm):
    disabled_fields = ['last_email_sent', 'created_by']

    class Meta():
        model = Debtor
        fields = ['name', 'amount_owed', 'email', 'is_paid', 'due_date', 'last_email_sent', 'created_by', 'image']

    def __init__(self, *args, **kwargs):
        """Method Inherits from Original
        to make fields disabled
        """     
        super(DebtorUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.disabled_fields:
                self.fields[field].disabled = True

