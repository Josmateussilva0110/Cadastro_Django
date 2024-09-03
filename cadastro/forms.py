from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



class Register_User(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
        label='password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label='confirm password'
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password',]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your e-mail'}),
        }
    

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name == last_name:
            msg = ValidationError('Os nomes precisa ser diferentes.', code='invalid')
            self.add_error('last_name', msg)
    
        return cleaned_data
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)
        return password
    
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError('As senhas precisa ser iguais.')
        return password2


    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError('Usuário ja existe.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email já existe.')
        return email


    def save(self, commit=True):
        person = super().save(commit=False)
        person.password = make_password(self.cleaned_data['password'])
        if commit:
            person.save()
        return person


class Login_user(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
     
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))
    