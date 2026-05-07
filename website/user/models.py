from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields): 
        
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)     
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(verbose_name='Correo electrónico', max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True, verbose_name='Nombre de usuario')
    
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    is_admin = models.BooleanField(default=False, verbose_name="¿Es administrador?")   
    
    username = models.CharField(max_length=150, unique=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    class Meta:

        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        
        return self.username if self.username else self.email

    is_staff = models.BooleanField(default=False, verbose_name="Acceso al admin")
