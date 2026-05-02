from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser):
    
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

    @property
    def is_staff(self):
        
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
