#import threading
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib import messages
from .forms import AuthForm, UserForm, RecoveryForm
#from django.contrib.auth.tokens import default_token_generator
#from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#from django.utils.encoding import force_bytes
#from django.contrib.sites.shortcuts import get_current_site
#from .tasks import send_token_email_sync
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


User = get_user_model()

def login(request):
    
    if request.method == 'POST':
    
        form = AuthForm(request, data=request.POST)
    
        if form.is_valid():
    
            user = form.get_user()
            auth_login(request, user) 

            request.session['cart'] = {} 
            request.session.modified = True 
            
            redirect_to = request.GET.get('next') or resolve_url('index')
            return redirect(redirect_to)  
    
        else:
            messages.error(request, "Correo o contraseña incorrecta")
    
    else:
        
        form = AuthForm()
    
    return render(request, 'login/login.html', {'form': form})

def register(request):
    
    if request.method == 'POST':
        
        form = UserForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_active = True  
            user.save()

            messages.success(request, f"¡Registro exitoso, {user.username}! Ya puedes iniciar sesión.")
            
            return redirect('user:login')
        
        else:
            messages.error(request, "Por favor completa los campos correctamente.")
    else:
        form = UserForm()
    
    return render(request, 'register/register.html', {'form': form})

# Logica de activacion de correo electronico mediante token

"""

def check_email(request):

    return render(request, 'user/check_email.html')

def activate(request, uidb64, token):
    
    try:
        
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    
        user = None

    if user is not None and default_token_generator.check_token(user, token):
    
        user.is_active = True
        user.save()
        messages.success(request, "¡Cuenta activada con éxito! Ya puedes iniciar sesión.")
        return redirect('user:login')
    
    else:
        
        return render(request, 'register/activation_invalid.html')

"""

def custom_password_reset(request):
    
    if request.user.is_authenticated:
        
        return redirect('user:home') 

    if request.method == 'POST':
        
        form = RecoveryForm(request.POST)
        
        if form.is_valid():
            
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('nueva_contraseña')
            
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return redirect('user:password_reset_complete')
    
    else:
    
        form = RecoveryForm()
        
    return render(request, 'password_reset/password_reset_form.html', {'form': form})

def custom_password_reset_complete(request):
    
    return render(request, 'password_reset/password_reset_complete.html')

def logout_view(request):
    
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request, "Has cerrado sesion.")
    
    return redirect('index') 