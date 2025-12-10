from django.contrib import admin
from django.urls import path, include

# You do NOT need 'from . import views' here if you use include()

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the apps
    path('', include('layout.urls')),
    path('', include('datafeed.urls')),
    path('', include('feedbackform.urls')),
    path('', include('users.urls')), # This handles ragister/ and verify_otp/
    
    # ... keep your password reset paths here if they are custom ...
    path('account/', include('django.contrib.auth.urls')),
]