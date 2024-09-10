from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label='نوم او تخلص',
        widget=forms.TextInput(
           attrs={'placeholder': 'مثلا: فضل الله ماموند',}
           )
        )
    email = forms.EmailField(
        label='ایمیل آدرس',
        widget=forms.EmailInput(
           attrs={'placeholder': 'خپل ایمیل ادرس ولیکی'}
            )
        )
    password1 = forms.CharField(
        label='پاسورډ',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'خپل پاسورډ ادرس ولیکی'}
            )
        )
    password2 = forms.CharField(
        label='تکرار پاسورډ',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'خپل پاسورډ بیا ادرس ولیکی'}
            )
        )
    
    error_messages = {
        'password_mismatch': "پاسورډ یو شان نه دی",
    }
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("ایمیل مخکی استفاده شوی")
        return email

    class Meta:
        model = User
        fields=['full_name', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل آدرس',
        widget=forms.EmailInput(
           attrs={'placeholder': 'خپل ایمیل ادرس ولیکی'}
        )
    )
    password = forms.CharField(
        label='پاسورډ',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'خپل پاسورډ ادرس ولیکی'}
        )
    )