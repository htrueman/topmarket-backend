from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms.utils import ErrorList
from django.contrib.auth.password_validation import validate_password


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    def clean(self):
        email = self.cleaned_data['email'].lower()
        password = self.cleaned_data['password1']
        if CustomUser.objects.filter(email=email).exists():
            msg = 'Email already exists.'
            self._errors['email'] = ErrorList([msg])
            del self.cleaned_data['email']
        else:
            validate_password(password)
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('email', 'password')