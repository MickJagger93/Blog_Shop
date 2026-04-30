from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .tasks import send_token

User = get_user_model()

class AuthForm(AuthenticationForm):
    
    username = forms.EmailField(label='Email', max_length=254)

    def confirm_login_allowed(self, user):
        
        if not user.is_active:
            raise ValidationError("This user is not active.", code='inactive')

class UserForm(UserCreationForm):
    
    email = forms.EmailField(label='Email', max_length=254)
    username = forms.CharField(label='Username', max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already exist a user with this email.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class celery_token(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string

        body = render_to_string(email_template_name, context)
        
        send_token.delay(
            subject="Password Reset Requested",
            message=body,
            recipient_list=[to_email]
        )