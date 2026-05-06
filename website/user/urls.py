from django.urls import path
#from django.urls import path, reverse_lazy
from .views import login, register, logout_view, activate, check_email
from django.contrib.auth import views as auth_views
#from .forms import celery_token

app_name = 'user'

urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout_view, name='logout'),
    #path('check_email/', check_email, name="check_email"),
    #path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    #path('password_reset/', 
     #    auth_views.PasswordResetView.as_view(
      #       form_class=celery_token,
       #      template_name='password_reset/password_reset_form.html', 
        #     success_url=reverse_lazy('user:password_reset_done'), 
         #    email_template_name='password_reset/password_reset_email.html'
         #), 
         #name='password_reset'),
    
    #path('password_reset/done/', 
     #    auth_views.PasswordResetDoneView.as_view(
      #       template_name='password_reset/password_reset_done.html'
       #  ), 
        # name='password_reset_done'),
    
    #path('reset/<uidb64>/<token>/', 
     #    auth_views.PasswordResetConfirmView.as_view(
      #       template_name='password_reset/password_reset_confirm.html',
       #      success_url=reverse_lazy('user:password_reset_complete') 
        # ), 
         #name='password_reset_confirm'),
    
    #path('reset/done/', 
     #    auth_views.PasswordResetCompleteView.as_view(
      #       template_name='password_reset/password_reset_complete.html'
       #  ), 
        # name='password_reset_complete'),

    path('password_reset/', auth_views.CustomPasswordChangeView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.CustomPasswordChangeDoneView.as_view(), name='password_reset_complete'),

]
