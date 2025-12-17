from django.urls import path
from django.contrib.auth import views as auth_views
from users import views  # Import from the 'users' app

urlpatterns = [
   # --- ADDED: Explicit Login/Logout URLs for Normal Users ---
    # This ensures 'login' resolves to your custom template (login.html)
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   
    # Added trailing slash '/' to prevent POST data loss during redirects
    path('ragister/', views.ragister, name='ragister'),

    # New URL for OTP Verification
    path('verify_otp/', views.verify_otp, name='verify_otp'),

    # --- NEW: WhatsApp URLs ---
    path('whatsapp-login/', views.whatsapp_login, name='whatsapp_login'),
    path('whatsapp-verify/', views.whatsapp_verify, name='whatsapp_verify'),
    
    # --- Password Reset Patterns ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]