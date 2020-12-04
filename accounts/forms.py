from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

class PwdChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=_('Old Password'), widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('Old Password'), 'id': 'form-oldpass'}
        )
    )
    new_password1 = forms.CharField(
        label=_('New Password'), widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('New Password'), 'id': 'form-newpass'}
        )
    )
    new_password2 = forms.CharField(
        label=_('Repeat Password'), widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('New Password'), 'id': 'form-newpass2'}
        )
    )

class PwdResetConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label=_('New password'), widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('New Password'), 'id': 'form-newpass'}
        )
    )
    new_password2 = forms.CharField(
        label=_('Repeat password'), widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('New Password'), 'id': 'form-newpass2'}
        )
    )

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': _('Email'), 'id': 'form-email'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)

        if not test:
            raise ValidationError(_('Unfortunately, we cannot find that email address.'))
        return email

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control bm-3', 'placeholder': _('Username'), 'id': 'login-username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password'), 'id': 'login-pwd'}
    ))

class RegistrationForm(forms.ModelForm):

    username = forms.CharField(
        label=_('Enter Username'), min_length=4, max_length=50, help_text=_('Required'))

    email = forms.EmailField(max_length=100, help_text=_('Required'), error_messages={
        'required': _('Sorry, you will need an email address.')
    })

    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError(_('Username already exists.'))
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError(_('Passwords do not match.'))
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Please use another Email address, that one is already taken.'))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': _('Username')}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': _('E-mail'), 'name': 'email'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Password')}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Repeat Password')}
        )

class UserEditForm(forms.ModelForm):

    first_name = forms.CharField(
        label=_('First Name'), min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('First Name'), 'id': 'form-firstname'}
        )
    )

    last_name = forms.CharField(
        label=_('Last Name'), min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('Last Name'), 'id': 'form-lastname'}
        )
    )

    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': _('E-mail Address'), 'id': 'form-email'}
        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Please use another E-mail, that one is already taken.')
        )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = False
        self.fields['email'].required = False