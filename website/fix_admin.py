import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings') # Cambia 'tu_proyecto' por el nombre de tu carpeta de config
django.setup()

from user.models import User

def fix_user():
    try:
        u = User.objects.get(email='guillen993mi@gmail.com')
        u.is_admin = True
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print("¡Usuario actualizado con éxito!")
    except User.DoesNotExist:
        print("El usuario no existe.")

if __name__ == "__main__":
    fix_user()
