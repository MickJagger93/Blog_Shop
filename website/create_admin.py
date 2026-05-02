import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings') 
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'Jagger93'
email = 'guillen993mi@gmail.com'
password = 'Test44%%'

try:
    
    User.objects.filter(email='Mick93').delete()
    User.objects.filter(username=username).delete()
    User.objects.filter(email=email).delete()
    
    User.objects.create_superuser(username, email, password)
    print(f"✅ ÉXITO: Superusuario '{username}' creado desde cero.")

except Exception as e:
    print(f"⚠️ Nota: {e}")

