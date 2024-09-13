from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



class Register_User(forms.ModelForm):
    """
    Formulário de registro de usuários.
    Este formulário é utilizado para criar um novo usuário no sistema, 
    com validação adicional para senhas e campos de nome.

    Atributos:
        password (CharField): Campo de senha com widget de entrada oculta.
        password2 (CharField): Campo de confirmação de senha com widget de entrada oculta.
    
    Métodos: clean(): Realiza a validação dos campos e garante que os nomes 
                 'first_name' e 'last_name' não sejam iguais.
        clean_password(): Valida a senha utilizando as validações padrão do Django.
        clean_password2(): Verifica se as senhas inseridas são iguais.
        clean_username(): Valida se o nome de usuário já está em uso.
        clean_email(): Valida se o email já está em uso.
        save(): Salva o usuário no banco de dados após criptografar a senha.
    """

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
    """
    Formulário de login de usuários.

    Este formulário é utilizado para autenticar um usuário com base no nome de usuário 
    e senha.

    Atributos:
        username (CharField): Campo de nome de usuário.
        password (CharField): Campo de senha com widget de entrada oculta.
    """

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
     
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))


class Update_User(forms.ModelForm):
    """
    Formulário de atualização de usuários.

    Este formulário permite que os usuários atualizem seus dados pessoais, 
    como nome, sobrenome, email e nome de usuário.

    Métodos: clean(): Realiza a validação dos campos e garante que os nomes 
                 'first_name' e 'last_name' não sejam iguais.
        clean_email(): Verifica se o email inserido já está em uso por outro usuário.
        clean_username(): Verifica se o nome de usuário já está em uso por outro usuário.
        save(): Salva as alterações no banco de dados.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error('email', ValidationError('Email já existe', code='invalid'))
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        current_username = self.instance.username
        if current_username != username:
            if User.objects.filter(username=username).exists():
                self.add_error('username', ValidationError('Usuário já existe.', code='invalid'))
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
