#import threading
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
#from .tasks import send_token_email_sync

User = get_user_model()

class AuthForm(AuthenticationForm):
    
    username = forms.EmailField(label='Email', max_length=254)

    def confirm_login_allowed(self, user):
        
        if not user.is_active:
            raise ValidationError("Esta cuenta no está activa.", code='inactive')

class UserForm(UserCreationForm):
    
    email = forms.EmailField(label='Email', max_length=254)
    username = forms.CharField(label='Username', max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already exist a user with this email.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

"""

class celery_token(PasswordResetForm):
    
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        
        from django.template.loader import render_to_string

        subject = "Password Reset Requested"
        body = render_to_string(email_template_name, context)
        
        thread = threading.Thread(
            target=send_token_email_sync,
            kwargs={
                'subject': subject,
                'message': body,
                'user_email': to_email
            }
        )
        thread.start()

"""

class RecoveryForm(forms.Form):
    
    email = forms.EmailField(
        label="Tu correo electrónico", 
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    
    nueva_contraseña = forms.CharField(
        label="Nueva contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )
    
    confirmar_contraseña = forms.CharField(
        label="Confirma tu nueva contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )

    def clean_email(self):
        
        email = self.cleaned_data.get('email').lower()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No existe ninguna cuenta registrada con este correo.")
        return email

    def clean(self):
        
        cleaned_data = super().clean()
        password = cleaned_data.get("nueva_contraseña")
        confirm = cleaned_data.get("confirmar_contraseña")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Las contraseñas nuevas no coinciden.")
        return cleaned_data