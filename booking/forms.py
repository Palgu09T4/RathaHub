from django import forms
from .models import Book
from driver.models import Driver

class BookForm(forms.ModelForm):
    startDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Start Date & Time",
        input_formats=['%Y-%m-%dT%H:%M']
    )
    endDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="End Date & Time",
        input_formats=['%Y-%m-%dT%H:%M']
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super(BookForm, self).__init__(*args, **kwargs)

        # Add driver field only if user is superuser
        if user and user.is_superuser:
            self.fields['driver'] = forms.ModelChoiceField(
                queryset=Driver.objects.filter(status="NB"),
                required=False,
                label="Select Driver (admin only)"
            )

    class Meta:
        model = Book
        fields = (
            'source', 'destination', 'startDate', 'endDate',
            'securityDeposit', 'discountId', 'vehicle'
            # driver field will be added conditionally
        )
