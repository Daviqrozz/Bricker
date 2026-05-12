from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('api.urls')),
  path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
  path('accounts/', include('django.contrib.auth.urls')),
]
