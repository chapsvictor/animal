from django import forms
from django.core.exceptions import ValidationError
from location.models import State, LocalGovernmentArea
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128)

    '''to check if second password"confirm password" matches with the password passed in'''

    def clean(self):
        cd = self.cleaned_data

        if self._errors:
            return cd

        cd['password'] = cd['password'].strip()
        cd['confirm_password'] = cd['confirm_password'].strip()

        if not cd['password']:
            raise ValidationError("Passwords Can't Be Blank")

        if not cd['confirm_password']:
            raise ValidationError("Passwords Can't Be Blank")

        if cd['password'] != cd['confirm_password']:
            raise ValidationError("Passwords Don't Match")

        return cd

    '''set the local government area field to none until a state is selected'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['local_government_area'].queryset = LocalGovernmentArea.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['local_government_area'].queryset = LocalGovernmentArea.objects.filter(
                    state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['local_government_area'].queryset = self.instance.state.localgovernmentarea_set.all()

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'confirm_password', 'first_name', 'last_name', 'user_image', 'address',
            'state', 'local_government_area', 'mobile_no', 'certificate_upload', 'specialization',)
        widgets = {
            'specialization': forms.TextInput(attrs={'placeholder': "for veterinary doctor's only"}),
            'email': forms.TextInput(
                attrs={'placeholder': "enter your email here"}),
            'confirm_password': forms.TextInput(
                attrs={'placeholder': "enter the password again"}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'user_image', 'address', 'state',
            'local_government_area',
            'mobile_no', 'certificate_upload', 'specialization',)
        widgets = {
            'specialization': forms.TextInput(attrs={'placeholder': "for veterinary doctor's only"}),
            'email': forms.TextInput(
                attrs={'placeholder': "enter your email here"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['local_government_area'].queryset = LocalGovernmentArea.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['local_government_area'].queryset = LocalGovernmentArea.objects.filter(
                    state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['local_government_area'].queryset = self.instance.state.localgovernmentarea_set.all()


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "enter your old password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "enter a new password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Re-enter the new password"}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2', )


