
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from driver.models import Driver  # Import to validate driver email

ROLE_CHOICES = (
    ('customer', 'Customer'),
    ('driver', 'Driver'),
)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'role'
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')

        # Validate if email is present in Driver table if role is driver
        if role == 'driver':
            if not Driver.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "You are not authorized to register as a driver. Please contact the admin."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            from .models import UserProfile
            role = self.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
        return user

class editForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def save(self, commit=True):
        user = super(editForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
